"""Tool category management functionality.

AI_CONTEXT:
    This module handles listing and displaying tool categories,
    including both default and custom categories. It can show
    category statistics and tool distribution.
    
    Features:
    - List all categories with icons and descriptions
    - Show category statistics (tool counts)
    - Display categorization summary
"""

import asyncio

import typer
from rich.console import Console
from rich.table import Table
from rich import box

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager, ToolCategory
from ...errors import handle_error

console = Console()


def list_categories(
    stats: bool = typer.Option(
        False, "--stats", "-s",
        help="Show category statistics"
    )
):
    """List all tool categories.
    
    AI_CONTEXT:
        Shows all available categories (both default and custom) with
        optional statistics about tool distribution.
    """
    try:
        asyncio.run(_list_categories_async(stats=stats))
    except Exception as e:
        handle_error(e)


async def _list_categories_async(stats: bool):
    """Async implementation of list_categories command.
    
    AI_CONTEXT:
        Retrieves category information and optionally calculates
        statistics about tool distribution across categories.
    """
    category_manager = CategoryManager()
    
    # Create server to get tools
    server = MetaMCPServer(port=0)
    await server.initialize()
    
    # Categorize all tools
    for service_name, service_info in server.registry.services.items():
        for tool in service_info.tools:
            category_manager.categorize_tool(tool)
    
    # Get category information
    all_categories = category_manager.get_all_categories()
    
    if stats:
        # Show detailed statistics
        _display_category_stats(category_manager)
    else:
        # Simple category listing
        _display_category_list(category_manager)


def _display_category_stats(category_manager: CategoryManager):
    """Display detailed category statistics.
    
    AI_CONTEXT:
        Shows a table with category names, icons, tool counts, and
        descriptions. Also displays a summary of categorization coverage.
    """
    stats_data = category_manager.get_category_stats()
    
    # Create stats table
    table = Table(
        title="Tool Category Statistics",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Category", style="green")
    table.add_column("Icon", justify="center")
    table.add_column("Tools", justify="right", style="yellow")
    table.add_column("Description", style="dim")
    
    # Sort categories by tool count
    sorted_cats = sorted(
        [(name, info) for name, info in stats_data.items() if name != "_summary"],
        key=lambda x: x[1]["tool_count"],
        reverse=True
    )
    
    for cat_name, info in sorted_cats:
        table.add_row(
            cat_name,
            info["icon"],
            str(info["tool_count"]),
            info["description"]
        )
    
    console.print(table)
    
    # Show summary
    summary = stats_data["_summary"]
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"  Total Tools: [yellow]{summary['total_tools']}[/yellow]")
    console.print(f"  Categorized: [green]{summary['categorized_tools']}[/green]")
    console.print(f"  Uncategorized: [red]{summary['uncategorized_tools']}[/red]")
    console.print(f"  Categories: {summary['total_categories']} ({summary['default_categories']} default, {summary['custom_categories']} custom)")


def _display_category_list(category_manager: CategoryManager):
    """Display simple category listing.
    
    AI_CONTEXT:
        Shows all categories grouped by type (default vs custom) with
        their icons and descriptions.
    """
    console.print("[bold cyan]Tool Categories:[/bold cyan]\n")
    
    # Default categories
    console.print("[bold]Default Categories:[/bold]")
    for category in ToolCategory:
        info = category_manager.categories.get(category)
        if info:
            console.print(f"  {info.icon} [green]{category.value}[/green] - {info.description}")
    
    # Custom categories
    if category_manager.custom_categories:
        console.print("\n[bold]Custom Categories:[/bold]")
        for key, info in category_manager.custom_categories.items():
            name = key.replace("custom_", "").replace("_", " ").title()
            console.print(f"  {info.icon} [green]{name}[/green] - {info.description}")