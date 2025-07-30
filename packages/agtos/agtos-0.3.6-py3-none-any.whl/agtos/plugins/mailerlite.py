"""MailerLite REST API plugin."""
import requests
import os
from typing import Dict, List, Any, Optional

def safe_execute(func):
    """Decorator for safe execution with consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result}
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response else {}
            error_msg = error_data.get("message", str(e))
            return {"success": False, "error": f"API Error: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return wrapper

@safe_execute
def add_subscriber(
    email: str, 
    group_id: str, 
    name: str = "",
    fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Add a new subscriber to a MailerLite group.
    
    Args:
        email: Email address of the subscriber
        group_id: MailerLite group ID
        name: Subscriber name (optional)
        fields: Additional custom fields (optional)
        
    Returns:
        Created subscriber information
    """
    api_key = os.environ.get("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError(
            "MAILERLITE_API_KEY not set. Add with: agentctl key add mailerlite"
        )
    
    # Prepare request data
    data = {
        "email": email,
        "name": name,
        "fields": fields or {},
        "status": "active"
    }
    
    # Add subscriber to group
    response = requests.post(
        f"https://api.mailerlite.com/api/v2/groups/{group_id}/subscribers",
        json=data,
        headers={
            "X-MailerLite-ApiKey": api_key,
            "Content-Type": "application/json"
        }
    )
    
    response.raise_for_status()
    subscriber = response.json()
    
    return {
        "id": subscriber.get("id"),
        "email": subscriber.get("email"),
        "name": subscriber.get("name"),
        "status": subscriber.get("status"),
        "created_at": subscriber.get("date_created"),
        "group_id": group_id
    }

@safe_execute
def get_groups() -> List[Dict[str, Any]]:
    """List all MailerLite groups in your account.
    
    Returns:
        List of group information
    """
    api_key = os.environ.get("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError(
            "MAILERLITE_API_KEY not set. Add with: agentctl key add mailerlite"
        )
    
    response = requests.get(
        "https://api.mailerlite.com/api/v2/groups",
        headers={"X-MailerLite-ApiKey": api_key}
    )
    
    response.raise_for_status()
    groups = response.json()
    
    # Format group data
    formatted_groups = []
    for group in groups:
        formatted_groups.append({
            "id": group.get("id"),
            "name": group.get("name"),
            "active_count": group.get("active_count", 0),
            "total_count": group.get("total_count", 0),
            "created_at": group.get("date_created")
        })
    
    return formatted_groups

@safe_execute
def create_campaign(
    subject: str,
    group_ids: List[str],
    html_content: str,
    from_name: str,
    from_email: str,
    plain_text: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new email campaign.
    
    Args:
        subject: Email subject line
        group_ids: List of group IDs to send to
        html_content: HTML content of the email
        from_name: Sender name
        from_email: Sender email address
        plain_text: Plain text version (optional)
        
    Returns:
        Created campaign information
    """
    api_key = os.environ.get("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError(
            "MAILERLITE_API_KEY not set. Add with: agentctl key add mailerlite"
        )
    
    # Auto-generate plain text if not provided
    if not plain_text:
        # Simple HTML to text conversion
        import re
        plain_text = re.sub('<[^<]+?>', '', html_content)
    
    # Create campaign
    data = {
        "type": "regular",
        "subject": subject,
        "from": from_email,
        "from_name": from_name,
        "groups": group_ids,
        "content": {
            "html": html_content,
            "plain": plain_text
        }
    }
    
    response = requests.post(
        "https://api.mailerlite.com/api/v2/campaigns",
        json=data,
        headers={
            "X-MailerLite-ApiKey": api_key,
            "Content-Type": "application/json"
        }
    )
    
    response.raise_for_status()
    campaign = response.json()
    
    return {
        "id": campaign.get("id"),
        "name": campaign.get("name"),
        "subject": campaign.get("subject"),
        "status": campaign.get("status"),
        "created_at": campaign.get("date_created"),
        "recipient_count": len(group_ids)
    }

@safe_execute
def get_subscriber_count() -> Dict[str, int]:
    """Get total subscriber counts across all groups.
    
    Returns:
        Subscriber statistics
    """
    api_key = os.environ.get("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError(
            "MAILERLITE_API_KEY not set. Add with: agentctl key add mailerlite"
        )
    
    # Get account stats
    response = requests.get(
        "https://api.mailerlite.com/api/v2/stats",
        headers={"X-MailerLite-ApiKey": api_key}
    )
    
    response.raise_for_status()
    stats = response.json()
    
    return {
        "total": stats.get("subscribed", 0) + stats.get("unsubscribed", 0),
        "active": stats.get("subscribed", 0),
        "unsubscribed": stats.get("unsubscribed", 0),
        "bounced": stats.get("bounced", 0),
        "junk": stats.get("junk", 0)
    }

# Export tools for MCP
TOOLS = {
    "mailerlite.add_subscriber": {
        "version": "1.0",
        "description": "Add a new subscriber to a MailerLite group",
        "schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Email address of the subscriber",
                    "format": "email"
                },
                "group_id": {
                    "type": "string",
                    "description": "MailerLite group ID (get with mailerlite.get_groups)"
                },
                "name": {
                    "type": "string",
                    "description": "Subscriber's full name (optional)",
                    "default": ""
                },
                "fields": {
                    "type": "object",
                    "description": "Custom fields as key-value pairs (optional)",
                    "default": {}
                }
            },
            "required": ["email", "group_id"]
        },
        "func": add_subscriber
    },
    "mailerlite.get_groups": {
        "version": "1.0",
        "description": "Get all MailerLite groups in your account",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": get_groups
    },
    "mailerlite.create_campaign": {
        "version": "1.0",
        "description": "Create a new email campaign (draft status)",
        "schema": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "Email subject line"
                },
                "group_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of group IDs to send to"
                },
                "html_content": {
                    "type": "string",
                    "description": "HTML content of the email"
                },
                "from_name": {
                    "type": "string",
                    "description": "Sender name"
                },
                "from_email": {
                    "type": "string",
                    "description": "Sender email address",
                    "format": "email"
                },
                "plain_text": {
                    "type": "string",
                    "description": "Plain text version (auto-generated if not provided)",
                    "default": None
                }
            },
            "required": ["subject", "group_ids", "html_content", "from_name", "from_email"]
        },
        "func": create_campaign
    },
    "mailerlite.get_subscriber_count": {
        "version": "1.0",
        "description": "Get total subscriber statistics across all groups",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": get_subscriber_count
    }
}