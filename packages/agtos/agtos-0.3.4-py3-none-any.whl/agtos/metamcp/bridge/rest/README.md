# REST Bridge Package

This package implements the REST API to MCP tool bridge, allowing any REST API to be exposed as MCP tools.

## Purpose

The REST bridge automatically generates MCP tools from OpenAPI specifications, handling authentication, request building, and response processing. It enables seamless integration of REST APIs like GitHub, Stripe, or custom APIs into the agtos ecosystem.

## Module Breakdown

- **`core.py`** (~306 lines) - Main RESTBridge class and tool generation
  - `RESTBridge` class for managing REST API connections
  - Tool generation from OpenAPI specs
  - Integration with the service registry

- **`auth.py`** (~202 lines) - Authentication handling
  - Bearer token authentication
  - API key authentication (header and query)
  - Basic authentication
  - Credential management integration

- **`openapi.py`** (~351 lines) - OpenAPI specification parsing
  - Parse OpenAPI/Swagger specs
  - Extract operations and schemas
  - Generate parameter definitions
  - Handle complex nested schemas

- **`execution.py`** (~311 lines) - Request execution and response handling
  - Build HTTP requests from tool calls
  - Execute requests with proper auth
  - Handle responses and errors
  - Format responses for MCP

## Key Classes and Functions

### RESTBridge (core.py)
```python
bridge = RESTBridge()
tools = bridge.discover_rest_tools("github", {
    "base_url": "https://api.github.com",
    "openapi_spec": "https://api.github.com/openapi.json",
    "auth": {"type": "bearer", "token": "..."}
})
```

### Authentication (auth.py)
```python
auth_handler = create_auth_handler({
    "type": "bearer",
    "token": "ghp_xxxxx"
})
headers = auth_handler.apply_auth({})  # Adds Authorization header
```

### OpenAPI Parsing (openapi.py)
```python
spec = load_openapi_spec("https://api.github.com/openapi.json")
operations = extract_operations(spec)
tool_spec = operation_to_tool(operations[0], "github")
```

### Execution (execution.py)
```python
result = await execute_rest_tool(
    tool_name="rest__github__create_issue",
    params={"owner": "agtos-ai", "repo": "agtos", "title": "Test"},
    config=service_config
)
```

## How Modules Work Together

1. **Discovery**: `core.py` uses `openapi.py` to parse API specs and generate tools
2. **Authentication**: `auth.py` provides auth handlers used by `execution.py`
3. **Execution**: `execution.py` builds requests using parsed schemas and auth
4. **Registry**: `core.py` registers generated tools with the service registry

The REST bridge supports dynamic tool generation, allowing new APIs to be integrated without code changes. It handles complex authentication scenarios and provides comprehensive error handling for robust API integration.