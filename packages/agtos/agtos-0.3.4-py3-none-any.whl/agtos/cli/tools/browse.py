"""Interactive tool browser functionality.

AI_CONTEXT:
    This module provides an interactive menu-based interface for
    browsing tools by category. Users can navigate through categories,
    view tool lists, and see detailed information about specific tools.
    
    Navigation flow:
    1. Category selection menu
    2. Tool list for selected category
    3. Tool details with schema and examples
"""

import asyncio

import typer
from rich.console import Console
from rich.prompt import Prompt

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager, ToolCategory
from ...metamcp.registry import ServiceRegistry
from ...errors import handle_error
from .search import _search_tools_async
from .describe import _describe_tool_async

console = Console()


def browse_tools():
    """Interactive tool browser.
    
    AI_CONTEXT:
        Launches an interactive menu system for browsing and exploring
        tools by category, with the ability to view details and examples.
    """
    try:
        asyncio.run(_browse_tools_async())
    except Exception as e:
        handle_error(e)


async def _browse_tools_async():
    """Interactive tool browser implementation.
    
    AI_CONTEXT:
        Main loop for the interactive browser. Shows category menu,
        handles user input, and delegates to appropriate functions
        for browsing categories or searching.
    """
    console.print("[bold cyan]Interactive Tool Browser[/bold cyan]")
    console.print("[dim]Loading tools...[/dim]\n")
    
    # Create server and category manager
    server = MetaMCPServer(port=0)
    await server.initialize()
    category_manager = CategoryManager()
    
    # Categorize all tools
    for service_name, service_info in server.registry.services.items():
        for tool in service_info.tools:
            category_manager.categorize_tool(tool)
    
    while True:
        # Show category menu
        console.print("\n[bold]Select a category:[/bold]")
        
        categories = list(ToolCategory)
        for i, category in enumerate(categories, 1):
            info = category_manager.categories[category]
            tool_count = info.tool_count()
            console.print(f"  {i}. {info.icon} {category.value} ({tool_count} tools)")
        
        console.print(f"  {len(categories) + 1}. 🔍 Search all tools")
        console.print(f"  {len(categories) + 2}. ❌ Exit")
        
        choice = Prompt.ask("\nEnter your choice", default="1")
        
        try:
            choice_num = int(choice)
            
            if choice_num == len(categories) + 2:
                # Exit
                console.print("[yellow]Exiting tool browser[/yellow]")
                break
            
            elif choice_num == len(categories) + 1:
                # Search
                query = Prompt.ask("Enter search query")
                await _search_tools_async(query, None, 20)
                
                if Prompt.ask("\nPress Enter to continue"):
                    pass
            
            elif 1 <= choice_num <= len(categories):
                # Browse category
                selected_category = categories[choice_num - 1]
                await _browse_category_tools(
                    server.registry,
                    category_manager,
                    selected_category
                )
            
            else:
                console.print("[red]Invalid choice[/red]")
        
        except ValueError:
            console.print("[red]Please enter a number[/red]")


async def _browse_category_tools(
    registry: ServiceRegistry,
    category_manager: CategoryManager,
    category: ToolCategory
):
    """Browse tools in a specific category.
    
    AI_CONTEXT:
        Shows a list of tools in the selected category and allows
        the user to view detailed information about each tool.
        Provides navigation back to the category menu.
    """
    # Get tools in category
    tool_names = category_manager.get_tools_by_category(category)
    
    if not tool_names:
        console.print(f"\n[yellow]No tools in category: {category.value}[/yellow]")
        return
    
    # Collect tool details
    tools = []
    for service_name, service_info in registry.services.items():
        for tool in service_info.tools:
            if tool.name in tool_names:
                tool_dict = tool.to_dict() if hasattr(tool, "to_dict") else dict(tool)
                tool_dict["service"] = service_name
                tool_dict["_tool_obj"] = tool
                tools.append(tool_dict)
    
    # Sort by name
    tools.sort(key=lambda t: t["name"])
    
    while True:
        console.print(f"\n[bold]{category.value} Tools:[/bold]")
        
        for i, tool in enumerate(tools, 1):
            console.print(f"  {i}. [bright_blue]{tool['name']}[/bright_blue] - {tool['service']}")
        
        console.print(f"  {len(tools) + 1}. ⬅️  Back to categories")
        
        choice = Prompt.ask("\nSelect a tool for details", default="1")
        
        try:
            choice_num = int(choice)
            
            if choice_num == len(tools) + 1:
                # Back
                break
            
            elif 1 <= choice_num <= len(tools):
                # Show tool details
                selected_tool = tools[choice_num - 1]
                await _describe_tool_async(
                    selected_tool["name"],
                    show_schema=True,
                    show_examples=True
                )
                
                if Prompt.ask("\nPress Enter to continue"):
                    pass
            
            else:
                console.print("[red]Invalid choice[/red]")
        
        except ValueError:
            console.print("[red]Please enter a number[/red]")