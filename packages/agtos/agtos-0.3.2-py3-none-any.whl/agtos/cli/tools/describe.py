"""Tool description and example generation functionality.

AI_CONTEXT:
    This module provides detailed information about specific tools,
    including their parameters, schemas, and usage examples. It can
    generate example JSON based on tool schemas.
    
    Key features:
    - Tool lookup by name or alias
    - Schema visualization
    - Automatic example generation
    - Similar tool suggestions
"""

import asyncio
import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager
from ...errors import handle_error

console = Console()


def describe_tool(
    tool_name: str = typer.Argument(..., help="Tool name or alias"),
    show_schema: bool = typer.Option(
        False, "--schema", "-s",
        help="Show input schema"
    ),
    show_examples: bool = typer.Option(
        False, "--examples", "-e",
        help="Show usage examples"
    )
):
    """Show detailed information about a specific tool.
    
    AI_CONTEXT:
        Displays comprehensive information about a tool including its
        description, parameters, categories, and usage examples.
    """
    try:
        asyncio.run(_describe_tool_async(
            tool_name=tool_name,
            show_schema=show_schema,
            show_examples=show_examples
        ))
    except Exception as e:
        handle_error(e)


async def _describe_tool_async(
    tool_name: str,
    show_schema: bool,
    show_examples: bool
):
    """Async implementation of describe_tool command.
    
    AI_CONTEXT:
        Looks up a tool by name or alias and displays detailed information.
        If the tool is not found, it suggests similar tools based on
        name similarity.
    """
    # Create server instance
    server = MetaMCPServer(port=0)
    await server.initialize()
    
    registry = server.registry
    category_manager = CategoryManager()
    
    # Find the tool
    found_tool = None
    tool_service = None
    
    for service_name, service_info in registry.services.items():
        for tool in service_info.tools:
            # Check direct name match
            if tool.name == tool_name:
                found_tool = tool
                tool_service = service_name
                break
            
            # Check aliases
            if hasattr(tool, "aliases"):
                if tool_name.lower() in [a.lower() for a in tool.aliases]:
                    found_tool = tool
                    tool_service = service_name
                    break
        
        if found_tool:
            break
    
    if not found_tool:
        console.print(f"[red]Tool '{tool_name}' not found[/red]")
        
        # Suggest similar tools
        _suggest_similar_tools(tool_name, registry)
        return
    
    # Display tool information
    _display_tool_info(found_tool, tool_service, category_manager)
    
    # Show schema if requested
    if show_schema and hasattr(found_tool, "inputSchema"):
        console.print("\n[bold]Input Schema:[/bold]")
        schema_json = json.dumps(found_tool.inputSchema, indent=2)
        syntax = Syntax(schema_json, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
    
    # Show examples if requested
    if show_examples:
        console.print("\n[bold]Usage Examples:[/bold]")
        
        # Generate example based on schema
        if hasattr(found_tool, "inputSchema"):
            example = generate_tool_example(found_tool.name, found_tool.inputSchema)
            syntax = Syntax(example, "json", theme="monokai", line_numbers=False)
            console.print(syntax)
        else:
            console.print("[dim]No schema available to generate examples[/dim]")


def _display_tool_info(tool, service_name: str, category_manager: CategoryManager):
    """Display basic tool information in a panel.
    
    AI_CONTEXT:
        Creates a formatted panel with tool name, service, display name,
        aliases, categories, and description.
    """
    panel_content = []
    
    # Basic info
    panel_content.append(f"[bold]Name:[/bold] {tool.name}")
    panel_content.append(f"[bold]Service:[/bold] [yellow]{service_name}[/yellow]")
    
    # Display name
    if hasattr(tool, "displayName") and tool.displayName:
        panel_content.append(f"[bold]Display Name:[/bold] {tool.displayName}")
    
    # Aliases
    if hasattr(tool, "aliases") and tool.aliases:
        panel_content.append(f"[bold]Aliases:[/bold] [magenta]{', '.join(tool.aliases)}[/magenta]")
    
    # Categories
    categories = category_manager.categorize_tool(tool)
    cat_names = [cat.value for cat in categories]
    panel_content.append(f"[bold]Categories:[/bold] [green]{', '.join(cat_names)}[/green]")
    
    # Description
    if tool.description:
        panel_content.append(f"\n[bold]Description:[/bold]\n{tool.description}")
    
    console.print(Panel(
        "\n".join(panel_content),
        title=f"Tool: {tool.name}",
        border_style="cyan"
    ))


def _suggest_similar_tools(tool_name: str, registry):
    """Suggest similar tools when a tool is not found.
    
    AI_CONTEXT:
        Uses simple string matching to find tools with similar names.
        Checks if the query is a substring of tool names or vice versa.
    """
    all_tool_names = []
    for _, service_info in registry.services.items():
        for tool in service_info.tools:
            all_tool_names.append(tool.name)
    
    # Simple similarity check
    suggestions = [
        name for name in all_tool_names
        if tool_name.lower() in name.lower() or name.lower() in tool_name.lower()
    ]
    
    if suggestions:
        console.print("\n[yellow]Did you mean one of these?[/yellow]")
        for suggestion in suggestions[:5]:
            console.print(f"  • {suggestion}")


def generate_tool_example(tool_name: str, schema: dict) -> str:
    """Generate an example usage based on tool schema.
    
    AI_CONTEXT:
        Creates a realistic example JSON for tool usage by analyzing
        the schema and generating appropriate values based on property
        names and types. Includes special handling for common patterns
        like paths, URLs, and enums.
    """
    example = {
        "tool": tool_name,
        "arguments": {}
    }
    
    # Generate example values based on schema
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    for prop_name, prop_schema in properties.items():
        prop_type = prop_schema.get("type", "string")
        
        # Generate example value based on type
        if prop_type == "string":
            if "enum" in prop_schema:
                example["arguments"][prop_name] = prop_schema["enum"][0]
            elif prop_name.lower() in ["path", "file", "filename"]:
                example["arguments"][prop_name] = "/path/to/file"
            elif prop_name.lower() in ["url", "endpoint"]:
                example["arguments"][prop_name] = "https://example.com"
            else:
                example["arguments"][prop_name] = f"example_{prop_name}"
        
        elif prop_type == "number" or prop_type == "integer":
            example["arguments"][prop_name] = 42
        
        elif prop_type == "boolean":
            example["arguments"][prop_name] = True
        
        elif prop_type == "array":
            example["arguments"][prop_name] = ["item1", "item2"]
        
        elif prop_type == "object":
            example["arguments"][prop_name] = {"key": "value"}
    
    # Add comment about required fields
    if required:
        example["_required_fields"] = required
    
    return json.dumps(example, indent=2)