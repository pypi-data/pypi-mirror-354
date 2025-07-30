"""Request execution and response handling for REST Bridge.

This module handles the actual HTTP request execution, including
rate limiting, URL construction, response parsing, and error handling.

AI_CONTEXT: This module is responsible for the runtime execution of
REST API calls. It implements:
1. Rate limiting with exponential backoff
2. URL construction with path/query parameters
3. Request execution with timeout handling
4. Response transformation to MCP format
5. Detailed error extraction for debugging

The module is designed to be resilient and provide maximum information
when things go wrong, helping AI assistants debug issues independently.
"""
import json
import time
import requests
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse, urlencode
from datetime import datetime, timedelta


class RateLimiter:
    """Simple rate limiter for API calls.
    
    AI_CONTEXT: This class implements a per-host rate limiter that:
    1. Tracks API calls to prevent overwhelming servers
    2. Implements exponential backoff on 429 responses
    3. Respects Retry-After headers when present
    4. Maintains a sliding window of recent calls
    
    The rate limiter is designed to be non-blocking - it returns
    wait times rather than sleeping, allowing the caller to decide
    how to handle rate limits.
    """
    
    def __init__(self):
        self.calls: Dict[str, List[datetime]] = {}
        self.backoff: Dict[str, datetime] = {}
    
    def check_rate_limit(self, url: str) -> Optional[float]:
        """Check if we should wait before making a request.
        
        Args:
            url: The URL to check
            
        Returns:
            Number of seconds to wait, or None if no wait needed
        """
        host = urlparse(url).netloc
        
        # Check backoff
        if host in self.backoff:
            wait_until = self.backoff[host]
            if datetime.now() < wait_until:
                return (wait_until - datetime.now()).total_seconds()
            else:
                del self.backoff[host]
        
        return None
    
    def record_call(self, url: str, response: Optional[requests.Response] = None):
        """Record an API call and check for rate limit headers.
        
        Args:
            url: The URL that was called
            response: The response object (to check for 429 status)
        """
        host = urlparse(url).netloc
        
        # Record the call
        if host not in self.calls:
            self.calls[host] = []
        self.calls[host].append(datetime.now())
        
        # Clean old calls (older than 1 hour)
        cutoff = datetime.now() - timedelta(hours=1)
        self.calls[host] = [dt for dt in self.calls[host] if dt > cutoff]
        
        # Check rate limit headers if response provided
        if response and response.status_code == 429:
            # Look for Retry-After header
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                try:
                    # Could be seconds or HTTP date
                    seconds = int(retry_after)
                    self.backoff[host] = datetime.now() + timedelta(seconds=seconds)
                except ValueError:
                    # Default to 60 seconds
                    self.backoff[host] = datetime.now() + timedelta(seconds=60)
            else:
                # Default backoff
                self.backoff[host] = datetime.now() + timedelta(seconds=60)


class RequestExecutor:
    """Executes HTTP requests for REST API tools.
    
    AI_CONTEXT: This class handles the execution phase of REST API calls.
    It's responsible for:
    1. Building complete URLs from base + path + parameters
    2. Constructing request headers and body
    3. Executing HTTP requests with proper error handling
    4. Transforming responses to MCP format
    5. Extracting meaningful error messages
    
    The executor is stateless and thread-safe, using only the
    provided parameters for each request.
    """
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        self.rate_limiter = rate_limiter or RateLimiter()
    
    def execute_request(self,
                       method: str,
                       base_url: str,
                       endpoint: Dict[str, Any],
                       params: Dict[str, Any],
                       headers: Dict[str, str],
                       timeout: int = 30) -> Dict[str, Any]:
        """Execute an HTTP request for a REST API endpoint.
        
        AI_CONTEXT: This method coordinates the full request execution:
        1. Checks rate limits and waits if necessary
        2. Builds the complete URL with parameters
        3. Adds required headers (Accept, Content-Type)
        4. Makes the HTTP request with timeout
        5. Handles various error scenarios
        6. Returns structured response data
        
        Args:
            method: HTTP method (GET, POST, etc.)
            base_url: Base URL of the API
            endpoint: Endpoint configuration
            params: Parameters from the tool call
            headers: Authentication and other headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict with success status, data, and error info
        """
        try:
            # Check and wait for rate limit
            self._check_and_wait_rate_limit(base_url)
            
            # Build URL and prepare request
            url = self.build_url(base_url, endpoint, params)
            request_headers = self._prepare_request_headers(headers)
            body = params.get("body")
            
            # Execute request
            response = self._execute_http_request(
                method, url, request_headers, body, timeout
            )
            
            # Record for rate limiting and handle response
            self.rate_limiter.record_call(url, response)
            return self._handle_response(response)
                
        except requests.exceptions.Timeout:
            return self._build_timeout_error(timeout)
        except requests.exceptions.ConnectionError:
            return self._build_connection_error()
        except Exception as e:
            return self._build_unexpected_error(e)
    
    def _check_and_wait_rate_limit(self, base_url: str) -> None:
        """Check rate limit and wait if necessary.
        
        Args:
            base_url: API base URL for rate limit checking
        """
        wait_time = self.rate_limiter.check_rate_limit(base_url)
        if wait_time:
            time.sleep(wait_time)
    
    def _prepare_request_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Prepare headers for JSON API request.
        
        Args:
            headers: Base headers to extend
            
        Returns:
            Complete headers with Accept and Content-Type
        """
        request_headers = headers.copy()
        request_headers["Accept"] = "application/json"
        request_headers["Content-Type"] = "application/json"
        return request_headers
    
    def _execute_http_request(self,
                             method: str,
                             url: str,
                             headers: Dict[str, str],
                             body: Optional[Any],
                             timeout: int) -> requests.Response:
        """Execute the actual HTTP request.
        
        Args:
            method: HTTP method
            url: Complete URL
            headers: Request headers
            body: Request body (if any)
            timeout: Request timeout
            
        Returns:
            Response object
        """
        return requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=body if body else None,
            timeout=timeout
        )
    
    def _build_timeout_error(self, timeout: int) -> Dict[str, Any]:
        """Build timeout error response.
        
        Args:
            timeout: Timeout duration that was exceeded
            
        Returns:
            Error response dict
        """
        return {
            "success": False,
            "error": f"Request timed out after {timeout} seconds"
        }
    
    def _build_connection_error(self) -> Dict[str, Any]:
        """Build connection error response.
        
        Returns:
            Error response dict
        """
        return {
            "success": False,
            "error": "Failed to connect to the API"
        }
    
    def _build_unexpected_error(self, exception: Exception) -> Dict[str, Any]:
        """Build unexpected error response.
        
        Args:
            exception: The exception that occurred
            
        Returns:
            Error response dict
        """
        return {
            "success": False,
            "error": f"Unexpected error: {str(exception)}"
        }
    
    def build_url(self, base_url: str, endpoint: Dict[str, Any], params: Dict[str, Any]) -> str:
        """Build the full URL for the request.
        
        AI_CONTEXT: URL building involves:
        1. Joining base URL with endpoint path
        2. Substituting path parameters (e.g., {id})
        3. Adding query parameters with proper encoding
        4. Handling edge cases (trailing slashes, empty paths)
        
        Args:
            base_url: Base URL of the API
            endpoint: Endpoint configuration
            params: Parameters containing path and query values
            
        Returns:
            Complete URL ready for the request
        """
        # Start with base URL and path
        path = endpoint.get("path", "/")
        # Ensure path starts with / for proper joining
        if not path.startswith("/"):
            path = "/" + path
        
        # Join base URL and path - ensure base_url ends without /
        base_url = base_url.rstrip("/")
        url = base_url + path
        
        # Replace path parameters
        for param in endpoint.get("parameters", []):
            if param.get("in") == "path":
                name = param.get("name", "")
                if name and name in params:
                    # Replace {param} with value
                    url = url.replace(f"{{{name}}}", str(params[name]))
        
        # Add query parameters
        query_params = {}
        for param in endpoint.get("parameters", []):
            if param.get("in") == "query":
                name = param.get("name", "")
                if name and name in params:
                    query_params[name] = params[name]
        
        if query_params:
            # Convert to query string
            query_string = urlencode(query_params)
            url = f"{url}?{query_string}"
        
        return url
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and transform to MCP format.
        
        Args:
            response: The requests Response object
            
        Returns:
            Standardized response dict
        """
        if response.status_code >= 200 and response.status_code < 300:
            try:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json() if response.text else None
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.text
                }
        else:
            # Error response
            error_detail = self.extract_error_detail(response)
            return {
                "success": False,
                "status_code": response.status_code,
                "error": error_detail,
                "headers": dict(response.headers)
            }
    
    def extract_error_detail(self, response: requests.Response) -> str:
        """Extract detailed error information from response.
        
        AI_CONTEXT: Error extraction is crucial for debugging. This method:
        1. Attempts to parse JSON error responses
        2. Looks for common error fields (message, error, detail)
        3. Handles nested error structures
        4. Falls back to text content if not JSON
        5. Provides meaningful defaults
        
        The goal is to give AI assistants enough information to
        understand and potentially fix the issue.
        
        Args:
            response: Failed response object
            
        Returns:
            Human-readable error message
        """
        try:
            error_data = response.json()
            
            # Common error message fields
            for field in ["message", "error", "detail", "error_description"]:
                if field in error_data:
                    return str(error_data[field])
            
            # If it's a dict with nested error
            if isinstance(error_data, dict) and "error" in error_data:
                if isinstance(error_data["error"], dict):
                    return json.dumps(error_data["error"])
            
            # Return full JSON if no specific field found
            return json.dumps(error_data)
            
        except json.JSONDecodeError:
            # Return text content if not JSON
            return response.text[:500] if response.text else f"HTTP {response.status_code}"