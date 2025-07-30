# CLI Tools Package

This package contains the CLI commands for interacting with tools in the agtos system.

## Purpose

The tools CLI provides commands for discovering, searching, browsing, and exporting tools available through the Meta-MCP server. It serves as the primary interface for users to explore and understand available capabilities.

## Module Breakdown

- **`list.py`** (~233 lines) - Tool listing functionality
  - List all tools or filter by service/category
  - Multiple output formats (table, json, yaml)
  - Sorting and filtering options

- **`search.py`** (~120 lines) - Tool search capabilities
  - Full-text search across tool names and descriptions
  - Fuzzy matching support
  - Category and tag filtering

- **`describe.py`** (~172 lines) - Detailed tool information
  - Show tool schemas and parameters
  - Generate usage examples
  - Display authentication requirements

- **`categories.py`** (~117 lines) - Category management
  - List available categories
  - Show category statistics
  - Manage custom categories

- **`browse.py`** (~196 lines) - Interactive browser
  - Terminal UI for exploring tools
  - Real-time filtering and search
  - Category-based navigation

- **`export.py`** (~185 lines) - Export functionality
  - Export tool catalogs
  - Generate documentation
  - Create shareable tool definitions

## Key Commands

### List Tools
```bash
agtos tools list                    # List all tools
agtos tools list --service cli      # List CLI tools only
agtos tools list --format json      # Output as JSON
```

### Search Tools
```bash
agtos tools search "git"            # Search for git-related tools
agtos tools search "api" --category rest  # Search within category
```

### Describe Tool
```bash
agtos tools describe cli__git__status      # Show detailed info
agtos tools describe rest__github__create_issue --examples  # With examples
```

### Browse Interactively
```bash
agtos tools browse                  # Launch interactive browser
agtos tools browse --category dev   # Start in specific category
```

## How Modules Work Together

1. **Discovery**: All modules use the service registry to discover available tools
2. **Filtering**: Search and category modules provide filtering used by list and browse
3. **Display**: List and describe share formatting utilities for consistent output
4. **Export**: Export module leverages list and describe functionality for comprehensive exports

The tools CLI integrates with the Meta-MCP server's registry to provide real-time information about available tools across all connected services.