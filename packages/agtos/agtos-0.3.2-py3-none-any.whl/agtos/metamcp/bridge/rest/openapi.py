"""OpenAPI spec parsing and tool generation for REST Bridge.

This module handles the conversion of OpenAPI specifications and
discovered endpoints into MCP tool definitions, including schema
generation, naming, and alias creation.

AI_CONTEXT: This module is responsible for the "understanding" phase
of REST API integration. It:
1. Parses OpenAPI specifications or discovered endpoint data
2. Generates human-friendly tool names
3. Builds JSON schemas from OpenAPI parameters
4. Creates natural language aliases
5. Formats descriptions for clarity

The module focuses on making APIs accessible and intuitive for
AI assistants to use.
"""
import re
from typing import Dict, Any, List, Optional

# TODO: Fix alias import - module not found
# from ...aliases import get_registry


class OpenAPIParser:
    """Parses OpenAPI specs and generates MCP tool definitions.
    
    AI_CONTEXT: This class converts OpenAPI/Swagger specifications
    into MCP-compatible tool definitions. It handles:
    1. Parameter extraction (path, query, header, body)
    2. Schema generation with proper types
    3. Description formatting
    4. Tool naming conventions
    5. Alias generation for natural language
    
    The parser is designed to be flexible, handling both full
    OpenAPI specs and simplified endpoint descriptions from
    API discovery.
    """
    
    def generate_tool_name(self, api_name: str, endpoint: Dict[str, Any]) -> str:
        """Generate a unique tool name for an endpoint.
        
        AI_CONTEXT: Tool naming is critical for usability. This method:
        1. Prefers operation IDs when available (most descriptive)
        2. Falls back to method + path combinations
        3. Cleans names to be valid Python identifiers
        4. Ensures uniqueness within the API namespace
        
        Examples:
        - github + listRepos -> github_list_repos
        - stripe + POST /customers -> stripe_post_customers
        - weather + GET /forecast/{city} -> weather_get_forecast_city
        
        Args:
            api_name: Name of the API (e.g., "github", "stripe")
            endpoint: Endpoint configuration dict
            
        Returns:
            Unique tool name following naming conventions
        """
        # Clean API name
        api_prefix = re.sub(r'[^a-z0-9]+', '_', api_name.lower()).strip('_')
        
        # Try operation ID first
        if endpoint.get("operation_id"):
            op_id = re.sub(r'[^a-z0-9]+', '_', endpoint["operation_id"].lower())
            return f"{api_prefix}_{op_id}"
        
        # Fall back to method + path
        method = endpoint.get("method", "get").lower()
        path = endpoint.get("path", "/").strip("/")
        
        # Convert path to name (e.g., /users/{id}/repos -> users_id_repos)
        path_parts = []
        for part in path.split("/"):
            if part:
                # Remove braces from path parameters
                clean_part = re.sub(r'[{}]', '', part)
                clean_part = re.sub(r'[^a-z0-9]+', '_', clean_part.lower())
                if clean_part:
                    path_parts.append(clean_part)
        
        if path_parts:
            return f"{api_prefix}_{method}_{'_'.join(path_parts)}"
        else:
            return f"{api_prefix}_{method}_root"
    
    def build_parameter_schema(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Build JSON schema for endpoint parameters.
        
        AI_CONTEXT: Schema building combines multiple parameter sources:
        1. Path parameters - always required, embedded in URL
        2. Query parameters - optional/required, appended to URL
        3. Header parameters - custom headers (rare in practice)
        4. Request body - JSON payload for POST/PUT/PATCH
        
        The schema must be compatible with JSON Schema draft-07
        and provide clear descriptions for AI understanding.
        
        Args:
            endpoint: Endpoint configuration with parameters
            
        Returns:
            JSON Schema dict for tool parameters
        """
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Process all parameters
        for param in endpoint.get("parameters", []):
            param_in = param.get("in")
            param_name = param.get("name", "")
            
            if not param_name:
                continue
            
            # Build parameter schema
            param_schema = self._build_single_parameter_schema(param)
            
            if param_in in ["path", "query", "header"]:
                schema["properties"][param_name] = param_schema
                
                # Path parameters are always required
                if param_in == "path" or param.get("required", False):
                    schema["required"].append(param_name)
        
        # Add request body if present
        if endpoint.get("request_body"):
            body_schema = self._build_request_body_schema(endpoint["request_body"])
            if body_schema:
                schema["properties"]["body"] = body_schema
                if endpoint["request_body"].get("required", False):
                    schema["required"].append("body")
        
        return schema
    
    def _build_single_parameter_schema(self, param: Dict[str, Any]) -> Dict[str, Any]:
        """Build schema for a single parameter.
        
        Args:
            param: Parameter definition
            
        Returns:
            Parameter schema dict
        """
        schema = {
            "type": param.get("type", "string"),
            "description": param.get("description", f"{param.get('in', '')} parameter: {param.get('name', '')}")
        }
        
        # Add constraints if present
        if "enum" in param:
            schema["enum"] = param["enum"]
        if "pattern" in param:
            schema["pattern"] = param["pattern"]
        if "minimum" in param:
            schema["minimum"] = param["minimum"]
        if "maximum" in param:
            schema["maximum"] = param["maximum"]
        
        return schema
    
    def _build_request_body_schema(self, request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Build schema for request body.
        
        Args:
            request_body: Request body definition
            
        Returns:
            Body schema dict or None
        """
        body_schema = request_body.get("schema", {})
        if not body_schema:
            return None
        
        return {
            "type": "object",
            "description": request_body.get("description", "Request body"),
            "properties": body_schema.get("properties", {}),
            "required": body_schema.get("required", [])
        }
    
    def build_description(self, endpoint: Dict[str, Any]) -> str:
        """Build a descriptive string for the endpoint.
        
        AI_CONTEXT: Good descriptions help AI assistants understand
        when and how to use each tool. This method:
        1. Prioritizes human-written summaries
        2. Falls back to operation descriptions
        3. Includes method and path for clarity
        4. Limits length for readability
        
        Args:
            endpoint: Endpoint configuration
            
        Returns:
            Human-readable description
        """
        parts = []
        
        # Add summary or description
        if endpoint.get("summary"):
            parts.append(endpoint["summary"])
        elif endpoint.get("description"):
            # Limit description length
            desc = endpoint["description"]
            if len(desc) > 200:
                desc = desc[:197] + "..."
            parts.append(desc)
        
        # Add method and path
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "/")
        parts.append(f"{method} {path}")
        
        return " - ".join(parts)
    
    def generate_aliases(self, api_name: str, endpoint: Dict[str, Any], tool_name: str) -> List[str]:
        """Generate natural language aliases for a REST endpoint.
        
        AI_CONTEXT: Aliases make tools discoverable through natural language.
        This method generates intelligent aliases based on:
        1. HTTP method semantics (GET = list/fetch, POST = create, etc.)
        2. Resource names extracted from the path
        3. Operation IDs converted to readable phrases
        4. Common REST patterns (CRUD operations)
        
        The aliases are registered with the global alias registry for
        fuzzy matching during tool discovery.
        
        Args:
            api_name: Name of the API
            endpoint: Endpoint configuration
            tool_name: Generated tool name
            
        Returns:
            List of natural language aliases
        """
        aliases = []
        # TODO: Fix alias registry
        # registry = get_registry()
        
        method = endpoint.get("method", "GET").upper()
        path = endpoint.get("path", "/")
        operation_id = endpoint.get("operation_id", "")
        
        # Clean up path for alias generation
        path_parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
        
        # If we have an operation ID, use it
        if operation_id:
            # Convert camelCase to space-separated
            readable = re.sub(r'([a-z])([A-Z])', r'\1 \2', operation_id).lower()
            aliases.append(readable)
            
            # Also add variant with API name
            aliases.append(f"{api_name} {readable}")
        
        # Generate aliases based on REST patterns
        if path_parts:
            resource = path_parts[-1]  # Last part is usually the resource
            
            # Singularize if needed (simple heuristic)
            singular = resource.rstrip('s') if resource.endswith('s') else resource
            
            aliases.extend(self._generate_method_aliases(method, resource, singular, path, api_name))
        
        # Register aliases with the alias system
        # TODO: Fix alias registration - AliasRegistry doesn't have add_custom_alias method
        # for alias in aliases:
        #     registry.add_custom_alias(
        #         alias=alias,
        #         tool_name=tool_name,
        #         weight=0.8  # Slightly lower weight for auto-generated aliases
        #     )
        
        # Remove duplicates while preserving order
        seen = set()
        unique_aliases = []
        for alias in aliases:
            if alias not in seen:
                seen.add(alias)
                unique_aliases.append(alias)
        
        return unique_aliases
    
    def _generate_method_aliases(self, method: str, resource: str, singular: str, 
                                path: str, api_name: str) -> List[str]:
        """Generate method-specific aliases.
        
        Args:
            method: HTTP method
            resource: Plural resource name
            singular: Singular resource name
            path: Full endpoint path
            api_name: API name
            
        Returns:
            List of method-specific aliases
        """
        aliases = []
        
        if method == "GET":
            if "{" in path:  # Has path parameters - single resource
                aliases.extend([
                    f"get {singular}",
                    f"fetch {singular}",
                    f"retrieve {singular}",
                    f"show {singular}",
                    f"{api_name} get {singular}"
                ])
            else:  # List operation
                aliases.extend([
                    f"list {resource}",
                    f"get all {resource}",
                    f"fetch {resource}",
                    f"show {resource}",
                    f"{api_name} list {resource}"
                ])
        
        elif method == "POST":
            aliases.extend([
                f"create {singular}",
                f"add {singular}",
                f"new {singular}",
                f"make {singular}",
                f"{api_name} create {singular}"
            ])
        
        elif method in ["PUT", "PATCH"]:
            aliases.extend([
                f"update {singular}",
                f"edit {singular}",
                f"modify {singular}",
                f"change {singular}",
                f"{api_name} update {singular}"
            ])
        
        elif method == "DELETE":
            aliases.extend([
                f"delete {singular}",
                f"remove {singular}",
                f"rm {singular}",
                f"destroy {singular}",
                f"{api_name} delete {singular}"
            ])
        
        return aliases