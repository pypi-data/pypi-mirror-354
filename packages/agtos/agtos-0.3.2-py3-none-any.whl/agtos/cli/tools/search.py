"""Tool search functionality for the CLI.

AI_CONTEXT:
    This module provides fuzzy search capabilities for finding tools
    by name, alias, or description. It scores results based on match
    quality and displays them in a ranked order.
    
    Search scoring:
    - Name match: 10 points
    - Alias match: 8 points
    - Display name match: 7 points
    - Description match: 5 points
"""

import asyncio
from typing import List

import typer
from rich.console import Console
from rich.text import Text

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager
from ...errors import handle_error

console = Console()


def search_tools(
    query: str = typer.Argument(..., help="Search query"),
    category: str = typer.Option(
        None, "--category", "-c",
        help="Filter by category"
    ),
    limit: int = typer.Option(
        20, "--limit", "-l",
        help="Maximum number of results"
    )
):
    """Search for tools by name or description.
    
    AI_CONTEXT:
        Performs fuzzy matching on tool names and descriptions to find
        relevant tools. Results are ranked by relevance.
    """
    try:
        asyncio.run(_search_tools_async(
            query=query,
            category=category,
            limit=limit
        ))
    except Exception as e:
        handle_error(e)


async def _search_tools_async(
    query: str,
    category: str,
    limit: int
):
    """Async implementation of search_tools command.
    
    AI_CONTEXT:
        This function performs the actual search by scoring each tool
        based on how well it matches the query. Tools are scored on
        multiple attributes and results are sorted by score.
    """
    # Create server instance
    server = MetaMCPServer(port=0)
    await server.initialize()
    
    registry = server.registry
    category_manager = CategoryManager()
    
    # Get all tools
    all_tools = []
    for service_name, service_info in registry.services.items():
        for tool in service_info.tools:
            tool_dict = tool.to_dict() if hasattr(tool, "to_dict") else dict(tool)
            tool_dict["service"] = service_name
            
            # Categorize
            categories = category_manager.categorize_tool(tool)
            tool_dict["categories"] = [cat.value for cat in categories]
            
            all_tools.append(tool_dict)
    
    # Search and score tools
    query_lower = query.lower()
    scored_tools = []
    
    for tool in all_tools:
        score = 0
        
        # Check tool name (highest weight)
        if query_lower in tool["name"].lower():
            score += 10
        
        # Check aliases
        for alias in tool.get("aliases", []):
            if query_lower in alias.lower():
                score += 8
                break
        
        # Check description
        if query_lower in tool.get("description", "").lower():
            score += 5
        
        # Check display name
        if query_lower in tool.get("displayName", "").lower():
            score += 7
        
        if score > 0:
            # Apply category filter if specified
            if category:
                if category not in tool.get("categories", []):
                    continue
            
            scored_tools.append((score, tool))
    
    # Sort by score and limit results
    scored_tools.sort(key=lambda x: x[0], reverse=True)
    results = [tool for _, tool in scored_tools[:limit]]
    
    if not results:
        console.print(f"[yellow]No tools found matching '{query}'[/yellow]")
        return
    
    # Display results
    _display_search_results(query, results)


def _display_search_results(query: str, results: list):
    """Display search results in a formatted way.
    
    AI_CONTEXT:
        Shows each matching tool with its service, categories, aliases,
        and description. Results are numbered for easy reference.
    """
    console.print(f"\n[bold]Search Results for '{query}':[/bold]\n")
    
    for i, tool in enumerate(results, 1):
        console.print(f"[bright_blue]{i}. {tool['name']}[/bright_blue]")
        console.print(f"   Service: [yellow]{tool['service']}[/yellow]")
        console.print(f"   Categories: [green]{', '.join(tool['categories'])}[/green]")
        
        if tool.get("aliases"):
            console.print(f"   Aliases: [magenta]{', '.join(tool['aliases'])}[/magenta]")
        
        if tool.get("description"):
            desc = Text(tool["description"], style="dim")
            desc.truncate(100)
            console.print(f"   Description: {desc}")
        
        console.print()