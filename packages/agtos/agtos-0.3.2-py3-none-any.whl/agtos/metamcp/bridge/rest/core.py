"""Core REST Bridge functionality for MCP.

This module contains the main RESTBridge class that coordinates
the conversion of REST APIs into MCP-compatible tools.

AI_CONTEXT: This is the central module of the REST bridge. It:
1. Loads API definitions from the knowledge store
2. Coordinates with other modules for auth, parsing, and execution
3. Generates MCP tool definitions with proper handlers
4. Manages the lifecycle of REST API tools

The bridge is designed to be stateless and safe for concurrent use,
making it suitable for integration with the MCP server.
"""
import sys
from typing import Dict, Any, List, Optional, Callable
from functools import wraps

from ....knowledge_store import get_knowledge_store
from .auth import AuthHandler
from .openapi import OpenAPIParser
from .execution import RequestExecutor, RateLimiter


class RESTBridge:
    """Bridge for converting REST APIs into MCP tools.
    
    AI_CONTEXT: This is the main bridge class that handles the conversion
    of REST APIs into MCP tools. It's designed to be stateless and safe
    for concurrent use. The bridge:
    
    1. Loads API definitions from the knowledge store
    2. Generates MCP tool definitions with proper JSON schemas
    3. Executes HTTP requests when tools are called
    4. Handles authentication transparently
    5. Provides detailed error information for debugging
    
    The bridge coordinates between specialized modules:
    - AuthHandler: Manages authentication and credentials
    - OpenAPIParser: Parses specs and generates schemas
    - RequestExecutor: Handles HTTP request execution
    
    Each generated tool includes:
    - Descriptive name based on operation ID or path
    - Clear description of what the endpoint does
    - JSON schema for parameters (path, query, body)
    - Proper error handling with actionable messages
    """
    
    def __init__(self):
        self.store = get_knowledge_store()
        self.auth_handler = AuthHandler()
        self.parser = OpenAPIParser()
        self.rate_limiter = RateLimiter()
        self.executor = RequestExecutor(self.rate_limiter)
    
    def generate_tools_for_api(self, api_name: str) -> Dict[str, Dict[str, Any]]:
        """Generate MCP tools from API knowledge.
        
        AI_CONTEXT: This method is the entry point for converting an API
        into MCP tools. It retrieves API knowledge from the store and
        generates a tool for each endpoint. The process:
        
        1. Retrieves API knowledge (OpenAPI spec or discovered endpoints)
        2. Extracts authentication requirements
        3. For each endpoint, generates:
           - Tool name (e.g., "github_list_repos")
           - Description from endpoint documentation
           - JSON schema from parameters and request body
           - Handler function that makes the HTTP request
        
        The generated tools are returned as a dictionary mapping tool names
        to tool definitions compatible with the MCP server.
        
        Args:
            api_name: Name or URL of the API in the knowledge store
            
        Returns:
            Dictionary of tool_name -> tool_definition
        """
        # Retrieve API knowledge
        knowledge = self.store.retrieve("api", api_name)
        if not knowledge:
            return {}
        
        api_data = knowledge["data"]
        tools = {}
        
        # Extract base URL
        base_url = api_data.get("base_url", api_data.get("url", ""))
        if not base_url:
            return {}
        
        # Process each endpoint
        endpoints = api_data.get("endpoints", [])
        for endpoint in endpoints:
            tool_name = self.parser.generate_tool_name(api_name, endpoint)
            tool_def = self._create_tool_definition(
                base_url=base_url,
                endpoint=endpoint,
                auth_methods=api_data.get("auth_methods", []),
                api_name=api_name,
                tool_name=tool_name
            )
            if tool_def:
                tools[tool_name] = tool_def
        
        return tools
    
    def _create_tool_definition(self, 
                               base_url: str,
                               endpoint: Dict[str, Any],
                               auth_methods: List[Dict[str, Any]],
                               api_name: str,
                               tool_name: str) -> Optional[Dict[str, Any]]:
        """Create MCP tool definition for an endpoint.
        
        AI_CONTEXT: This method creates a complete MCP tool definition
        for a REST endpoint. It coordinates between the parser for
        schema generation and creates a handler function that will
        execute the actual HTTP request.
        
        The handler function is created as a closure that captures
        the endpoint configuration, making each tool self-contained.
        
        Args:
            base_url: Base URL of the API
            endpoint: Endpoint configuration from API knowledge
            auth_methods: List of authentication methods for the API
            api_name: Name of the API for auth lookup
            tool_name: Generated tool name for alias registration
            
        Returns:
            Tool definition dict or None if invalid
        """
        # Build JSON schema for parameters
        schema = self.parser.build_parameter_schema(endpoint)
        
        # Create description
        description = self.parser.build_description(endpoint)
        
        # Create handler function
        handler = self._create_handler(
            base_url=base_url,
            endpoint=endpoint,
            auth_methods=auth_methods,
            api_name=api_name
        )
        
        # Generate and register aliases
        aliases = self.parser.generate_aliases(api_name, endpoint, tool_name)
        
        return {
            "description": description,
            "schema": schema,
            "func": handler,
            "version": "1.0.0",  # Required by plugin system
            "aliases": aliases  # Include aliases in tool definition
        }
    
    def _create_handler(self,
                       base_url: str,
                       endpoint: Dict[str, Any],
                       auth_methods: List[Dict[str, Any]],
                       api_name: str) -> Callable:
        """Create the handler function for a tool.
        
        AI_CONTEXT: This creates the actual function that gets called
        when the MCP tool is invoked. The handler coordinates between:
        1. AuthHandler for authentication headers
        2. RequestExecutor for HTTP execution
        
        The handler includes detailed error messages to help AI assistants
        debug issues without human intervention.
        
        Args:
            base_url: Base URL of the API
            endpoint: Endpoint configuration
            auth_methods: Authentication methods
            api_name: API name for auth lookup
            
        Returns:
            Callable that handles the tool execution
        """
        def handler(**kwargs) -> Dict[str, Any]:
            # Build headers with authentication
            headers = self.auth_handler.build_headers(auth_methods, api_name)
            
            # Determine method
            method = endpoint.get("method", "GET")
            
            # Execute request
            return self.executor.execute_request(
                method=method,
                base_url=base_url,
                endpoint=endpoint,
                params=kwargs,
                headers=headers
            )
        
        return handler
    
    def list_available_apis(self) -> List[Dict[str, Any]]:
        """List all APIs available in the knowledge store.
        
        AI_CONTEXT: This method provides a summary of all REST APIs
        that have been discovered or imported into the knowledge store.
        It's useful for:
        1. Showing users what APIs are available
        2. Debugging which APIs have been loaded
        3. Checking authentication status
        
        Returns:
            List of API summaries with name, type, and endpoint count
        """
        # Search for all API entries
        results = self.store.search("", type="api")
        
        apis = []
        for result in results:
            # Retrieve full data to get endpoint count
            knowledge = self.store.retrieve("api", result["name"])
            if knowledge:
                api_data = knowledge["data"]
                apis.append({
                    "name": result["name"],
                    "source": result["source"],
                    "discovered_via": api_data.get("method", "unknown"),
                    "endpoint_count": len(api_data.get("endpoints", [])),
                    "has_auth": bool(api_data.get("auth_methods", [])),
                    "created_at": result["created_at"]
                })
        
        return apis


def generate_all_rest_tools() -> Dict[str, Dict[str, Any]]:
    """Generate MCP tools for all REST APIs in the knowledge store.
    
    AI_CONTEXT: This is the main entry point for the REST bridge when
    integrating with the MCP server. It:
    
    1. Creates a RESTBridge instance
    2. Lists all available APIs in the knowledge store
    3. Generates tools for each API
    4. Returns a merged dictionary of all tools
    
    This function is designed to be called during MCP server startup
    to automatically expose all known REST APIs as MCP tools.
    
    Returns:
        Dictionary mapping tool names to tool definitions
    """
    bridge = RESTBridge()
    all_tools = {}
    
    # Get all APIs
    apis = bridge.list_available_apis()
    
    for api_info in apis:
        api_name = api_info["name"]
        try:
            # Generate tools for this API
            tools = bridge.generate_tools_for_api(api_name)
            
            # Add to collection
            for tool_name, tool_def in tools.items():
                if tool_name in all_tools:
                    # Handle naming conflicts
                    tool_name = f"{api_name}_{tool_name}"
                all_tools[tool_name] = tool_def
                
            if tools:
                print(f"✅ Generated {len(tools)} tools for {api_name}", file=sys.stderr)
                
        except Exception as e:
            print(f"❌ Failed to generate tools for {api_name}: {e}", file=sys.stderr)
    
    return all_tools


# Export for plugin system - use lazy loading to avoid import-time issues
_TOOLS_CACHE = None

def get_tools():
    """Get all REST tools with lazy loading.
    
    AI_CONTEXT: This function implements lazy loading to ensure tools
    are generated only after the knowledge store is populated, not at
    module import time. This prevents issues where:
    1. The knowledge store isn't ready yet
    2. Environment variables aren't set
    3. Import order causes missing dependencies
    
    The function caches results to avoid regenerating tools on every call.
    
    Returns:
        Dictionary of tool_name -> tool_definition
    """
    global _TOOLS_CACHE
    if _TOOLS_CACHE is None:
        _TOOLS_CACHE = generate_all_rest_tools()
    return _TOOLS_CACHE

# For backward compatibility - this will be an empty dict initially
# and populated on first access via get_tools()
TOOLS = {}