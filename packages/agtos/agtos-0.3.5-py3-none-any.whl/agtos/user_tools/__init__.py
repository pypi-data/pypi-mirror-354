"""Natural language tool creation for agtOS.

This module enables users to create new tools by describing APIs in natural language.
No coding required - just describe what you need and the system generates the tool.

AI_CONTEXT:
    This is a CORE feature of agtOS. Users should never have to:
    - Read API documentation
    - Write code manually
    - Understand technical details
    
    The module handles:
    - Natural language parsing
    - API analysis and inference
    - Tool code generation
    - Validation and testing
    - Registration with Meta-MCP
    
    Architecture:
    1. User describes API in plain English
    2. Analyzer extracts endpoints and parameters
    3. Generator creates tool implementation
    4. Validator ensures it works
    5. Tool immediately available to all agents
"""

from .generator import ToolGenerator
from .analyzer import APIAnalyzer
from .validator import ToolValidator
from .models import (
    ToolSpecification,
    APIEndpoint,
    AuthenticationMethod,
    GeneratedTool
)

__all__ = [
    "ToolGenerator",
    "APIAnalyzer", 
    "ToolValidator",
    "ToolSpecification",
    "APIEndpoint",
    "AuthenticationMethod",
    "GeneratedTool"
]