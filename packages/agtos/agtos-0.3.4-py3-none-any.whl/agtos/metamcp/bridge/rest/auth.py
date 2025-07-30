"""Authentication handling for REST Bridge.

This module handles credential retrieval and authentication header
construction for various auth methods (Bearer, API Key, Basic).

AI_CONTEXT: Authentication is a critical security component. This module:
1. Retrieves credentials from secure storage (env vars now, keychain later)
2. Formats authentication headers according to API requirements
3. Caches auth data to avoid repeated credential lookups
4. Supports multiple auth schemes with fallback logic

The module is designed to be defensive - it never logs credentials
and provides clear error messages when auth fails.
"""
import os
import base64
from typing import Dict, Any, List, Optional


def get_credential(key: str) -> Optional[str]:
    """Get a credential from environment variables.
    
    AI_CONTEXT: This is a simple credential retrieval function that
    checks environment variables. In the future, this will be replaced
    with the full credential provider system that supports multiple
    backends (keychain, 1Password, etc.).
    
    The function checks for credentials in this order:
    1. Direct environment variable (e.g., GITHUB_TOKEN)
    2. Uppercase version with _API_KEY suffix
    3. Uppercase version with _TOKEN suffix
    
    Args:
        key: Credential key (e.g., "github_token", "stripe_api_key")
        
    Returns:
        Credential value or None if not found
    """
    # Try direct lookup
    value = os.environ.get(key)
    if value:
        return value
    
    # Try uppercase variations
    base_key = key.upper().replace("-", "_")
    
    # Try exact uppercase
    value = os.environ.get(base_key)
    if value:
        return value
    
    # Try with _API_KEY suffix if not already present
    if not base_key.endswith("_API_KEY") and not base_key.endswith("_TOKEN"):
        value = os.environ.get(f"{base_key}_API_KEY")
        if value:
            return value
        
        value = os.environ.get(f"{base_key}_TOKEN")
        if value:
            return value
    
    return None


class AuthHandler:
    """Handles authentication for REST API requests.
    
    AI_CONTEXT: This class manages authentication by:
    1. Caching auth headers to avoid repeated credential lookups
    2. Supporting multiple auth methods with priority ordering
    3. Providing secure credential handling without logging
    4. Generating proper headers for different auth schemes
    
    The handler supports:
    - Bearer tokens (OAuth2, JWT)
    - API keys (header or query parameter)
    - Basic authentication (username:password)
    - Custom header schemes
    """
    
    def __init__(self):
        self._auth_cache: Dict[str, Dict[str, str]] = {}
    
    def build_headers(self, auth_methods: List[Dict[str, Any]], api_name: str) -> Dict[str, str]:
        """Build authentication headers for the request.
        
        AI_CONTEXT: This method handles authentication by:
        
        1. Checking the auth methods defined for the API
        2. Retrieving credentials from the credential store
        3. Formatting headers according to the auth type:
           - Bearer: "Authorization: Bearer <token>"
           - API Key: Custom header or "X-API-Key: <key>"
           - Basic: "Authorization: Basic <base64(user:pass)>"
        
        The method caches authentication data to avoid repeated
        credential lookups. It supports multiple auth methods
        and uses the first one with available credentials.
        
        Args:
            auth_methods: List of auth methods from API knowledge
            api_name: Name of the API for credential lookup
            
        Returns:
            Dict of headers to include in the request
        """
        headers = {}
        
        # Check cache first
        if api_name in self._auth_cache:
            return self._auth_cache[api_name].copy()
        
        # Try each auth method
        for auth in auth_methods:
            auth_type = auth.get("type", "")
            
            if auth_type == "http" and auth.get("scheme") == "bearer":
                headers_with_bearer = self._handle_bearer_auth(api_name)
                if headers_with_bearer:
                    headers.update(headers_with_bearer)
                    self._auth_cache[api_name] = headers.copy()
                    break
                    
            elif auth_type == "api_key":
                headers_with_key = self._handle_api_key_auth(auth, api_name)
                if headers_with_key:
                    headers.update(headers_with_key)
                    self._auth_cache[api_name] = headers.copy()
                    break
                        
            elif auth_type == "basic":
                headers_with_basic = self._handle_basic_auth(api_name)
                if headers_with_basic:
                    headers.update(headers_with_basic)
                    self._auth_cache[api_name] = headers.copy()
                    break
        
        return headers
    
    def _handle_bearer_auth(self, api_name: str) -> Optional[Dict[str, str]]:
        """Handle Bearer token authentication.
        
        Args:
            api_name: Name of the API
            
        Returns:
            Headers dict with Authorization header or None
        """
        # Try to get bearer token
        token = get_credential(f"{api_name}_token") or get_credential(f"{api_name}_api_key")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return None
    
    def _handle_api_key_auth(self, auth: Dict[str, Any], api_name: str) -> Optional[Dict[str, str]]:
        """Handle API key authentication.
        
        Args:
            auth: Auth configuration dict
            api_name: Name of the API
            
        Returns:
            Headers dict with API key or None
        """
        key_name = auth.get("key_name", "X-API-Key")
        location = auth.get("in", "header")
        
        if location == "header":
            api_key = get_credential(f"{api_name}_api_key") or get_credential(f"{api_name}_key")
            if api_key:
                return {key_name: api_key}
        
        # TODO: Handle query parameter API keys
        return None
    
    def _handle_basic_auth(self, api_name: str) -> Optional[Dict[str, str]]:
        """Handle Basic authentication.
        
        Args:
            api_name: Name of the API
            
        Returns:
            Headers dict with Basic auth or None
        """
        username = get_credential(f"{api_name}_username")
        password = get_credential(f"{api_name}_password")
        
        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            return {"Authorization": f"Basic {credentials}"}
        
        return None
    
    def clear_cache(self, api_name: Optional[str] = None):
        """Clear authentication cache.
        
        Args:
            api_name: Specific API to clear, or None to clear all
        """
        if api_name:
            self._auth_cache.pop(api_name, None)
        else:
            self._auth_cache.clear()