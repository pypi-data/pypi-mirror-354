"""Tool creation plugin for Meta-MCP.

This plugin allows orchestrator agents (like Claude) to create new tools
on-demand based on natural language descriptions from users.

AI_CONTEXT:
    This is the RIGHT way to implement tool creation - as a tool that
    agents can call, not as a CLI command. When a user asks Claude to
    do something that requires a tool that doesn't exist, Claude can
    use this tool to create it dynamically.
    
    NEW: Integrates with hot-reload functionality to make tools
    immediately available without server restart.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

from ..user_tools import APIAnalyzer, ToolGenerator, ToolValidator
from ..errors import AgentCtlError


def _trigger_hot_reload(tool_name: str) -> str:
    """Trigger hot-reload for a newly created tool.
    
    AI_CONTEXT:
        This function attempts to notify the Meta-MCP server to reload
        the newly created tool. It uses a simple HTTP request to a
        reload endpoint if the server is running.
    
    Args:
        tool_name: Name of the tool to reload
        
    Returns:
        Status message about the reload attempt
    """
    try:
        # Check if Meta-MCP server is running by attempting connection
        import requests
        
        # Try localhost ports where Meta-MCP might be running
        for port in [8585, 3000, 8000]:
            try:
                # Attempt to trigger reload via HTTP endpoint
                response = requests.post(
                    f"http://localhost:{port}/internal/reload-tool",
                    json={"tool_name": tool_name},
                    timeout=1
                )
                
                if response.status_code == 200:
                    return f"Tool hot-reloaded successfully (port {port})"
                    
            except requests.exceptions.RequestException:
                continue
        
        # If no server found, check if we can reload via file marker
        reload_marker = Path.home() / ".agtos" / "user_tools" / ".reload_marker"
        reload_marker.parent.mkdir(parents=True, exist_ok=True)
        
        # Write tool name to reload marker
        import time
        reload_marker.write_text(f"{tool_name}\n{time.time()}")
        
        return "Tool saved. Will be loaded on next server start or when file watcher detects change."
        
    except Exception as e:
        return f"Tool saved but hot-reload failed: {str(e)}"


def create_tool_from_description(
    description: str,
    name: Optional[str] = None,
    save: bool = True
) -> Dict[str, Any]:
    """Create a new tool from natural language description.
    
    This is meant to be called by orchestrator agents when they need
    to create a new tool based on user requirements.
    
    Args:
        description: Natural language description of the API/tool
        name: Optional tool name (will be inferred if not provided)
        save: Whether to save the tool to disk
        
    Returns:
        Dict with tool info and generated code
    """
    try:
        # Analyze and generate the tool
        spec, tool = _analyze_and_generate_tool(description, name)
        
        # Validate the generated tool
        errors = _validate_generated_tool(tool)
        
        # Save if requested
        saved_path = None
        hot_reload_status = "Not attempted"
        if save:
            saved_path, hot_reload_status = _save_tool_to_disk(spec, tool)
        
        # Build and return the response
        return _build_tool_creation_response(
            spec, tool, errors, saved_path, hot_reload_status
        )
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Please provide more details about the API, including the URL, HTTP method, and any required parameters."
        }


def _analyze_and_generate_tool(description: str, name: Optional[str] = None):
    """Analyze the description and generate the tool.
    
    Args:
        description: Natural language API description
        name: Optional tool name
        
    Returns:
        Tuple of (spec, tool)
    """
    # Analyze the description
    analyzer = APIAnalyzer()
    spec = analyzer.analyze(description, name)
    
    # Generate the tool
    generator = ToolGenerator()
    tool = generator.generate(spec)
    
    return spec, tool


def _validate_generated_tool(tool) -> list:
    """Validate the generated tool and check for critical errors.
    
    Args:
        tool: Generated tool to validate
        
    Returns:
        List of validation errors
        
    Raises:
        AgentCtlError: If critical validation errors found
    """
    validator = ToolValidator()
    is_valid, errors = validator.validate(tool)
    
    # Check for critical errors
    syntax_errors = [e for e in errors if "Syntax" in e]
    security_errors = [e for e in errors if "Dangerous" in e or "security" in e.lower()]
    
    if syntax_errors or security_errors:
        raise AgentCtlError(
            f"Tool validation failed: {'; '.join(syntax_errors + security_errors)}",
            suggestion="Check the API description for syntax issues or security concerns"
        )
    
    return errors


def _save_tool_to_disk(spec, tool) -> tuple[str, str]:
    """Save the tool to disk and trigger hot reload.
    
    Args:
        spec: Tool specification
        tool: Generated tool
        
    Returns:
        Tuple of (saved_path, hot_reload_status)
    """
    user_tools_dir = Path.home() / ".agtos" / "user_tools"
    user_tools_dir.mkdir(parents=True, exist_ok=True)
    
    # Save tool code
    tool_file = user_tools_dir / f"{spec.name}.py"
    tool_file.write_text(tool.tool_code)
    
    # Save metadata
    metadata_file = user_tools_dir / f"{spec.name}.json"
    metadata_file.write_text(json.dumps(tool.to_dict(), indent=2))
    
    saved_path = str(tool_file)
    
    # Trigger hot-reload
    hot_reload_status = _trigger_hot_reload(spec.name)
    
    return saved_path, hot_reload_status


def _build_tool_creation_response(
    spec, tool, errors: list, saved_path: Optional[str], hot_reload_status: str
) -> Dict[str, Any]:
    """Build the response dictionary for tool creation.
    
    Args:
        spec: Tool specification
        tool: Generated tool
        errors: Validation errors
        saved_path: Path where tool was saved
        hot_reload_status: Status of hot reload attempt
        
    Returns:
        Response dictionary with tool information
    """
    # Extract only non-critical warnings
    syntax_errors = [e for e in errors if "Syntax" in e]
    security_errors = [e for e in errors if "Dangerous" in e or "security" in e.lower()]
    validation_warnings = [e for e in errors if e not in syntax_errors + security_errors]
    
    return {
        "success": True,
        "tool_name": spec.name,
        "description": spec.description,
        "endpoints": _format_endpoints(spec.endpoints),
        "code_preview": tool.tool_code[:500] + "...",
        "validation_warnings": validation_warnings,
        "saved_to": saved_path,
        "mcp_schema": tool.mcp_schema,
        "hot_reload": hot_reload_status,
        "usage": f"The tool '{spec.name}' is now available. You can call it with the appropriate parameters."
    }


def _format_endpoints(endpoints) -> list:
    """Format endpoint information for the response.
    
    Args:
        endpoints: List of endpoint specifications
        
    Returns:
        List of formatted endpoint dictionaries
    """
    return [
        {
            "url": ep.url,
            "method": ep.method.value,
            "parameters": [p.name for p in ep.parameters],
            "auth": ep.authentication.type.value if ep.authentication else None
        }
        for ep in endpoints
    ]


def analyze_api_description(description: str) -> Dict[str, Any]:
    """Analyze a natural language API description without creating the tool.
    
    Useful for agents to understand what would be created before committing.
    
    Args:
        description: Natural language description of the API
        
    Returns:
        Analysis results
    """
    try:
        analyzer = APIAnalyzer()
        spec = analyzer.analyze(description)
        
        return {
            "success": True,
            "analysis": {
                "tool_name": spec.name,
                "description": spec.description,
                "endpoints": [
                    {
                        "url": ep.url,
                        "method": ep.method.value,
                        "parameters": [
                            {
                                "name": p.name,
                                "type": p.type,
                                "required": p.required,
                                "location": p.location.value
                            }
                            for p in ep.parameters
                        ],
                        "authentication": {
                            "type": ep.authentication.type.value,
                            "location": ep.authentication.location
                        } if ep.authentication else None
                    }
                    for ep in spec.endpoints
                ]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_user_tools() -> Dict[str, Any]:
    """List all user-created tools.
    
    Returns:
        Dict with list of user tools and their metadata
    """
    user_tools_dir = Path.home() / ".agtos" / "user_tools"
    
    if not user_tools_dir.exists():
        return {
            "success": True,
            "tools": [],
            "message": "No user-created tools found"
        }
    
    tools = []
    for json_file in user_tools_dir.glob("*.json"):
        try:
            metadata = json.loads(json_file.read_text())
            tools.append({
                "name": metadata["name"],
                "description": metadata["description"],
                "created_at": metadata.get("created_at"),
                "endpoints": len(metadata.get("specification", {}).get("endpoints", [])),
                "file": str(json_file.with_suffix(".py"))
            })
        except:
            continue
    
    return {
        "success": True,
        "tools": tools,
        "total": len(tools)
    }


# Plugin registration in agtos format
TOOLS = {
    "tool_creator.create": {
        "version": "1.0",
        "description": "Create a new tool from natural language API description. Use this when a user needs to integrate with an API that doesn't have an existing tool.",
        "schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Natural language description of the API (e.g., 'post messages to api.slack.com/messages with text and channel')"
                },
                "name": {
                    "type": "string",
                    "description": "Optional tool name (will be inferred from API if not provided)"
                },
                "save": {
                    "type": "boolean",
                    "description": "Whether to save the tool to disk (default: true)",
                    "default": True
                }
            },
            "required": ["description"]
        },
        "func": create_tool_from_description
    },
    "tool_creator.analyze": {
        "version": "1.0",
        "description": "Analyze an API description to preview what tool would be created without actually creating it.",
        "schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Natural language description of the API to analyze"
                }
            },
            "required": ["description"]
        },
        "func": analyze_api_description
    },
    "tool_creator.list": {
        "version": "1.0",
        "description": "List all user-created tools that have been saved.",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": list_user_tools
    }
}