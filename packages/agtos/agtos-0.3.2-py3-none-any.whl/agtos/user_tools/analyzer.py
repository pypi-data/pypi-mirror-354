"""Natural language API analyzer.

This module analyzes natural language descriptions to extract API specifications.

AI_CONTEXT:
    The analyzer is responsible for understanding user intent from descriptions like:
    - "I need to post messages to api.company.com/messages"
    - "Get user data from https://api.service.com/users/{id}"
    - "Update products at our API using PUT requests"
    
    It extracts:
    - Base URLs and endpoints
    - HTTP methods
    - Parameters (path, query, body)
    - Authentication requirements
    - Response expectations
"""

import re
import logging
from typing import List, Optional, Dict, Tuple
from urllib.parse import urlparse, parse_qs

from .models import (
    APIEndpoint, 
    HTTPMethod, 
    Parameter,
    ParameterLocation,
    AuthenticationMethod,
    AuthType,
    ToolSpecification
)

logger = logging.getLogger(__name__)


class APIAnalyzer:
    """Analyzes natural language to extract API specifications.
    
    AI_CONTEXT: This is the brain that understands what the user wants.
    It uses patterns and heuristics to extract structured API information
    from free-form descriptions.
    """
    
    # Patterns for extracting API information
    URL_PATTERN = re.compile(
        r'https?://[^\s<>"|\\^`\[\]]+|'
        r'(?:api\.|/api/)[^\s<>"|\\^`\[\]]+'
    )
    
    METHOD_PATTERNS = {
        HTTPMethod.GET: r'\b(get|fetch|retrieve|read|list|show)\b',
        HTTPMethod.POST: r'\b(post|create|send|submit|add)\b',
        HTTPMethod.PUT: r'\b(put|update|modify|edit)\b',
        HTTPMethod.DELETE: r'\b(delete|remove|destroy)\b',
        HTTPMethod.PATCH: r'\b(patch|partial|update partially)\b'
    }
    
    AUTH_PATTERNS = {
        AuthType.BEARER: r'\b(bearer|token|jwt|access token)\b',
        AuthType.API_KEY: r'\b(api[- ]?key|key|apikey)\b',
        AuthType.BASIC: r'\b(basic auth|username|password)\b',
    }
    
    def analyze(self, description: str, name: str = None) -> ToolSpecification:
        """Analyze natural language description to extract API specification.
        
        Args:
            description: Natural language description of the API
            name: Optional tool name (will be inferred if not provided)
            
        Returns:
            ToolSpecification with extracted information
        """
        logger.info(f"Analyzing description: {description[:100]}...")
        
        # Extract endpoints
        endpoints = self._extract_endpoints(description)
        
        # Infer tool name if not provided
        if not name:
            name = self._infer_tool_name(description, endpoints)
        
        # Extract authentication
        auth = self._extract_authentication(description)
        
        # Apply auth to all endpoints
        for endpoint in endpoints:
            if not endpoint.authentication:
                endpoint.authentication = auth
        
        return ToolSpecification(
            name=name,
            description=self._generate_description(endpoints),
            natural_language_spec=description,
            endpoints=endpoints,
            tags=self._extract_tags(description)
        )
    
    def _extract_endpoints(self, description: str) -> List[APIEndpoint]:
        """Extract API endpoints from description."""
        endpoints = []
        
        # Find URLs in the description
        urls = self.URL_PATTERN.findall(description)
        
        if not urls:
            # Try to construct from context
            urls = self._infer_urls(description)
        
        for url in urls:
            # Extract method
            method = self._extract_method(description, url)
            
            # Extract parameters
            parameters = self._extract_parameters(description, url)
            
            # Create endpoint
            endpoint = APIEndpoint(
                url=self._normalize_url(url),
                method=method,
                description=self._extract_endpoint_description(description, url),
                parameters=parameters
            )
            
            endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_method(self, description: str, url: str) -> HTTPMethod:
        """Extract HTTP method from description context."""
        description_lower = description.lower()
        
        # Check for explicit method mentions
        for method, pattern in self.METHOD_PATTERNS.items():
            if re.search(pattern, description_lower):
                return method
        
        # Default based on context
        if '{' in url or 'id' in url.lower():
            return HTTPMethod.GET  # Likely fetching specific resource
        
        return HTTPMethod.POST  # Default for APIs
    
    def _extract_parameters(self, description: str, url: str) -> List[Parameter]:
        """Extract parameters from description and URL."""
        parameters = []
        
        # Extract path parameters from URL
        path_params = re.findall(r'\{([^}]+)\}', url)
        for param in path_params:
            parameters.append(Parameter(
                name=param,
                type="string",
                location=ParameterLocation.PATH,
                required=True,
                description=f"Path parameter {param}"
            ))
        
        # Extract mentioned fields from description
        # Look for patterns like "with title and content" or "including name, email"
        field_patterns = [
            r'with\s+(?:the\s+)?([^.]+?)(?:\.|$|\s+using|\s+with)',
            r'including\s+([^.]+?)(?:\.|$)',
            r'fields?:?\s*([^.]+?)(?:\.|$)',
            r'parameters?:?\s*([^.]+?)(?:\.|$)'
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, description.lower())
            for match in matches:
                # Stop at certain keywords
                stop_words = ['using', 'with', 'bearer', 'token', 'api', 'key', 'auth']
                for stop_word in stop_words:
                    if stop_word in match:
                        match = match.split(stop_word)[0]
                
                # Split by common separators
                fields = re.split(r'[,;&]|\s+and\s+', match)
                for field in fields:
                    field = field.strip()
                    # Clean up field name
                    if field and len(field) < 30 and not any(sw in field for sw in stop_words):
                        param_location = (
                            ParameterLocation.BODY 
                            if self._extract_method(description, url) in [HTTPMethod.POST, HTTPMethod.PUT]
                            else ParameterLocation.QUERY
                        )
                        # Avoid duplicates
                        param_names = {p.name for p in parameters}
                        clean_name = field.replace(' ', '_').replace('-', '_')
                        if clean_name not in param_names:
                            parameters.append(Parameter(
                                name=clean_name,
                                type="string",
                                location=param_location,
                                required=False
                            ))
        
        return parameters
    
    def _extract_authentication(self, description: str) -> Optional[AuthenticationMethod]:
        """Extract authentication method from description."""
        description_lower = description.lower()
        
        for auth_type, pattern in self.AUTH_PATTERNS.items():
            if re.search(pattern, description_lower):
                # Extract specific details
                if auth_type == AuthType.BEARER:
                    return AuthenticationMethod(
                        type=AuthType.BEARER,
                        location="header",
                        key_name="Authorization",
                        value_prefix="Bearer "
                    )
                elif auth_type == AuthType.API_KEY:
                    # Check if header or query
                    if 'header' in description_lower:
                        location = "header"
                    elif 'query' in description_lower or 'url' in description_lower:
                        location = "query"
                    else:
                        location = "header"  # Default
                    
                    return AuthenticationMethod(
                        type=AuthType.API_KEY,
                        location=location,
                        key_name="X-API-Key"
                    )
        
        return None
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to ensure it's valid."""
        if not url.startswith(('http://', 'https://')):
            # Assume HTTPS
            url = f"https://{url}"
        
        # Don't remove trailing slashes if there are path params
        if '{' not in url:
            url = url.rstrip('/')
        
        return url
    
    def _infer_tool_name(self, description: str, endpoints: List[APIEndpoint]) -> str:
        """Infer a tool name from the description."""
        # Try to extract service name from URL
        if endpoints:
            parsed = urlparse(endpoints[0].url)
            domain_parts = parsed.netloc.split('.')
            if len(domain_parts) > 1:
                # Get the main domain name
                name = domain_parts[-2] if domain_parts[-2] != 'api' else domain_parts[0]
                return f"{name}_tool"
        
        # Extract from description
        words = description.lower().split()
        for word in ['api', 'service', 'platform', 'system']:
            if word in words:
                idx = words.index(word)
                if idx > 0:
                    return f"{words[idx-1]}_{word}"
        
        return "custom_api_tool"
    
    def _generate_description(self, endpoints: List[APIEndpoint]) -> str:
        """Generate a concise description from endpoints."""
        if not endpoints:
            return "Custom API tool"
        
        methods = list(set(ep.method.value for ep in endpoints))
        urls = list(set(urlparse(ep.url).netloc for ep in endpoints))
        
        return f"Tool for {', '.join(methods)} operations on {', '.join(urls)}"
    
    def _extract_tags(self, description: str) -> List[str]:
        """Extract relevant tags from description."""
        tags = ["custom", "user-generated"]
        
        # Add method tags
        description_lower = description.lower()
        for method, pattern in self.METHOD_PATTERNS.items():
            if re.search(pattern, description_lower):
                tags.append(method.value.lower())
        
        return tags
    
    def _infer_urls(self, description: str) -> List[str]:
        """Try to infer URLs from description when none are explicitly provided."""
        # This is a fallback for descriptions like "our company API"
        # In real implementation, this might prompt the user
        return []
    
    def _extract_endpoint_description(self, description: str, url: str) -> str:
        """Extract description specific to an endpoint."""
        # Find sentence containing the URL
        sentences = description.split('.')
        for sentence in sentences:
            if url in sentence or urlparse(url).path in sentence:
                return sentence.strip()
        
        return f"API endpoint at {url}"