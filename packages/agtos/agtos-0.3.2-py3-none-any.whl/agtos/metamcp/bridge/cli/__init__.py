"""CLI Bridge subpackage for Meta-MCP Server.

This package contains the modular components of the CLI Bridge:
- core.py: Main CLIBridge class and integration logic
- parser.py: Help text parsing and JSON schema generation
- discovery.py: CLI tool discovery from knowledge store
- execution.py: Command building and subprocess execution

AI_CONTEXT:
    The CLI Bridge is split into focused modules following AI-First principles.
    Each module handles a specific aspect of CLI-to-MCP conversion, making it
    easier to understand, test, and maintain individual components.
"""

# Re-export main CLIBridge class for backward compatibility
from .core import CLIBridge

__all__ = ['CLIBridge']