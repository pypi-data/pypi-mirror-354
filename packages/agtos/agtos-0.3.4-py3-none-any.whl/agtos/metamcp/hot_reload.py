"""Hot-reload functionality for dynamically created tools.

AI_CONTEXT:
    This module provides hot-reload capabilities for user-created tools in agtos.
    When a new tool is created via tool_creator.create, it can be immediately
    loaded into the Meta-MCP registry without restarting the server.
    
    Key features:
    - Monitor ~/.agtos/user_tools/ for changes
    - Dynamically load single tools or tool modules
    - Thread-safe updates to the registry
    - Integration with tool creation workflow
    
    Architecture:
    1. FileWatcher monitors user_tools directory
    2. ToolLoader dynamically imports and validates tools
    3. HotReloader coordinates updates to the registry
    4. Thread safety via asyncio locks
"""

import asyncio
import importlib
import importlib.util
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Set, Callable
from datetime import datetime
import threading

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Create dummy classes to avoid import errors
    FileSystemEventHandler = object
    FileCreatedEvent = object
    FileModifiedEvent = object
    Observer = None

from .types import ToolSpec
from .registry import ServiceRegistry

logger = logging.getLogger(__name__)


class ToolFileHandler(FileSystemEventHandler):
    """Handles file system events for tool hot-reload.
    
    AI_CONTEXT:
        This handler watches for new or modified Python files in the user_tools
        directory and triggers reload when changes are detected.
    """
    
    def __init__(self, callback: Callable[[Path], None]):
        """Initialize with callback for tool changes.
        
        Args:
            callback: Function to call with path when a tool file changes
        """
        self.callback = callback
        self._debounce_timers: Dict[str, threading.Timer] = {}
        self._debounce_delay = 0.5  # seconds
    
    def on_created(self, event: FileCreatedEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and event.src_path.endswith('.py'):
            self._debounced_callback(Path(event.src_path))
    
    def on_modified(self, event: FileModifiedEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.py'):
            self._debounced_callback(Path(event.src_path))
    
    def _debounced_callback(self, path: Path) -> None:
        """Debounce rapid file changes to avoid multiple reloads.
        
        AI_CONTEXT:
            File saves often trigger multiple events. This debouncer ensures
            we only reload once after changes have settled.
        """
        # Cancel existing timer for this file
        if str(path) in self._debounce_timers:
            self._debounce_timers[str(path)].cancel()
        
        # Start new timer
        timer = threading.Timer(
            self._debounce_delay,
            lambda: self.callback(path)
        )
        self._debounce_timers[str(path)] = timer
        timer.start()


class ToolLoader:
    """Dynamically loads and validates user-created tools.
    
    AI_CONTEXT:
        This class handles the actual loading of Python modules from the
        user_tools directory. It validates tool structure and converts
        them to the format expected by the Meta-MCP registry.
    """
    
    def __init__(self):
        """Initialize the tool loader."""
        self._loaded_modules: Dict[str, Any] = {}
    
    def load_tool_file(self, tool_path: Path) -> Optional[Dict[str, Any]]:
        """Load a tool from a Python file.
        
        Args:
            tool_path: Path to the tool Python file
            
        Returns:
            Dictionary of tool_name -> tool_data or None if loading fails
        """
        try:
            # Get module name from file
            module_name = f"agtos.user_tools.{tool_path.stem}"
            
            # Create module spec
            spec = self._create_module_spec(module_name, tool_path)
            if not spec:
                return None
            
            # Load or reload module
            module = self._load_or_reload_module(module_name, spec)
            
            # Store reference
            self._loaded_modules[str(tool_path)] = module
            
            # Extract tools from module
            tools = self._extract_tools_from_module(module)
            
            # Load and apply metadata
            self._load_tool_metadata(tool_path, tools)
            
            return tools
            
        except Exception as e:
            logger.error(f"Failed to load tool from {tool_path}: {e}")
            return None
    
    def _create_module_spec(self, module_name: str, tool_path: Path) -> Optional[importlib.machinery.ModuleSpec]:
        """Create module spec for the tool file.
        
        Args:
            module_name: Name for the module
            tool_path: Path to the tool file
            
        Returns:
            Module spec or None if creation fails
        """
        spec = importlib.util.spec_from_file_location(module_name, tool_path)
        if not spec or not spec.loader:
            logger.error(f"Failed to create spec for {tool_path}")
            return None
        return spec
    
    def _load_or_reload_module(self, module_name: str, spec: importlib.machinery.ModuleSpec) -> Any:
        """Load a new module or reload if already loaded.
        
        Args:
            module_name: Module name
            spec: Module spec
            
        Returns:
            Loaded module
        """
        if module_name in sys.modules:
            # Reload existing module
            module = importlib.reload(sys.modules[module_name])
            logger.info(f"Reloaded tool module: {module_name}")
        else:
            # Load new module
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            logger.info(f"Loaded new tool module: {module_name}")
        
        return module
    
    def _extract_tools_from_module(self, module: Any) -> Dict[str, Any]:
        """Extract all tools from a module.
        
        Args:
            module: The loaded module
            
        Returns:
            Dictionary of tool_name -> tool_data
        """
        tools = {}
        
        # Check for TOOLS dictionary (standard format)
        if hasattr(module, "TOOLS") and isinstance(module.TOOLS, dict):
            tools.update(module.TOOLS)
        
        # Check for decorated tool functions
        decorated_tools = self._extract_decorated_tools(module)
        tools.update(decorated_tools)
        
        return tools
    
    def _extract_decorated_tools(self, module: Any) -> Dict[str, Any]:
        """Extract tools from decorated functions.
        
        Args:
            module: The loaded module
            
        Returns:
            Dictionary of tool_name -> tool_data for decorated tools
        """
        tools = {}
        
        for attr_name in dir(module):
            if attr_name.startswith("_"):
                continue
                
            attr = getattr(module, attr_name)
            if hasattr(attr, "_mcp_tool"):
                # Function decorated with tool metadata
                tool_info = attr._mcp_tool
                tools[tool_info["name"]] = {
                    "func": attr,
                    "schema": tool_info["schema"],
                    "description": tool_info["description"],
                    "version": tool_info.get("version", "1.0")
                }
        
        return tools
    
    def _load_tool_metadata(self, tool_path: Path, tools: Dict[str, Any]) -> None:
        """Load metadata from JSON file and apply to tools.
        
        Args:
            tool_path: Path to the tool file
            tools: Dictionary of tools to enhance with metadata
        """
        metadata_path = tool_path.with_suffix(".json")
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text())
                # Enhance tools with metadata
                for tool_name in tools:
                    if "metadata" not in tools[tool_name]:
                        tools[tool_name]["metadata"] = metadata
            except Exception as e:
                logger.warning(f"Failed to load metadata for {tool_path}: {e}")
    
    def validate_tool(self, tool_name: str, tool_data: Dict[str, Any]) -> bool:
        """Validate tool structure and requirements.
        
        Args:
            tool_name: Name of the tool
            tool_data: Tool configuration
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["func", "schema", "description"]
        
        for field in required_fields:
            if field not in tool_data:
                logger.error(f"Tool '{tool_name}' missing required field: {field}")
                return False
        
        # Check that func is callable
        if not callable(tool_data["func"]):
            logger.error(f"Tool '{tool_name}' func is not callable")
            return False
        
        # Check schema structure
        schema = tool_data["schema"]
        if not isinstance(schema, dict) or "type" not in schema:
            logger.error(f"Tool '{tool_name}' has invalid schema")
            return False
        
        return True


class HotReloader:
    """Manages hot-reload functionality for user-created tools.
    
    AI_CONTEXT:
        This is the main class that coordinates hot-reload functionality.
        It watches the user_tools directory, loads new/modified tools,
        and updates the Meta-MCP registry dynamically.
    """
    
    def __init__(self, registry: ServiceRegistry):
        """Initialize hot reloader with registry reference.
        
        Args:
            registry: The Meta-MCP service registry to update
        """
        self.registry = registry
        self.loader = ToolLoader()
        self.observer: Optional[Observer] = None
        self._reload_lock = asyncio.Lock()
        self._loaded_tools: Set[str] = set()
        self.user_tools_dir = Path.home() / ".agtos" / "user_tools"
        
        # Ensure user tools directory exists
        self.user_tools_dir.mkdir(parents=True, exist_ok=True)
    
    async def start_watching(self) -> None:
        """Start watching the user_tools directory for changes.
        
        AI_CONTEXT:
            This method starts a background file watcher that monitors
            the user_tools directory. When files change, it triggers
            automatic reload of the affected tools.
        """
        # Load existing tools first
        await self.load_all_user_tools()
        
        if not WATCHDOG_AVAILABLE:
            logger.warning("Watchdog not available. Hot-reload will not monitor file changes automatically.")
            logger.info("Install watchdog with: pip install watchdog")
            return
        
        if self.observer and self.observer.is_alive():
            logger.warning("File watcher already running")
            return
        
        # Setup file watcher
        event_handler = ToolFileHandler(
            callback=lambda path: asyncio.create_task(self.reload_tool(path))
        )
        
        self.observer = Observer()
        self.observer.schedule(
            event_handler,
            str(self.user_tools_dir),
            recursive=False
        )
        
        self.observer.start()
        logger.info(f"Started watching {self.user_tools_dir} for tool changes")
    
    def stop_watching(self) -> None:
        """Stop watching for file changes."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped file watcher")
    
    async def load_all_user_tools(self) -> None:
        """Load all existing user tools from the directory.
        
        AI_CONTEXT:
            This method is called on startup to load any tools that
            were created in previous sessions.
        """
        logger.info("Loading existing user tools...")
        
        for tool_file in self.user_tools_dir.glob("*.py"):
            if not tool_file.name.startswith("_"):
                await self.reload_tool(tool_file)
    
    async def reload_tool(self, tool_path: Path) -> bool:
        """Reload a specific tool file.
        
        Args:
            tool_path: Path to the tool Python file
            
        Returns:
            True if successfully reloaded, False otherwise
        """
        async with self._reload_lock:
            try:
                logger.info(f"Reloading tool: {tool_path.name}")
                
                # Load the tool file
                tools = self.loader.load_tool_file(tool_path)
                if not tools:
                    logger.error(f"No tools found in {tool_path}")
                    return False
                
                # Validate all tools
                valid_tools = {}
                for tool_name, tool_data in tools.items():
                    if self.loader.validate_tool(tool_name, tool_data):
                        valid_tools[tool_name] = tool_data
                    else:
                        logger.warning(f"Skipping invalid tool: {tool_name}")
                
                if not valid_tools:
                    logger.error(f"No valid tools in {tool_path}")
                    return False
                
                # Update registry
                await self._update_registry(tool_path.stem, valid_tools)
                
                # Track loaded tools
                self._loaded_tools.add(tool_path.stem)
                
                logger.info(f"Successfully loaded {len(valid_tools)} tools from {tool_path.name}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to reload tool {tool_path}: {e}")
                return False
    
    async def _update_registry(self, service_name: str, tools: Dict[str, Any]) -> None:
        """Update the service registry with new/updated tools.
        
        AI_CONTEXT:
            This method updates the Meta-MCP registry to include the
            newly loaded tools. It creates or updates a service entry
            for user-created tools.
        """
        # Prepare service name
        full_service_name = f"user_tools.{service_name}"
        
        # Check if service already exists
        if full_service_name in self.registry.services:
            # Update existing service
            logger.info(f"Updating existing service: {full_service_name}")
            await self.registry.unregister_service(full_service_name)
        
        # Register as plugin service
        await self.registry.register_plugin_service(
            full_service_name,
            {
                "description": f"User-created tools: {service_name}",
                "tools": tools
            }
        )
    
    async def reload_specific_tool(self, tool_name: str) -> bool:
        """Reload a specific tool by name.
        
        Args:
            tool_name: Name of the tool file (without .py extension)
            
        Returns:
            True if successfully reloaded, False otherwise
        """
        tool_path = self.user_tools_dir / f"{tool_name}.py"
        
        if not tool_path.exists():
            logger.error(f"Tool file not found: {tool_path}")
            return False
        
        return await self.reload_tool(tool_path)
    
    def get_loaded_tools(self) -> Set[str]:
        """Get set of currently loaded user tool names."""
        return self._loaded_tools.copy()


# Singleton instance
_hot_reloader: Optional[HotReloader] = None


def get_hot_reloader(registry: ServiceRegistry) -> HotReloader:
    """Get or create the hot reloader instance.
    
    Args:
        registry: The Meta-MCP service registry
        
    Returns:
        The hot reloader singleton instance
    """
    global _hot_reloader
    
    if _hot_reloader is None:
        _hot_reloader = HotReloader(registry)
    
    return _hot_reloader


async def reload_user_tool(tool_name: str, registry: ServiceRegistry) -> bool:
    """Convenience function to reload a specific user tool.
    
    Args:
        tool_name: Name of the tool to reload
        registry: The Meta-MCP service registry
        
    Returns:
        True if successfully reloaded, False otherwise
    """
    reloader = get_hot_reloader(registry)
    return await reloader.reload_specific_tool(tool_name)