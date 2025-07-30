"""Core CLI Bridge implementation for Meta-MCP Server.

This module contains the main CLIBridge class that coordinates the conversion
of CLI tools into MCP-compatible tools.

AI_CONTEXT:
    The CLIBridge class is the main entry point for CLI tool integration.
    It delegates specific tasks to specialized modules:
    - parser.py for help text parsing
    - discovery.py for tool discovery
    - execution.py for command execution
    
    This separation allows each module to focus on a single responsibility
    while the core module handles orchestration and caching.
"""

import logging
from typing import Dict, List, Any, Optional

from ....knowledge_store import get_knowledge_store
from ....knowledge.cli import CLIKnowledge
from ...types import ToolSpec, MCPRequest, MCPResponse, MCPError
from ...aliases import suggest_aliases_for_tool
from .parser import HelpTextParser
from .discovery import CLIDiscovery
from .execution import CommandExecutor

logger = logging.getLogger(__name__)


class CLIBridge:
    """Bridge that converts CLI tools into MCP-compatible tools.
    
    AI_CONTEXT:
        This class coordinates the conversion of CLI tools into MCP tools by:
        1. Using CLIDiscovery to find and analyze CLI tools
        2. Using HelpTextParser to generate JSON schemas
        3. Using CommandExecutor to run commands safely
        4. Maintaining a cache of discovered tools
        
        The bridge supports various CLI patterns and provides a unified
        interface for MCP clients to interact with any CLI tool.
    """
    
    def __init__(self):
        """Initialize the CLI bridge with specialized components."""
        self.store = get_knowledge_store()
        self.cli_knowledge = CLIKnowledge()
        self._tool_cache: Dict[str, ToolSpec] = {}
        
        # Initialize specialized components
        self.parser = HelpTextParser()
        self.discovery = CLIDiscovery(self.store, self.cli_knowledge, self.parser)
        self.executor = CommandExecutor()
        
    def discover_cli_tools(self, cli_names: Optional[List[str]] = None) -> List[ToolSpec]:
        """Discover available CLI tools and convert to MCP tool specs.
        
        Args:
            cli_names: Optional list of specific CLIs to discover.
                      If None, discovers all CLIs in knowledge store.
                      
        Returns:
            List of ToolSpec objects for discovered CLI tools
            
        AI_CONTEXT:
            This method delegates to CLIDiscovery for the actual discovery work,
            then caches the results for fast access during execution.
        """
        tools = self.discovery.discover_cli_tools(cli_names)
        
        # Cache discovered tools
        for tool in tools:
            self._tool_cache[tool.name] = tool
            
        return tools
    
    def execute_tool(self, request: MCPRequest) -> MCPResponse:
        """Execute a CLI tool based on an MCP request.
        
        Args:
            request: MCP request containing tool name and parameters
            
        Returns:
            MCP response with execution results
            
        AI_CONTEXT:
            This method validates the request, extracts tool information,
            and delegates to CommandExecutor for safe command execution.
            It handles all error cases and returns properly formatted
            MCP responses.
        """
        try:
            # Extract tool name from request
            tool_name = self._extract_tool_name(request)
            params = request.params or {}
            
            # Validate tool exists
            if tool_name not in self._tool_cache:
                return self._error_response(
                    request.id,
                    -32601,
                    f"Tool '{tool_name}' not found"
                )
            
            # Extract CLI components from tool name
            cli_name, subcommand = self._parse_tool_name(tool_name)
            
            # Execute command using executor
            result = self.executor.execute_cli_command(
                cli_name, 
                subcommand, 
                params
            )
            
            # Return formatted response
            return MCPResponse(
                id=request.id,
                result={
                    "content": [{
                        "type": "text",
                        "text": result["output"]
                    }],
                    "exit_code": result["exit_code"],
                    "error": result.get("error")
                }
            )
            
        except Exception as e:
            logger.error(f"Error executing CLI tool: {e}")
            return self._error_response(
                request.id,
                -32603,
                f"Internal error: {str(e)}"
            )
    
    def refresh_cli_knowledge(self, cli_name: str) -> bool:
        """Refresh knowledge for a specific CLI.
        
        Args:
            cli_name: Name of the CLI to refresh
            
        Returns:
            True if successful, False otherwise
            
        AI_CONTEXT:
            This method forces a refresh by clearing the cache and
            re-discovering the CLI. It's useful when CLI capabilities
            have changed or when troubleshooting issues.
        """
        try:
            # Clear cached tools for this CLI
            tools_to_remove = [
                name for name in self._tool_cache 
                if name.startswith(f"cli__{cli_name}")
            ]
            for tool_name in tools_to_remove:
                del self._tool_cache[tool_name]
            
            # Re-discover CLI using discovery module
            return self.discovery.refresh_cli_knowledge(cli_name)
            
        except Exception as e:
            logger.error(f"Error refreshing CLI knowledge for {cli_name}: {e}")
            return False
    
    def get_tool_by_name(self, tool_name: str) -> Optional[ToolSpec]:
        """Get a tool spec by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            ToolSpec or None if not found
        """
        return self._tool_cache.get(tool_name)
    
    def list_available_tools(self) -> List[str]:
        """List all available CLI tools.
        
        Returns:
            List of tool names
        """
        return list(self._tool_cache.keys())
    
    def _extract_tool_name(self, request: MCPRequest) -> str:
        """Extract tool name from MCP request.
        
        Args:
            request: MCP request
            
        Returns:
            Tool name string
            
        AI_CONTEXT:
            Handles different request formats for tool invocation,
            including the standard "tools/call/<name>" format.
        """
        if isinstance(request.method, str) and "tools/call" in request.method:
            return request.method.replace("tools/call", "").strip("/")
        else:
            # Direct tool name passed
            return request.method if isinstance(request.method, str) else str(request.method)
    
    def _parse_tool_name(self, tool_name: str) -> tuple[str, Optional[str]]:
        """Parse tool name to extract CLI and subcommand.
        
        Args:
            tool_name: Full tool name (e.g., "cli__git__status")
            
        Returns:
            Tuple of (cli_name, subcommand or None)
            
        AI_CONTEXT:
            Uses double underscore separator to reliably parse tool names.
            Handles both new format (cli__name__subcommand) and legacy
            format (cli_name_subcommand) for backward compatibility.
        """
        if not tool_name.startswith("cli__"):
            # Handle legacy format for backward compatibility
            cli_parts = tool_name.split("_")[1:]  # Remove 'cli_' prefix
            cli_name = cli_parts[0]
            subcommand = "_".join(cli_parts[1:]).replace("_", "-") if len(cli_parts) > 1 else None
        else:
            # New format with double underscore separator
            parts = tool_name.split("__")
            if len(parts) >= 2:
                cli_name = parts[1]
                subcommand = parts[2] if len(parts) > 2 else None
            else:
                raise ValueError(f"Invalid tool name format: {tool_name}")
        
        return cli_name, subcommand
    
    def _error_response(self, request_id: Optional[Any], code: int, message: str) -> MCPResponse:
        """Create an error response.
        
        Args:
            request_id: Request ID to echo back
            code: Error code
            message: Error message
            
        Returns:
            MCPResponse with error
        """
        return MCPResponse(
            id=request_id,
            error=MCPError(code=code, message=message).to_dict()
        )
    
    # Expose internal methods for testing (backward compatibility)
    def _create_tool_spec(self, cli_name: str, cli_data: Dict[str, Any]) -> Optional[ToolSpec]:
        """Create a tool spec for a CLI command. Delegates to discovery module."""
        return self.discovery._create_tool_spec(cli_name, cli_data)
    
    def _parse_help_text(self, help_text: str) -> Dict[str, Any]:
        """Parse help text to extract arguments and flags. Delegates to parser."""
        return self.parser.parse_help_text(help_text)
    
    def _build_command(self, cli_name: str, subcommand: Optional[str], params: Dict[str, Any]) -> List[str]:
        """Build command line from parameters. Delegates to executor."""
        return self.executor._build_command(cli_name, subcommand, params)
    
    def _execute_command(self, command: List[str], working_directory: Optional[str] = None) -> Dict[str, Any]:
        """Execute a command and return results. Delegates to executor."""
        return self.executor._execute_command(command, working_directory)
    
    def _extract_description(self, help_text: str, command: str) -> str:
        """Extract a description from help text. Delegates to parser."""
        return self.parser.extract_description(help_text, command)
    
    def _create_schema_from_parsed_help(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Create JSON schema from parsed help text. Delegates to parser."""
        return self.parser.create_schema_from_parsed_help(parsed)