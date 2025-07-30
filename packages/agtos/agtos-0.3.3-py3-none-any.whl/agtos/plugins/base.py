"""Base plugin interface for agentctl plugins."""
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for agentctl plugins.
    
    All plugins should inherit from this class and implement
    the required methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the plugin name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the plugin description."""
        pass
    
    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools provided by this plugin.
        
        Each tool should be a dictionary with:
        - name: Tool name
        - description: Tool description
        - handler: Function to call
        - parameters: Parameter schema
        """
        pass