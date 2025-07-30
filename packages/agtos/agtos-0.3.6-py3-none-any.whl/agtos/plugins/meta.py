"""Meta-plugin for controlling agentctl through natural language."""
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import yaml

def safe_execute(func):
    """Decorator for safe execution with consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return wrapper

@safe_execute
def list_projects() -> List[Dict[str, Any]]:
    """List all registered projects.
    
    Returns:
        List of project information
    """
    config_file = Path.home() / ".agtos" / "projects.yml"
    
    if not config_file.exists():
        return []
    
    with open(config_file) as f:
        config = yaml.safe_load(f) or {"projects": {}}
    
    projects = []
    for slug, info in config["projects"].items():
        projects.append({
            "slug": slug,
            "path": info["path"],
            "agent": info["agent"],
            "exists": Path(info["path"]).exists()
        })
    
    return projects

@safe_execute
def add_project(slug: str, path: str, agent: str = "claude") -> Dict[str, str]:
    """Add a new project to agtos.
    
    Args:
        slug: Short name for the project
        path: Full path to project directory
        agent: Which AI agent to use (claude or codex)
        
    Returns:
        Confirmation of project addition
    """
    # Expand path
    project_path = Path(path).expanduser().absolute()
    
    # Validate path exists
    if not project_path.exists():
        project_path.mkdir(parents=True, exist_ok=True)
    
    # Run agentctl add command
    result = subprocess.run(
        ["agtos", "add", slug, str(project_path), "--agent", agent],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to add project: {result.stderr}")
    
    return {
        "message": f"Added project '{slug}' at {project_path}",
        "slug": slug,
        "path": str(project_path),
        "agent": agent
    }

@safe_execute
def list_stored_keys() -> List[str]:
    """List all stored API keys/services.
    
    Returns:
        List of service names with stored credentials
    """
    result = subprocess.run(
        ["agtos", "key", "ls"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return []
    
    # Parse output to extract service names
    services = []
    for line in result.stdout.strip().split('\n'):
        if line.strip().startswith('- '):
            service = line.strip()[2:].strip()
            services.append(service)
    
    return services

@safe_execute
def add_api_key(service: str, api_key: Optional[str] = None) -> Dict[str, str]:
    """Add or update an API key for a service.
    
    Args:
        service: Service name (e.g., 'cloudflare', 'openai')
        api_key: The API key value (will prompt if not provided)
        
    Returns:
        Confirmation message
    """
    if api_key:
        # Use echo to pipe the key to avoid exposing in process list
        process = subprocess.Popen(
            ["agtos", "key", "add", service],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=api_key)
        
        if process.returncode != 0:
            raise RuntimeError(f"Failed to add key: {stderr}")
    else:
        # Interactive mode - let agentctl prompt
        result = subprocess.run(
            ["agtos", "key", "add", service],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to add key: {result.stderr}")
    
    return {
        "message": f"Successfully stored API key for {service}",
        "service": service
    }

@safe_execute
def create_plugin(service: str, plugin_type: str = "rest") -> Dict[str, Any]:
    """Scaffold a new plugin for a service.
    
    Args:
        service: Name of the service
        plugin_type: Type of plugin ('cli' or 'rest')
        
    Returns:
        Information about created plugin
    """
    # Determine the flag
    flag = "--cli" if plugin_type.lower() == "cli" else "--rest"
    
    # Run integrate command
    result = subprocess.run(
        ["agtos", "integrate", service, flag],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent  # Run from agtos root
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create plugin: {result.stderr}")
    
    plugin_path = Path(__file__).parent / f"{service}.py"
    
    return {
        "message": f"Created {plugin_type} plugin for {service}",
        "path": str(plugin_path),
        "service": service,
        "type": plugin_type,
        "next_steps": [
            f"Edit {plugin_path} to implement functionality",
            "Update the tool descriptions and schemas",
            "Test with 'agtos run' and natural language"
        ]
    }

@safe_execute
def get_credential_provider() -> Dict[str, str]:
    """Get current credential provider information.
    
    Returns:
        Current provider details
    """
    provider_name = os.getenv("AGTOS_CRED_PROVIDER", "keychain")
    
    provider_info = {
        "keychain": {
            "name": "macOS Keychain",
            "security": "medium",
            "description": "Built-in macOS credential storage"
        },
        "1password": {
            "name": "1Password",
            "security": "high",
            "description": "1Password CLI integration"
        },
        "env": {
            "name": "Environment Variables",
            "security": "development",
            "description": "File-based storage for development"
        }
    }
    
    info = provider_info.get(provider_name, provider_info["keychain"])
    info["current"] = provider_name
    
    return info

@safe_execute
def change_credential_provider(provider: str) -> Dict[str, str]:
    """Change the credential provider.
    
    Args:
        provider: Provider name ('keychain', '1password', or 'env')
        
    Returns:
        Confirmation and instructions
    """
    valid_providers = ["keychain", "1password", "env"]
    
    if provider.lower() not in valid_providers:
        raise ValueError(f"Invalid provider. Choose from: {', '.join(valid_providers)}")
    
    # Test if provider works
    result = subprocess.run(
        ["agtos", "cred-provider", "set", provider],
        capture_output=True,
        text=True,
        env={**os.environ, "AGTOS_CRED_PROVIDER": provider}
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to set provider: {result.stderr}")
    
    shell_rc = ".zshrc" if os.path.exists(Path.home() / ".zshrc") else ".bashrc"
    
    return {
        "message": f"Credential provider set to {provider}",
        "provider": provider,
        "instructions": f"To make permanent, add to ~/{shell_rc}:\nexport AGTOS_CRED_PROVIDER={provider}"
    }

@safe_execute
def doctor() -> Dict[str, Any]:
    """Run diagnostics to check agentctl health.
    
    Returns:
        System status information
    """
    status = {
        "prerequisites": {},
        "credentials": {},
        "projects": {},
        "plugins": {}
    }
    
    # Check CLI tools
    for tool in ["claude", "codex", "wrangler", "npm", "poetry"]:
        result = subprocess.run(["which", tool], capture_output=True)
        status["prerequisites"][tool] = result.returncode == 0
    
    # Check credential provider
    provider = get_credential_provider()
    status["credentials"]["provider"] = provider["current"]
    status["credentials"]["security_level"] = provider["security"]
    
    # Count stored keys
    try:
        keys = list_stored_keys()
        status["credentials"]["stored_keys"] = len(keys)
        status["credentials"]["services"] = keys
    except:
        status["credentials"]["stored_keys"] = 0
        status["credentials"]["services"] = []
    
    # Count projects
    try:
        projects = list_projects()
        status["projects"]["count"] = len(projects)
        status["projects"]["list"] = [p["slug"] for p in projects]
    except:
        status["projects"]["count"] = 0
        status["projects"]["list"] = []
    
    # Count plugins
    plugin_dir = Path(__file__).parent
    plugin_files = list(plugin_dir.glob("*.py"))
    plugin_names = [f.stem for f in plugin_files if not f.stem.startswith("_")]
    status["plugins"]["count"] = len(plugin_names)
    status["plugins"]["list"] = plugin_names
    
    return status

# Export tools for MCP
TOOLS = {
    "agtos.list_projects": {
        "version": "1.0",
        "description": "List all projects registered with agtos",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": list_projects
    },
    "agtos.add_project": {
        "version": "1.0",
        "description": "Add a new project to agtos",
        "schema": {
            "type": "object",
            "properties": {
                "slug": {
                    "type": "string",
                    "description": "Short name for the project (letters, numbers, hyphens)"
                },
                "path": {
                    "type": "string",
                    "description": "Path to project directory (can use ~ for home)"
                },
                "agent": {
                    "type": "string",
                    "description": "Which AI agent to use",
                    "enum": ["claude", "codex"],
                    "default": "claude"
                }
            },
            "required": ["slug", "path"]
        },
        "func": add_project
    },
    "agtos.list_keys": {
        "version": "1.0",
        "description": "List all stored API keys/services",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": list_stored_keys
    },
    "agtos.add_key": {
        "version": "1.0",
        "description": "Add or update an API key for a service",
        "schema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service name (e.g., 'cloudflare', 'openai', 'stripe')"
                },
                "api_key": {
                    "type": "string",
                    "description": "The API key value (omit to prompt interactively)",
                    "default": None
                }
            },
            "required": ["service"]
        },
        "func": add_api_key
    },
    "agtos.create_plugin": {
        "version": "1.0",
        "description": "Scaffold a new plugin for a service",
        "schema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Name of the service to integrate"
                },
                "plugin_type": {
                    "type": "string",
                    "description": "Type of integration",
                    "enum": ["cli", "rest"],
                    "default": "rest"
                }
            },
            "required": ["service"]
        },
        "func": create_plugin
    },
    "agtos.get_credential_provider": {
        "version": "1.0",
        "description": "Get information about the current credential storage provider",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": get_credential_provider
    },
    "agtos.change_credential_provider": {
        "version": "1.0",
        "description": "Change the credential storage provider",
        "schema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Provider to use",
                    "enum": ["keychain", "1password", "env"]
                }
            },
            "required": ["provider"]
        },
        "func": change_credential_provider
    },
    "agtos.doctor": {
        "version": "1.0",
        "description": "Run diagnostics to check agentctl system health",
        "schema": {
            "type": "object",
            "properties": {}
        },
        "func": doctor
    }
}