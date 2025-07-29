"""REST API Bridge for MCP - Backward compatibility wrapper.

This module has been refactored into the rest/ subpackage following
AI-First principles. All functionality is preserved through imports.

AI_CONTEXT: This file exists for backward compatibility. The REST bridge
has been split into focused modules:
- rest/core.py: Main RESTBridge class
- rest/auth.py: Authentication handling
- rest/openapi.py: OpenAPI parsing and schema generation  
- rest/execution.py: Request execution and rate limiting

All exports are maintained for existing code.
"""

# Import everything for backward compatibility
from .rest.core import (
    RESTBridge,
    generate_all_rest_tools,
    get_tools,
    TOOLS
)

# Also expose internals that might be used
from .rest.auth import get_credential
from .rest.execution import RateLimiter

__all__ = [
    "RESTBridge",
    "generate_all_rest_tools",
    "get_tools",
    "TOOLS",
    "get_credential",
    "RateLimiter"
]