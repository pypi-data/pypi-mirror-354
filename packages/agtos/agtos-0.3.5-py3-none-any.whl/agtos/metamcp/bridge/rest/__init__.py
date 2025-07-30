"""REST Bridge refactored modules.

AI_CONTEXT: This package contains the refactored REST bridge functionality,
split into focused modules following AI-First principles:

- core.py: Main RESTBridge class and tool generation
- auth.py: Authentication handling (Bearer, API Key, Basic)
- openapi.py: OpenAPI spec parsing and schema building
- execution.py: Request execution and response handling

Each module is kept under 500 lines with clear AI_CONTEXT docstrings
for complex functionality.
"""

# Re-export main functionality for backward compatibility
from .core import RESTBridge, generate_all_rest_tools, get_tools, TOOLS
from .auth import get_credential
from .execution import RateLimiter

__all__ = [
    "RESTBridge",
    "generate_all_rest_tools", 
    "get_tools",
    "TOOLS",
    "get_credential",
    "RateLimiter"
]