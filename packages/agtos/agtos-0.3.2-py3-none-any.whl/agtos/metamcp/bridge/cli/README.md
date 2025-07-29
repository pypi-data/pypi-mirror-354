# CLI Bridge Package

This package implements the CLI to MCP tool bridge, allowing any command-line tool to be exposed as MCP tools.

## Purpose

The CLI bridge automatically discovers and wraps command-line tools, parsing their help text to generate MCP tool specifications. It enables seamless integration of tools like git, docker, kubectl, and any other CLI tool into the agtos ecosystem.

## Module Breakdown

- **`core.py`** (~273 lines) - Main CLIBridge class and orchestration
  - `CLIBridge` class for managing CLI tool discovery
  - Tool caching and refresh logic
  - Integration with the service registry

- **`parser.py`** (~336 lines) - Help text parsing and schema generation
  - Parse CLI help text using regex patterns
  - Extract commands, arguments, and options
  - Generate JSON schemas from parsed data
  - Handle various help text formats

- **`discovery.py`** (~295 lines) - Tool discovery from knowledge store
  - Query knowledge store for CLI tools
  - Generate tool specifications
  - Create display names and aliases
  - Handle subcommands and complex CLIs

- **`execution.py`** (~262 lines) - Safe command execution
  - Build command lines from parameters
  - Execute in subprocess with timeout
  - Capture and format output
  - Handle errors and security

## Key Classes and Functions

### CLIBridge (core.py)
```python
bridge = CLIBridge()
tools = bridge.discover_cli_tools(["git", "docker"])
result = bridge.execute_tool("cli__git__status", {})
```

### Help Text Parsing (parser.py)
```python
parsed = parse_help_text(help_output)
schema = create_schema_from_parsed_help(parsed)
# Returns JSON schema for tool parameters
```

### Tool Discovery (discovery.py)
```python
tools = discover_tools_from_knowledge(knowledge_store, ["git"])
spec = create_tool_spec("git", "status", parsed_help)
aliases = generate_cli_aliases("git", "status")  # ["git status", "show changes"]
```

### Command Execution (execution.py)
```python
command = build_command("git", ["status"], {"verbose": True})
result = execute_command(command, timeout=30)
formatted = format_output(result, "git status")
```

## How Modules Work Together

1. **Discovery**: `discovery.py` queries knowledge store and uses `parser.py` to understand tools
2. **Parsing**: `parser.py` extracts structured data from help text
3. **Registration**: `core.py` creates tool specs and registers with service registry
4. **Execution**: `execution.py` safely runs commands when tools are called

The CLI bridge supports automatic discovery of new tools through the knowledge acquisition system. It provides secure command execution with proper escaping, timeout handling, and output formatting. The bridge can handle complex CLIs with subcommands, making virtually any command-line tool accessible through MCP.