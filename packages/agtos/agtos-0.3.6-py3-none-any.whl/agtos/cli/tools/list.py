"""Tool listing functionality for the CLI.

AI_CONTEXT:
    This module handles listing and displaying tools in various formats.
    It supports filtering by category, tag, service, and can display
    results as tables, trees, or JSON.
    
    Key functions:
    - list_tools: Main CLI command for listing tools
    - _list_tools_async: Async implementation that does the work
    - _display_tools_as_table: Rich table format display
    - _display_tools_as_tree: Tree format grouped by category
"""

import asyncio
import json
from typing import List

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.text import Text
from rich import box

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager, ToolCategory
from ...errors import handle_error

console = Console()


def list_tools(
    category: str = typer.Option(
        None, 
        "--category", 
        "-c",
        help="Filter by category (e.g., 'Git Operations', 'API Integrations')"
    ),
    tag: str = typer.Option(
        None, 
        "--tag", 
        "-t",
        help="Filter by tag"
    ),
    service: str = typer.Option(
        None, 
        "--service", 
        "-s",
        help="Filter by service name"
    ),
    output_format: str = typer.Option(
        "table", 
        "--format", 
        "-f",
        help="Output format: table, json, tree"
    ),
    show_aliases: bool = typer.Option(
        False, 
        "--aliases", 
        "-a",
        help="Show tool aliases"
    )
):
    """List all available tools with optional filtering.
    
    AI_CONTEXT:
        This command discovers all tools from registered services and
        displays them in various formats. It supports filtering by
        category, tag, or service.
    """
    try:
        # Run async function
        asyncio.run(_list_tools_async(
            category=category,
            tag=tag,
            service=service,
            format=output_format,
            show_aliases=show_aliases
        ))
    except Exception as e:
        handle_error(e)


async def _list_tools_async(
    category: str,
    tag: str,
    service: str,
    format: str,
    show_aliases: bool
):
    """Async implementation of list_tools command.
    
    AI_CONTEXT:
        This function does the actual work of discovering and listing tools.
        It creates a temporary Meta-MCP server instance to access the registry
        and category manager.
    """
    # Create server instance to get registry
    server = MetaMCPServer(port=0)  # Port 0 since we're not starting the server
    await server.initialize()
    
    registry = server.registry
    category_manager = CategoryManager()
    
    # Discover all tools from services
    all_tools = []
    for service_name, service_info in registry.services.items():
        # Filter by service if specified
        if service and service_name != service:
            continue
        
        for tool in service_info.tools:
            tool_dict = tool.to_dict() if hasattr(tool, "to_dict") else dict(tool)
            tool_dict["service"] = service_name
            
            # Categorize the tool
            categories = category_manager.categorize_tool(tool)
            tool_dict["categories"] = [cat.value for cat in categories]
            
            all_tools.append(tool_dict)
    
    # Filter by category if specified
    if category:
        # Try to match category enum
        cat_enum = ToolCategory.from_string(category)
        if cat_enum:
            all_tools = [
                tool for tool in all_tools
                if cat_enum.value in tool.get("categories", [])
            ]
        else:
            # Try custom category
            all_tools = [
                tool for tool in all_tools
                if category in tool.get("categories", [])
            ]
    
    # Filter by tag if specified
    if tag:
        # For now, we'll check if tag is in the tool name or description
        tag_lower = tag.lower()
        all_tools = [
            tool for tool in all_tools
            if tag_lower in tool["name"].lower() or tag_lower in tool.get("description", "").lower()
        ]
    
    # Display results based on format
    if format == "json":
        console.print_json(json.dumps(all_tools, indent=2))
    
    elif format == "tree":
        _display_tools_as_tree(all_tools, show_aliases)
    
    else:  # table format
        _display_tools_as_table(all_tools, show_aliases)
    
    # Show summary
    console.print(f"\n[dim]Total tools: {len(all_tools)}[/dim]")


def _display_tools_as_table(tools: List[dict], show_aliases: bool):
    """Display tools in a rich table format.
    
    AI_CONTEXT:
        Creates a formatted table with tool information including
        name, service, categories, and description. Optionally shows
        aliases if requested.
    """
    table = Table(
        title="Available Tools",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Tool Name", style="bright_blue", no_wrap=True)
    table.add_column("Service", style="yellow")
    table.add_column("Categories", style="green")
    table.add_column("Description", style="dim", overflow="fold")
    
    if show_aliases:
        table.add_column("Aliases", style="magenta")
    
    for tool in tools:
        categories = ", ".join(tool.get("categories", ["Uncategorized"]))
        
        row = [
            tool["name"],
            tool["service"],
            categories,
            tool.get("description", "")
        ]
        
        if show_aliases:
            aliases = ", ".join(tool.get("aliases", []))
            row.append(aliases)
        
        table.add_row(*row)
    
    console.print(table)


def _display_tools_as_tree(tools: List[dict], show_aliases: bool):
    """Display tools in a tree format grouped by category.
    
    AI_CONTEXT:
        Creates a hierarchical tree view of tools organized by their
        categories. Each category shows its tool count and each tool
        shows its service and description.
    """
    tree = Tree("[bold cyan]Tool Categories[/bold cyan]")
    
    # Group tools by category
    category_tools = {}
    for tool in tools:
        for category in tool.get("categories", ["Uncategorized"]):
            if category not in category_tools:
                category_tools[category] = []
            category_tools[category].append(tool)
    
    # Build tree
    for category, cat_tools in sorted(category_tools.items()):
        cat_branch = tree.add(f"[bold green]{category}[/bold green] ({len(cat_tools)} tools)")
        
        for tool in sorted(cat_tools, key=lambda t: t["name"]):
            tool_text = f"[bright_blue]{tool['name']}[/bright_blue]"
            if tool["service"]:
                tool_text += f" [dim]({tool['service']})[/dim]"
            
            tool_branch = cat_branch.add(tool_text)
            
            # Add description as a sub-item
            if tool.get("description"):
                desc_text = Text(tool["description"], style="dim")
                desc_text.truncate(80)
                tool_branch.add(desc_text)
            
            # Add aliases if requested
            if show_aliases and tool.get("aliases"):
                aliases_text = f"[magenta]Aliases: {', '.join(tool['aliases'])}[/magenta]"
                tool_branch.add(aliases_text)
    
    console.print(tree)