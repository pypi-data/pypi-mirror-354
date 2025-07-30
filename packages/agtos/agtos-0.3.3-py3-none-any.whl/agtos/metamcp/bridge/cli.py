"""CLI Bridge for Meta-MCP Server - Backward compatibility wrapper.

This module maintains backward compatibility by re-exporting the CLIBridge
class from the new modular structure.

AI_CONTEXT:
    This file exists solely for backward compatibility. All functionality
    has been moved to the cli/ subpackage following AI-First principles:
    - cli/core.py: Main CLIBridge class
    - cli/parser.py: Help text parsing
    - cli/discovery.py: Tool discovery
    - cli/execution.py: Command execution
    
    New code should import directly from agtos.metamcp.bridge.cli.core
"""

# Re-export for backward compatibility
from .cli.core import CLIBridge

__all__ = ['CLIBridge']