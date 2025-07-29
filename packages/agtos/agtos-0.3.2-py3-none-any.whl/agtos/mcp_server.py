"""Local MCP server implementation with full spec compliance."""
import asyncio
import json
import os
import signal
import subprocess
import sys
from typing import Dict, Any, Optional, Callable, Awaitable
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .plugins import get_all_tools
from .utils import is_port_in_use

# Global reference to loaded tools
TOOLS: Dict[str, Any] = {}
MCP_VERSION = "0.2"  # Latest MCP spec version
SERVER_INFO = {
    "name": "agtos",
    "version": "0.3.0",
    "vendor": "agtos"
}

# Method handler registry
METHOD_HANDLERS: Dict[str, Callable[[Dict[str, Any], Any], Awaitable[Dict[str, Any]]]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    global TOOLS
    TOOLS = get_all_tools()
    print(f"🔌 Loaded {len(TOOLS)} tools from plugins")
    for tool_name in TOOLS:
        print(f"   - {tool_name}")
    
    yield
    
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(title="agtos MCP Server", lifespan=lifespan)

# Add CORS middleware for broad compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def handle_initialize(request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP initialize request.
    
    AI_CONTEXT: Establishes MCP session with capability negotiation.
    Returns server info and supported capabilities.
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": MCP_VERSION,
            "serverInfo": SERVER_INFO,
            "capabilities": {
                "tools": True,
                "resources": False,  # Can add file/URL resources later
                "prompts": False,    # Can add prompt templates later
                "logging": True
            }
        }
    }


async def handle_tools_list(request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tools/list request.
    
    AI_CONTEXT: Returns all available tools with their schemas.
    Each tool includes name, description, and input schema.
    """
    tools_list = []
    for tool_name, tool_data in TOOLS.items():
        tools_list.append({
            "name": tool_name,
            "description": tool_data.get("description", ""),
            "inputSchema": tool_data["schema"]
        })
    
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"tools": tools_list}
    }


async def handle_tools_call(request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tools/call request.
    
    AI_CONTEXT: Executes a specific tool with provided parameters.
    Includes timeout handling and detailed error reporting.
    """
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    if tool_name not in TOOLS:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": f"Tool not found: {tool_name}"
            }
        }
    
    # Log tool execution
    print(f"⚡ Executing {tool_name} with args: {json.dumps(arguments, indent=2)}")
    
    try:
        # Execute tool with timeout
        tool_func = TOOLS[tool_name]["func"]
        result = await asyncio.wait_for(
            asyncio.to_thread(tool_func, **arguments),
            timeout=30.0
        )
        
        print(f"✅ {tool_name} completed successfully")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    except asyncio.TimeoutError:
        print(f"⏱️  {tool_name} timed out after 30s")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": "Tool execution timed out after 30 seconds"
            }
        }
    except Exception as e:
        print(f"❌ {tool_name} failed: {str(e)}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": f"Tool execution failed: {str(e)}"
            }
        }


async def handle_logging_setlevel(request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle logging/setLevel request.
    
    AI_CONTEXT: Updates the logging level for the server.
    Currently accepts the level but doesn't apply it.
    """
    level = params.get("level", "info")
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"level": level}
    }


# Register method handlers
METHOD_HANDLERS["initialize"] = handle_initialize
METHOD_HANDLERS["tools/list"] = handle_tools_list
METHOD_HANDLERS["tools/call"] = handle_tools_call
METHOD_HANDLERS["logging/setLevel"] = handle_logging_setlevel

@app.post("/")
async def handle_jsonrpc(request: Request):
    """Handle JSON-RPC 2.0 requests per MCP specification.
    
    AI_CONTEXT: Main entry point for MCP requests. Parses JSON-RPC,
    validates structure, and dispatches to appropriate handler.
    Uses method registry pattern for clean routing.
    
    Returns:
        JSONResponse with result or error per JSON-RPC 2.0 spec
    """
    # Parse JSON body
    body, parse_error = await _parse_json_body(request)
    if parse_error:
        return parse_error
    
    # Extract request components
    method = body.get("method")
    request_id = body.get("id")
    params = body.get("params", {})
    
    # Validate request structure
    validation_error = _validate_request_structure(method, request_id)
    if validation_error:
        return validation_error
    
    # Dispatch to handler
    return await _dispatch_to_handler(method, request_id, params)


async def _parse_json_body(request: Request):
    """Parse JSON body from request.
    
    Args:
        request: The HTTP request
        
    Returns:
        Tuple of (body dict, error response or None)
    """
    try:
        body = await request.json()
        return body, None
    except Exception:
        error = JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
        )
        return None, error


def _validate_request_structure(method: str, request_id: Any):
    """Validate JSON-RPC request structure.
    
    Args:
        method: The method name
        request_id: The request ID
        
    Returns:
        Error response dict or None if valid
    """
    if not method:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32600,
                "message": "Invalid request: missing method"
            }
        }
    return None


async def _dispatch_to_handler(method: str, request_id: Any, params: Dict[str, Any]):
    """Dispatch request to appropriate handler.
    
    Args:
        method: The method name
        request_id: The request ID
        params: Request parameters
        
    Returns:
        Handler response or error for unknown method
    """
    handler = METHOD_HANDLERS.get(method)
    if handler:
        return await handler(request_id, params)
    
    # Unknown method
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "tools_loaded": len(TOOLS),
        "mcp_version": MCP_VERSION,
        "server_info": SERVER_INFO,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/tools")
async def list_tools():
    """List available tools (non-MCP endpoint for debugging)."""
    return {
        "tools": list(TOOLS.keys()),
        "count": len(TOOLS)
    }

def start_mcp_server(port: int, env_vars: Dict[str, str]) -> subprocess.Popen:
    """Start the MCP server as a subprocess.
    
    Args:
        port: Port to run the server on
        env_vars: Environment variables to pass to the server
        
    Returns:
        subprocess.Popen instance for the server process
    """
    # Check if port is already in use
    if is_port_in_use(port):
        # Try to find an available port
        for alt_port in range(port + 1, port + 10):
            if not is_port_in_use(alt_port):
                port = alt_port
                print(f"⚠️  Port {port - 1} in use, using {port} instead")
                break
        else:
            raise RuntimeError(f"Could not find available port near {port}")
    
    # Merge env vars with current environment
    env = os.environ.copy()
    env.update(env_vars)
    
    # Get the path to the current Python interpreter
    python_path = sys.executable
    
    # Start uvicorn in subprocess - show output for logging
    cmd = [
        python_path, "-m", "uvicorn",
        "agtos.mcp_server:app",
        "--host", "127.0.0.1",
        "--port", str(port),
        "--log-level", "info",  # Show info level logs
    ]
    
    # Start process with output to console for monitoring
    process = subprocess.Popen(
        cmd, 
        env=env,
        # Let stdout/stderr flow to console
        stdout=None,
        stderr=None
    )
    
    # Give the server a moment to start
    import time
    time.sleep(1.5)
    
    # Check if process is still running
    if process.poll() is not None:
        raise RuntimeError("MCP server failed to start")
    
    return process

# For direct testing
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4405)