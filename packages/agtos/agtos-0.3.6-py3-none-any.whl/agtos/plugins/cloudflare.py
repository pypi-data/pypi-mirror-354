"""Cloudflare CLI wrapper plugin."""
import subprocess
import os
import json
from typing import Dict, List, Any

def safe_execute(func):
    """Decorator for safe execution with consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result}
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return {"success": False, "error": f"Command failed: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return wrapper

@safe_execute
def purge_cache(zone_id: str) -> Dict[str, Any]:
    """Purge all cached content for a Cloudflare zone.
    
    Args:
        zone_id: The Cloudflare zone ID
        
    Returns:
        Dict with success status and result
    """
    # Check if wrangler is installed
    if not subprocess.run(["which", "wrangler"], capture_output=True).returncode == 0:
        raise RuntimeError(
            "wrangler CLI not found. Install with: npm install -g wrangler"
        )
    
    # Ensure Cloudflare token is set
    if not os.environ.get("CLOUDFLARE_API_TOKEN"):
        raise ValueError(
            "CLOUDFLARE_API_TOKEN not set. Add with: agentctl key add cloudflare"
        )
    
    # Execute cache purge
    result = subprocess.run([
        "wrangler", "api",
        f"/zones/{zone_id}/purge_cache",
        "--json",
        "-X", "POST",
        "-d", '{"purge_everything": true}'
    ], capture_output=True, text=True, env=os.environ, check=True)
    
    # Parse response
    response = json.loads(result.stdout)
    
    return {
        "message": "Cache purged successfully",
        "zone_id": zone_id,
        "success": response.get("success", False),
        "errors": response.get("errors", [])
    }

@safe_execute
def list_zones() -> List[Dict[str, Any]]:
    """List all Cloudflare zones in your account.
    
    Returns:
        List of zone information
    """
    # Check requirements
    if not subprocess.run(["which", "wrangler"], capture_output=True).returncode == 0:
        raise RuntimeError(
            "wrangler CLI not found. Install with: npm install -g wrangler"
        )
    
    if not os.environ.get("CLOUDFLARE_API_TOKEN"):
        raise ValueError(
            "CLOUDFLARE_API_TOKEN not set. Add with: agentctl key add cloudflare"
        )
    
    # List zones
    result = subprocess.run([
        "wrangler", "api",
        "/zones",
        "--json"
    ], capture_output=True, text=True, env=os.environ, check=True)
    
    # Parse response
    response = json.loads(result.stdout)
    
    if not response.get("success"):
        raise RuntimeError(f"API request failed: {response.get('errors', [])}")
    
    zones = []
    for zone in response.get("result", []):
        zones.append({
            "id": zone["id"],
            "name": zone["name"],
            "status": zone["status"],
            "plan": zone["plan"]["name"]
        })
    
    return zones

@safe_execute
def create_dns_record(
    zone_id: str,
    record_type: str,
    name: str,
    content: str,
    proxied: bool = True
) -> Dict[str, Any]:
    """Create a DNS record in a Cloudflare zone.
    
    Args:
        zone_id: The zone ID
        record_type: Type of record (A, AAAA, CNAME, etc.)
        name: Record name (e.g., 'www')
        content: Record content (e.g., IP address)
        proxied: Whether to proxy through Cloudflare
        
    Returns:
        Created record information
    """
    if not os.environ.get("CLOUDFLARE_API_TOKEN"):
        raise ValueError(
            "CLOUDFLARE_API_TOKEN not set. Add with: agentctl key add cloudflare"
        )
    
    # Build request data
    data = {
        "type": record_type,
        "name": name,
        "content": content,
        "proxied": proxied
    }
    
    # Create DNS record
    result = subprocess.run([
        "wrangler", "api",
        f"/zones/{zone_id}/dns_records",
        "--json",
        "-X", "POST",
        "-d", json.dumps(data)
    ], capture_output=True, text=True, env=os.environ, check=True)
    
    response = json.loads(result.stdout)
    
    if not response.get("success"):
        raise RuntimeError(f"Failed to create DNS record: {response.get('errors', [])}")
    
    record = response.get("result", {})
    return {
        "id": record.get("id"),
        "type": record.get("type"),
        "name": record.get("name"),
        "content": record.get("content"),
        "proxied": record.get("proxied"),
        "created": True
    }

# Export tools for MCP
TOOLS = {
    "cloudflare.purge_cache": {
        "version": "1.0",
        "description": "Purge all cached content for a Cloudflare zone",
        "schema": {
            "type": "object",
            "properties": {
                "zone_id": {
                    "type": "string",
                    "description": "The Cloudflare zone ID (found in dashboard)"
                }
            },
            "required": ["zone_id"]
        },
        "func": purge_cache
    },
    "cloudflare.list_zones": {
        "version": "1.0",
        "description": "List all zones in your Cloudflare account",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": list_zones
    },
    "cloudflare.create_dns_record": {
        "version": "1.0",
        "description": "Create a DNS record in a Cloudflare zone",
        "schema": {
            "type": "object",
            "properties": {
                "zone_id": {
                    "type": "string",
                    "description": "The zone ID"
                },
                "record_type": {
                    "type": "string",
                    "description": "Record type (A, AAAA, CNAME, TXT, MX, etc.)",
                    "enum": ["A", "AAAA", "CNAME", "TXT", "MX", "SRV", "CAA"]
                },
                "name": {
                    "type": "string",
                    "description": "Record name (e.g., 'www' or '@' for root)"
                },
                "content": {
                    "type": "string",
                    "description": "Record content (e.g., IP address for A record)"
                },
                "proxied": {
                    "type": "boolean",
                    "description": "Whether to proxy through Cloudflare (orange cloud)",
                    "default": True
                }
            },
            "required": ["zone_id", "record_type", "name", "content"]
        },
        "func": create_dns_record
    }
}