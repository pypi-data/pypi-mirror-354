"""Help text parser and JSON schema generator for CLI Bridge.

This module handles parsing CLI help text and generating JSON schemas
for MCP tool specifications.

AI_CONTEXT:
    The HelpTextParser extracts structured information from unstructured
    CLI help text using regex patterns and heuristics. It generates
    JSON schemas that accurately represent CLI interfaces, handling:
    - Flags (short -f and long --flag)
    - Positional arguments
    - Optional vs required parameters
    - Value types and constraints
    - Subcommands and their specific options
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class HelpTextParser:
    """Parser for CLI help text and schema generator.
    
    AI_CONTEXT:
        This class uses pattern matching to extract structured data from
        help text. It handles common help text formats from popular CLIs
        like git, docker, npm, etc. The generated schemas follow JSON
        Schema draft-07 for MCP compatibility.
    """
    
    def __init__(self):
        """Initialize parser with common patterns."""
        # Pattern for flags with descriptions
        self.flag_pattern = re.compile(
            r'^\s*(-\w|--[\w-]+)(?:,?\s*(-\w|--[\w-]+))?\s*(?:<([\w_]+)>|=([\w_]+))?\s+(.+)$',
            re.MULTILINE
        )
        
        # Pattern for positional arguments
        self.arg_pattern = re.compile(
            r'^\s*<([\w_]+)>\s+(.+)$',
            re.MULTILINE
        )
        
        # Pattern for optional arguments
        self.optional_arg_pattern = re.compile(
            r'^\s*\[([\w_]+)\]\s+(.+)$',
            re.MULTILINE
        )
    
    def parse_help_text(self, help_text: str) -> Dict[str, Any]:
        """Parse help text to extract arguments and flags.
        
        Args:
            help_text: Raw help text from CLI
            
        Returns:
            Dictionary with parsed arguments and flags
            
        AI_CONTEXT:
            This method is the main entry point for parsing. It extracts:
            - Flags with their short/long forms and descriptions
            - Positional and optional arguments
            - Whether flags take values
            - Default values when mentioned
        """
        parsed = {
            "flags": [],
            "arguments": [],
            "optional_arguments": [],
            "global_flags": []
        }
        
        # Extract flags
        for match in self.flag_pattern.finditer(help_text):
            flag_info = self._parse_flag_match(match)
            if flag_info:
                parsed["flags"].append(flag_info)
        
        # Extract positional arguments
        for match in self.arg_pattern.finditer(help_text):
            arg_info = {
                "name": match.group(1),
                "description": match.group(2).strip(),
                "required": True
            }
            parsed["arguments"].append(arg_info)
        
        # Extract optional arguments
        for match in self.optional_arg_pattern.finditer(help_text):
            arg_info = {
                "name": match.group(1),
                "description": match.group(2).strip(),
                "required": False
            }
            parsed["optional_arguments"].append(arg_info)
        
        # Identify global flags (common ones)
        parsed["global_flags"] = self._identify_global_flags(parsed["flags"])
        
        return parsed
    
    def extract_description(self, help_text: str, command: str) -> str:
        """Extract a description from help text.
        
        Args:
            help_text: Raw help text from CLI
            command: Command name for fallback description
            
        Returns:
            Extracted or generated description
            
        AI_CONTEXT:
            Extracts the first paragraph of help text as description,
            stopping at bullet points, flags, or empty lines. Falls
            back to a generic description if extraction fails.
        """
        if not help_text:
            return f"Execute {command} command"
        
        # Try to extract first paragraph
        lines = help_text.strip().split('\n')
        description_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                break
            if line.startswith(('-', '*', '•')) or re.match(r'^\s*\w+:', line):
                break
            if self._is_usage_line(line):
                continue
            description_lines.append(line)
        
        if description_lines:
            return ' '.join(description_lines)
        
        return f"Execute {command} command"
    
    def create_parameter_schema(self, cli_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create JSON schema for CLI parameters.
        
        Args:
            cli_data: CLI knowledge data
            
        Returns:
            JSON schema for the parameters
            
        AI_CONTEXT:
            Generates a complete JSON schema including:
            - Properties for each parameter
            - Required array for mandatory parameters
            - Type constraints based on CLI patterns
            - Enum values for known options
            - Descriptions from help text
        """
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Add subcommand property if there are subcommands
        if cli_data.get("subcommands"):
            schema["properties"]["subcommand"] = {
                "type": "string",
                "description": "Subcommand to execute",
                "enum": cli_data["subcommands"]
            }
        
        # Add common flags
        if cli_data.get("global_flags"):
            schema["properties"]["flags"] = {
                "type": "array",
                "description": "Command flags",
                "items": {
                    "type": "string",
                    "enum": cli_data["global_flags"]
                }
            }
        
        # Add generic arguments property
        schema["properties"]["arguments"] = {
            "type": "array",
            "description": "Additional arguments",
            "items": {"type": "string"}
        }
        
        # Add working directory property
        schema["properties"]["working_directory"] = {
            "type": "string",
            "description": "Working directory for command execution"
        }
        
        return schema
    
    def create_schema_from_parsed_help(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Create JSON schema from parsed help text.
        
        Args:
            parsed: Parsed help text data
            
        Returns:
            JSON schema for the parameters
            
        AI_CONTEXT:
            Converts parsed help data into a proper JSON schema.
            Handles type inference - flags without values become
            booleans, flags with values become strings. Required
            arguments go into the required array.
        """
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Add positional arguments
        for arg in parsed["arguments"]:
            schema["properties"][arg["name"]] = {
                "type": "string",
                "description": arg["description"]
            }
            if arg.get("required", True):
                schema["required"].append(arg["name"])
        
        # Add optional arguments
        for arg in parsed.get("optional_arguments", []):
            schema["properties"][arg["name"]] = {
                "type": "string",
                "description": arg["description"]
            }
        
        # Add flags as properties
        for flag in parsed["flags"]:
            prop_name = flag["name"].replace("-", "_")
            
            if flag["has_value"]:
                schema["properties"][prop_name] = {
                    "type": "string",
                    "description": flag["description"]
                }
            else:
                schema["properties"][prop_name] = {
                    "type": "boolean",
                    "description": flag["description"]
                }
        
        # Always include generic arguments
        schema["properties"]["extra_args"] = {
            "type": "array",
            "description": "Additional arguments",
            "items": {"type": "string"}
        }
        
        return schema
    
    def _parse_flag_match(self, match: re.Match) -> Optional[Dict[str, Any]]:
        """Parse a regex match for a flag.
        
        Args:
            match: Regex match object
            
        Returns:
            Flag info dictionary or None
            
        AI_CONTEXT:
            Extracts flag information from regex match groups,
            handling both short and long flag forms, value names,
            and descriptions.
        """
        short_flag = match.group(1) if match.group(1) and match.group(1).startswith('-') and len(match.group(1)) == 2 else None
        long_flag = match.group(2) if match.group(2) else (match.group(1) if match.group(1).startswith('--') else None)
        arg_name = match.group(3) or match.group(4)
        description = match.group(5).strip()
        
        if not (short_flag or long_flag):
            return None
        
        flag_info = {
            "name": long_flag.lstrip('--') if long_flag else short_flag.lstrip('-'),
            "short": short_flag,
            "long": long_flag,
            "description": description,
            "has_value": bool(arg_name),
            "value_name": arg_name
        }
        
        return flag_info
    
    def _identify_global_flags(self, flags: List[Dict[str, Any]]) -> List[str]:
        """Identify common global flags.
        
        Args:
            flags: List of parsed flags
            
        Returns:
            List of global flag names
            
        AI_CONTEXT:
            Identifies flags that are likely global (available for all
            subcommands) based on common patterns like --help, --version,
            --verbose, etc.
        """
        global_patterns = [
            'help', 'version', 'verbose', 'quiet', 'debug',
            'config', 'no-color', 'color'
        ]
        
        global_flags = []
        for flag in flags:
            flag_name = flag['name'].lower()
            if any(pattern in flag_name for pattern in global_patterns):
                if flag['long']:
                    global_flags.append(flag['long'])
                elif flag['short']:
                    global_flags.append(flag['short'])
        
        return global_flags
    
    def _is_usage_line(self, line: str) -> bool:
        """Check if a line is a usage line.
        
        Args:
            line: Line to check
            
        Returns:
            True if it's a usage line
            
        AI_CONTEXT:
            Usage lines typically start with "Usage:" or "usage:"
            and should be excluded from descriptions.
        """
        return bool(re.match(r'^\s*(Usage|usage|USAGE):', line))