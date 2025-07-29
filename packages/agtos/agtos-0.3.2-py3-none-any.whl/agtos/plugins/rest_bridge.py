"""REST API Bridge Plugin for MCP.

This plugin automatically exposes all REST APIs from the knowledge store
as MCP tools. It bridges the gap between REST APIs and the MCP protocol.

AI_CONTEXT: This plugin is a key component of the Meta-MCP architecture.
It enables dynamic tool generation from API specifications without manual
coding. The plugin:

1. Loads on MCP server startup
2. Queries the knowledge store for all known APIs
3. Generates MCP-compatible tool definitions
4. Handles authentication and request execution
5. Provides structured responses with error handling

This allows AI assistants to interact with any REST API that has been
discovered through knowledge acquisition, making the system truly extensible.
"""
from ..metamcp.bridge.rest import generate_all_rest_tools

# Export tools for the MCP server
# This will be called by the plugin loader
TOOLS = generate_all_rest_tools()