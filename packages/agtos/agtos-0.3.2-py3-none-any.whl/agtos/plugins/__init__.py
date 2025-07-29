"""Plugin discovery and loading."""
import importlib
import pkgutil
import sys
from pathlib import Path
from typing import Dict, Any

def get_all_tools() -> Dict[str, Any]:
    """Discover and merge all plugin TOOLS.
    
    Scans the plugins directory for Python modules that export a TOOLS
    dictionary and merges them into a single registry.
    
    AI_CONTEXT:
        This function now also checks for user_tools that have been
        loaded dynamically, but does NOT load them directly - that's
        handled by the hot_reload module.
    """
    all_tools = {}
    
    # Get the plugins package path
    plugins_dir = Path(__file__).parent
    
    # Import all modules in the plugins package
    for file_path in plugins_dir.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
        
        module_name = file_path.stem
        
        try:
            # Import the module
            module = importlib.import_module(f"agtos.plugins.{module_name}")
            
            # Check if module has TOOLS
            if hasattr(module, "TOOLS"):
                tools = getattr(module, "TOOLS")
                if isinstance(tools, dict):
                    # Check for conflicts
                    for tool_name in tools:
                        if tool_name in all_tools:
                            print(f"⚠️  Warning: Tool '{tool_name}' already exists, skipping duplicate from {module_name}", file=sys.stderr)
                        else:
                            all_tools[tool_name] = tools[tool_name]
                    
                    print(f"✅ Loaded {len(tools)} tools from {module_name}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Failed to load plugin {module_name}: {e}", file=sys.stderr)
    
    return all_tools

def validate_tool_schema(tool_name: str, tool_data: Dict[str, Any]) -> bool:
    """Validate that a tool has the required structure.
    
    Args:
        tool_name: Name of the tool
        tool_data: Tool configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["schema", "func", "description"]
    
    for field in required_fields:
        if field not in tool_data:
            print(f"❌ Tool '{tool_name}' missing required field: {field}", file=sys.stderr)
            return False
    
    # Check that func is callable
    if not callable(tool_data["func"]):
        print(f"❌ Tool '{tool_name}' func is not callable", file=sys.stderr)
        return False
    
    # Check schema structure
    schema = tool_data["schema"]
    if not isinstance(schema, dict) or "type" not in schema:
        print(f"❌ Tool '{tool_name}' has invalid schema", file=sys.stderr)
        return False
    
    return True

def get_plugin(plugin_name: str) -> Any:
    """Get a specific plugin module by name.
    
    Args:
        plugin_name: Name of the plugin to load
        
    Returns:
        The plugin module or None if not found
    """
    try:
        # Import the module
        module = importlib.import_module(f"agtos.plugins.{plugin_name}")
        return module
    except ImportError:
        return None