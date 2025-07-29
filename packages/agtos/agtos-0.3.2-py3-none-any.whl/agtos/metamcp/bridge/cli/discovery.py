"""CLI tool discovery module for CLI Bridge.

This module handles discovering CLI tools from the knowledge store and
converting them into MCP tool specifications.

AI_CONTEXT:
    The CLIDiscovery class is responsible for finding available CLI tools,
    analyzing their capabilities, and generating MCP-compatible tool specs.
    It works with the knowledge store to cache and retrieve CLI information,
    and uses the HelpTextParser to understand CLI interfaces.
"""

import logging
from typing import Dict, List, Any, Optional

from ....knowledge_store import KnowledgeStore
from ....knowledge.cli import CLIKnowledge
from ...types import ToolSpec
from ...aliases import suggest_aliases_for_tool
from .parser import HelpTextParser

logger = logging.getLogger(__name__)


class CLIDiscovery:
    """Discovers and converts CLI tools to MCP tool specifications.
    
    AI_CONTEXT:
        This class handles the discovery phase of CLI integration:
        1. Finding available CLIs in the system or knowledge store
        2. Analyzing their capabilities through help text
        3. Generating tool specs for main commands and subcommands
        4. Managing aliases and natural language mappings
        
        It delegates parsing to HelpTextParser and focuses on the
        discovery and conversion workflow.
    """
    
    def __init__(self, store: KnowledgeStore, cli_knowledge: CLIKnowledge, parser: HelpTextParser):
        """Initialize discovery with required components.
        
        Args:
            store: Knowledge store for caching CLI information
            cli_knowledge: CLI knowledge acquisition system
            parser: Help text parser for schema generation
        """
        self.store = store
        self.cli_knowledge = cli_knowledge
        self.parser = parser
    
    def discover_cli_tools(self, cli_names: Optional[List[str]] = None) -> List[ToolSpec]:
        """Discover available CLI tools and convert to MCP tool specs.
        
        Args:
            cli_names: Optional list of specific CLIs to discover.
                      If None, discovers all CLIs in knowledge store.
                      
        Returns:
            List of ToolSpec objects for discovered CLI tools
            
        AI_CONTEXT:
            Main entry point for CLI discovery. Can operate in two modes:
            1. Targeted discovery - specific CLI names provided
            2. Full discovery - finds all CLIs in knowledge store
            
            For each CLI, it generates multiple tools (main + subcommands).
        """
        tools = []
        
        if cli_names:
            # Discover specific CLIs
            for cli_name in cli_names:
                cli_tools = self._discover_single_cli(cli_name)
                tools.extend(cli_tools)
        else:
            # Discover all CLIs in knowledge store
            cli_entries = self.store.search("", type="cli")
            for entry in cli_entries:
                cli_name = entry["name"]
                cli_tools = self._discover_single_cli(cli_name)
                tools.extend(cli_tools)
                
        return tools
    
    def _discover_single_cli(self, cli_name: str) -> List[ToolSpec]:
        """Discover tools for a single CLI command.
        
        Args:
            cli_name: Name of the CLI command (e.g., "git", "docker")
            
        Returns:
            List of ToolSpec objects for the CLI and its subcommands
            
        AI_CONTEXT:
            Discovers a single CLI by:
            1. Checking knowledge store for cached information
            2. Running discovery if not cached
            3. Creating tool spec for main command
            4. Creating tool specs for each subcommand
            
            Returns empty list if CLI is not available.
        """
        tools = []
        
        # Get CLI knowledge from store or discover it
        knowledge = self.store.retrieve("cli", cli_name)
        if not knowledge:
            # Try to discover the CLI
            knowledge_data = self.cli_knowledge.discover_cli_patterns(cli_name)
            if not knowledge_data.get("available"):
                logger.warning(f"CLI '{cli_name}' not found or not available")
                return tools
            knowledge = {"data": knowledge_data}
        
        cli_data = knowledge["data"]
        
        # Create main command tool
        main_tool = self._create_tool_spec(cli_name, cli_data)
        if main_tool:
            tools.append(main_tool)
        
        # Create tools for subcommands
        for subcommand in cli_data.get("subcommands", []):
            subcommand_help = self.cli_knowledge.get_subcommand_help(cli_name, subcommand)
            if subcommand_help:
                sub_tool = self._create_subcommand_tool_spec(cli_name, subcommand, subcommand_help)
                if sub_tool:
                    tools.append(sub_tool)
                    
        return tools
    
    def _create_tool_spec(self, cli_name: str, cli_data: Dict[str, Any]) -> Optional[ToolSpec]:
        """Create a tool spec for a CLI command.
        
        Args:
            cli_name: Name of the CLI command
            cli_data: CLI knowledge data from store
            
        Returns:
            ToolSpec object or None if creation fails
            
        AI_CONTEXT:
            Creates the main tool spec for a CLI. This handles CLIs that
            can be invoked directly (not just through subcommands).
            Includes examples in the description when available.
        """
        try:
            # Extract description from help text
            help_text = cli_data.get("help_text", "")
            description = self.parser.extract_description(help_text, cli_name)
            
            # Add examples to description if available
            examples = cli_data.get("examples", [])
            if examples:
                description += "\n\nExamples:\n"
                for example in examples[:3]:  # Limit to 3 examples
                    description += f"- {example}\n"
            
            # Create JSON schema for parameters
            schema = self.parser.create_parameter_schema(cli_data)
            
            # Generate display name and aliases
            display_name = f"{cli_name}"
            aliases = self._generate_aliases(cli_name, None)
            
            tool_spec = ToolSpec(
                name=f"cli__{cli_name}",
                description=description,
                inputSchema=schema,
                displayName=display_name,
                aliases=aliases
            )
            
            return tool_spec
            
        except Exception as e:
            logger.error(f"Error creating tool spec for {cli_name}: {e}")
            return None
    
    def _create_subcommand_tool_spec(self, cli_name: str, subcommand: str, help_text: str) -> Optional[ToolSpec]:
        """Create a tool spec for a CLI subcommand.
        
        Args:
            cli_name: Main CLI command name
            subcommand: Subcommand name
            help_text: Help text for the subcommand
            
        Returns:
            ToolSpec object or None if creation fails
            
        AI_CONTEXT:
            Creates tool specs for subcommands (e.g., "git status").
            Parses the subcommand-specific help text to understand its
            unique flags and arguments.
        """
        try:
            # Parse help text to extract flags and arguments
            parsed = self.parser.parse_help_text(help_text)
            
            # Extract description
            description = self.parser.extract_description(help_text, f"{cli_name} {subcommand}")
            
            # Create schema from parsed data
            schema = self.parser.create_schema_from_parsed_help(parsed)
            
            # Use double underscore as separator
            display_name = f"{cli_name} {subcommand}"
            aliases = self._generate_aliases(cli_name, subcommand)
            
            tool_spec = ToolSpec(
                name=f"cli__{cli_name}__{subcommand}",
                description=description,
                inputSchema=schema,
                displayName=display_name,
                aliases=aliases
            )
            
            return tool_spec
            
        except Exception as e:
            logger.error(f"Error creating tool spec for {cli_name} {subcommand}: {e}")
            return None
    
    def _generate_aliases(self, cli_name: str, subcommand: Optional[str] = None) -> List[str]:
        """Generate natural language aliases for a CLI command.
        
        Args:
            cli_name: Main CLI command name
            subcommand: Optional subcommand name
            
        Returns:
            List of natural language aliases
            
        AI_CONTEXT:
            Integrates with the comprehensive alias system to get all
            registered aliases. Also ensures basic command forms are
            included (e.g., "git status" for cli__git__status).
        """
        # Generate the tool name
        if subcommand:
            tool_name = f"cli__{cli_name}__{subcommand}"
        else:
            tool_name = f"cli__{cli_name}"
        
        # Get aliases from the registry
        aliases = suggest_aliases_for_tool(tool_name)
        
        # Always add the basic command alias
        if subcommand:
            basic_alias = f"{cli_name} {subcommand}"
            if basic_alias not in aliases:
                aliases.insert(0, basic_alias)
            
            # Add natural form with spaces instead of hyphens
            if '-' in subcommand:
                natural = subcommand.replace('-', ' ')
                natural_alias = f"{cli_name} {natural}"
                if natural_alias not in aliases:
                    aliases.append(natural_alias)
                if natural not in aliases:
                    aliases.append(natural)
        else:
            if cli_name not in aliases:
                aliases.insert(0, cli_name)
        
        return aliases
    
    def refresh_cli_knowledge(self, cli_name: str) -> bool:
        """Refresh knowledge for a specific CLI.
        
        Args:
            cli_name: Name of the CLI to refresh
            
        Returns:
            True if successful, False otherwise
            
        AI_CONTEXT:
            Forces re-discovery of a CLI, bypassing the cache.
            Useful when CLI has been updated or when troubleshooting.
        """
        try:
            # Re-discover CLI without cache
            knowledge = self.cli_knowledge.discover_cli_patterns(cli_name, use_cache=False)
            
            if not knowledge.get("available"):
                return False
                
            # Re-discover examples
            self.cli_knowledge.discover_command_examples(cli_name)
            
            # Knowledge is automatically stored by discover_cli_patterns
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing CLI knowledge for {cli_name}: {e}")
            return False