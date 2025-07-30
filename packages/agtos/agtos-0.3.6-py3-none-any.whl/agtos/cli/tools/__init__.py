"""Tool management and discovery CLI commands.

AI_CONTEXT:
    This module provides CLI commands for discovering, listing, and managing
    tools available through the Meta-MCP server. It includes:
    - Tool listing with category and tag filtering
    - Tool search functionality
    - Category management
    - Interactive tool browser
    - Tool description and usage information
    - Tool catalog export
    
MODULE_STRUCTURE:
    This package is organized into focused modules:
    - list.py: Tool listing and display functionality
    - search.py: Tool search with fuzzy matching
    - describe.py: Tool description and example generation
    - categories.py: Category listing and management
    - browse.py: Interactive tool browser
    - export.py: Tool catalog export functionality
"""

import typer

from .list import list_tools
from .search import search_tools
from .describe import describe_tool
from .categories import list_categories
from .browse import browse_tools
from .export import export_tools


def register_tools_commands(app: typer.Typer):
    """Register tool management commands with the main app.
    
    AI_CONTEXT:
        This function is called from cli/__init__.py to register all
        tool-related commands. It creates a command group for better
        organization. Each command is implemented in its own module
        for better maintainability.
    """
    tools_app = typer.Typer(
        name="tools",
        help="Discover and manage available tools"
    )
    
    app.add_typer(tools_app, name="tools")
    
    # Register commands from submodules
    tools_app.command("list")(list_tools)
    tools_app.command("search")(search_tools)
    tools_app.command("describe")(describe_tool)
    tools_app.command("categories")(list_categories)
    tools_app.command("browse")(browse_tools)
    tools_app.command("export")(export_tools)