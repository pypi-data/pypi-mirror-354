"""
PURPOSE: Diagnostic and status commands for agentctl
This module provides system health checks and status monitoring for
debugging and troubleshooting.

AI_CONTEXT: The doctor command performs comprehensive health checks while
the status command shows active MCP servers. Both are essential for
troubleshooting issues and understanding system state.
"""

import os
import sys
import subprocess
import shutil
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..config import Config

# Optional import for psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
from ..providers import get_provider
from ..project_store import ProjectStore

console = Console()


def register_diagnostic_commands(app: typer.Typer) -> None:
    """
    AI_CONTEXT: Registers diagnostic commands with the main app.
    Includes doctor for health checks, status for process monitoring,
    and mcp-server for running the Meta-MCP server.
    """
    app.command()(doctor)
    app.command()(status)
    app.command(name="mcp-server")(mcp_server)


def doctor() -> None:
    """Run system diagnostics and health checks."""
    console.print(Panel("🩺 Running agentctl diagnostics...", style="cyan"))
    
    # Collect all diagnostic results
    results = {
        "System": check_system(),
        "Dependencies": check_dependencies(),
        "Configuration": check_configuration(),
        "Projects": check_projects(),
        "Credentials": check_credentials(),
        "MCP": check_mcp_setup(),
    }
    
    # Display results
    display_diagnostic_results(results)
    
    # Summary
    display_diagnostic_summary(results)


def status() -> None:
    """Show status of active MCP servers and Claude Code configuration."""
    console.print(Panel("📊 Checking agentctl status...", style="cyan"))
    
    # Find MCP server processes
    mcp_processes = find_mcp_processes()
    
    if not mcp_processes:
        console.print("[yellow]No active MCP servers found[/yellow]")
        console.print("\nStart a server with: [cyan]agentctl mcp-server[/cyan]")
        return
    
    # Display active servers
    display_active_servers(mcp_processes)
    
    # Check Claude Code configuration
    check_claude_status()


def check_system() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks system-level requirements.
    Returns list of (check_name, passed, message) tuples.
    """
    checks = []
    
    # OS Check
    is_macos = sys.platform == "darwin"
    checks.append((
        "Operating System",
        is_macos,
        "macOS" if is_macos else f"Unsupported: {sys.platform}"
    ))
    
    # Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 12)
    checks.append((
        "Python Version",
        py_ok,
        py_version if py_ok else f"{py_version} (requires 3.12+)"
    ))
    
    # Home directory
    home_ok = Path.home().exists()
    checks.append((
        "Home Directory",
        home_ok,
        str(Path.home()) if home_ok else "Not found"
    ))
    
    return checks


def check_dependencies() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks required external dependencies.
    Verifies Claude Code configuration and command-line tools.
    """
    checks = []
    
    # Claude Code configuration
    claude_config_path = Path.home() / ".claude.json"
    claude_ok = claude_config_path.exists()
    checks.append((
        "Claude Code Configuration",
        claude_ok,
        "Configured" if claude_ok else "Not configured - run 'agtos claude-setup'"
    ))
    
    # Poetry - check both PATH and common installation locations
    poetry_ok = shutil.which("poetry") is not None
    if not poetry_ok:
        # Check common pipx installation location
        poetry_path = Path.home() / ".local" / "bin" / "poetry"
        poetry_ok = poetry_path.exists()
    
    checks.append((
        "Poetry",
        poetry_ok,
        "Installed" if poetry_ok else "Not found - install from python-poetry.org"
    ))
    
    # Git
    git_ok = shutil.which("git") is not None
    checks.append((
        "Git",
        git_ok,
        "Installed" if git_ok else "Not found"
    ))
    
    # 1Password CLI (optional)
    op_ok = shutil.which("op") is not None
    checks.append((
        "1Password CLI",
        True,  # Optional, so always "pass"
        "Installed" if op_ok else "Not installed (optional)"
    ))
    
    return checks


def check_configuration() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks agentctl configuration.
    Verifies config file and settings.
    """
    checks = []
    
    # Config directory
    config_dir = Path.home() / ".agtos"
    config_ok = config_dir.exists()
    checks.append((
        "Config Directory",
        config_ok,
        str(config_dir) if config_ok else "Not found"
    ))
    
    # Config file
    try:
        config = Config()
        config_ok = True
        provider = config.get("credential_provider") or "Not set"
    except Exception as e:
        config_ok = False
        provider = f"Error: {e}"
    
    checks.append((
        "Configuration",
        config_ok,
        f"Provider: {provider}" if config_ok else provider
    ))
    
    return checks


def check_projects() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks project configuration.
    Verifies project store and registered projects.
    """
    checks = []
    
    try:
        store = ProjectStore()  # Constructor takes no arguments
        projects = store.list_projects()  # Returns dict, not list
        
        if projects:
            # Check each project path - projects is a dict where values have 'path' key
            valid_count = sum(1 for slug, data in projects.items() if Path(data["path"]).exists())
            checks.append((
                "Projects",
                True,
                f"{len(projects)} registered, {valid_count} valid paths"
            ))
        else:
            checks.append((
                "Projects",
                True,  # Not an error to have no projects
                "No projects registered"
            ))
    except Exception as e:
        checks.append((
            "Projects",
            False,
            f"Error: {e}"
        ))
    
    return checks


def check_credentials() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks credential provider functionality.
    Tests if credentials can be accessed.
    """
    checks = []
    
    try:
        provider = get_provider()
        services = provider.list_services()
        
        checks.append((
            "Credential Provider",
            True,
            f"{len(services)} credentials stored" if services else "No credentials stored"
        ))
    except Exception as e:
        checks.append((
            "Credential Provider",
            False,
            f"Error: {e}"
        ))
    
    return checks


def check_mcp_setup() -> List[Tuple[str, bool, str]]:
    """
    AI_CONTEXT: Checks MCP-related setup.
    Verifies MCP server can be started.
    """
    checks = []
    
    # Check if mcp_server module exists
    try:
        from .. import mcp_server
        mcp_ok = True
        mcp_msg = "Module loaded"
    except ImportError as e:
        mcp_ok = False
        mcp_msg = f"Import error: {e}"
    
    checks.append(("MCP Server Module", mcp_ok, mcp_msg))
    
    return checks


def display_diagnostic_results(results: Dict[str, List[Tuple[str, bool, str]]]) -> None:
    """
    AI_CONTEXT: Displays diagnostic results in a formatted table.
    Shows each category with pass/fail status.
    """
    for category, checks in results.items():
        table = Table(title=f"{category} Checks", show_header=False)
        table.add_column("Check", style="cyan", width=25)
        table.add_column("Status", style="green", width=8)
        table.add_column("Details", style="white")
        
        for check_name, passed, message in checks:
            status = "[green]✓ Pass[/green]" if passed else "[red]✗ Fail[/red]"
            table.add_row(check_name, status, message)
        
        console.print(table)
        console.print()


def display_diagnostic_summary(results: Dict[str, List[Tuple[str, bool, str]]]) -> None:
    """
    AI_CONTEXT: Shows overall diagnostic summary.
    Provides actionable next steps if issues found.
    """
    # Count failures
    total_checks = 0
    failed_checks = 0
    
    for checks in results.values():
        for _, passed, _ in checks:
            total_checks += 1
            if not passed:
                failed_checks += 1
    
    if failed_checks == 0:
        console.print(Panel(
            "[green]✓ All checks passed![/green]\n\nYour agentctl installation is healthy.",
            title="Diagnostics Complete",
            style="green"
        ))
    else:
        message = f"[yellow]⚠ {failed_checks} check(s) failed[/yellow]\n\n"
        message += "Please address the issues above.\n"
        message += "Run [cyan]agentctl doctor[/cyan] again after fixing."
        
        console.print(Panel(message, title="Diagnostics Complete", style="yellow"))


def find_mcp_processes() -> List[Dict[str, Any]]:
    """
    AI_CONTEXT: Finds running MCP server processes.
    Returns process information for display.
    """
    mcp_processes = []
    
    if not HAS_PSUTIL:
        # Fallback method using ps command
        try:
            result = subprocess.run(
                ['ps', 'aux'], 
                capture_output=True, 
                text=True,
                check=True
            )
            for line in result.stdout.split('\n'):
                if 'agtos' in line and 'mcp-server' in line:
                    parts = line.split(None, 10)
                    if len(parts) > 10:
                        mcp_processes.append({
                            'pid': parts[1],
                            'name': 'agtos',
                            'cmdline': parts[10],
                            'uptime': 0  # Can't easily get uptime without psutil
                        })
        except:
            # If ps command fails, return empty list
            pass
    else:
        # Use psutil if available
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('agtos' in arg and 'mcp-server' in arg for arg in cmdline):
                    mcp_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': ' '.join(cmdline),
                        'uptime': time.time() - proc.info['create_time']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    return mcp_processes


def display_active_servers(processes: List[Dict[str, Any]]) -> None:
    """
    AI_CONTEXT: Displays active MCP server processes.
    Shows PID, uptime, and command details.
    """
    table = Table(title="Active MCP Servers")
    table.add_column("PID", style="cyan")
    table.add_column("Uptime", style="green")
    table.add_column("Command", style="white")
    
    for proc in processes:
        uptime = format_uptime(proc['uptime'])
        cmd = proc['cmdline']
        if len(cmd) > 60:
            cmd = cmd[:57] + "..."
        table.add_row(str(proc['pid']), uptime, cmd)
    
    console.print(table)


def check_claude_status() -> None:
    """
    AI_CONTEXT: Checks Claude Code configuration status.
    Verifies if agentctl is configured as an MCP server.
    """
    try:
        # Check if Claude Code is configured
        claude_config_path = Path.home() / ".claude.json"
        
        if claude_config_path.exists():
            with open(claude_config_path, 'r') as f:
                config = json.load(f)
                mcp_servers = config.get("mcpServers", {})
                
                if "agtos" in mcp_servers:
                    console.print("\n[green]✓[/green] agentctl is configured in Claude Code")
                    server_config = mcp_servers["agtos"]
                    if "args" in server_config and "--port" in server_config["args"]:
                        port_idx = server_config["args"].index("--port")
                        if port_idx + 1 < len(server_config["args"]):
                            port = server_config["args"][port_idx + 1]
                            console.print(f"  Port: {port}")
                else:
                    console.print("\n[yellow]○[/yellow] agentctl not configured in Claude Code")
                    console.print("  Run: [cyan]agentctl claude-setup[/cyan]")
        else:
            console.print("\n[yellow]○[/yellow] Claude Code not configured")
            console.print("  Run: [cyan]agentctl claude-setup[/cyan] to configure")
            
    except Exception as e:
        # Error reading config
        console.print(f"\n[yellow]?[/yellow] Could not check Claude Code configuration: {e}")


def format_uptime(seconds: float) -> str:
    """
    AI_CONTEXT: Formats uptime in human-readable format.
    Converts seconds to hours/minutes/seconds.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def mcp_server(
    port: int = typer.Option(8585, "--port", "-p", help="Port to run the Meta-MCP server on"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging"),
    log_file: Optional[str] = typer.Option(None, "--log-file", "-l", help="Log output to file"),
    log_requests: bool = typer.Option(False, "--log-requests", help="Log all MCP requests/responses")
) -> None:
    """
    Start the Meta-MCP server that aggregates all agentctl tools.
    
    AI_CONTEXT: This command starts the Meta-MCP server which acts as a
    proxy/aggregator for all agentctl tools. It's what Claude Code connects to.
    """
    console.print(Panel.fit(
        "[bold cyan]Starting agentctl Meta-MCP Server[/bold cyan]\n"
        f"Port: {port}\n"
        f"Debug: {'Enabled' if debug else 'Disabled'}\n"
        f"Request Logging: {'Enabled' if log_requests else 'Disabled'}\n"
        f"Log File: {log_file or 'None'}\n"
        "Press Ctrl+C to stop",
        border_style="cyan"
    ))
    
    try:
        # Start the metamcp server
        from ..metamcp.server import MetaMCPServer
        import asyncio
        
        # Configure logging
        import logging
        from rich.logging import RichHandler
        
        # Set up logging level
        log_level = logging.DEBUG if debug else logging.INFO
        
        # Configure handlers
        handlers = []
        
        # Console handler with Rich formatting
        console_handler = RichHandler(console=console, show_time=True, show_path=False)
        console_handler.setLevel(log_level)
        handlers.append(console_handler)
        
        # File handler if specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)  # Always debug level for file
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            handlers.append(file_handler)
            console.print(f"[green]✓[/green] Logging to file: {log_path}")
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            handlers=handlers,
            force=True  # Override any existing configuration
        )
        
        # Create and run the server
        console.print(f"\n[green]✓[/green] Server starting on port {port}...")
        console.print("[dim]Check http://localhost:{}/health for status[/dim]\n".format(port))
        
        async def run():
            # Create server config with debugging options
            config = {
                "debug": debug,
                "log_requests": log_requests
            }
            
            server = MetaMCPServer(config)
            
            # Pre-discover services at startup
            console.print("\n[green]Discovering services...[/green]")
            await server._discover_services()
            
            # Show discovered services
            service_count = len(server.registry.services)
            if service_count > 0:
                console.print(f"[green]✓[/green] Discovered {service_count} services:")
                for service_name, service_info in server.registry.services.items():
                    tool_count = len(service_info.tools)
                    console.print(f"  - {service_name}: {tool_count} tools")
            else:
                console.print("[yellow]⚠[/yellow] No services discovered")
            
            console.print("")
            await server.start(host="0.0.0.0", port=port)
        
        asyncio.run(run())
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error starting server:[/red] {e}")
        if debug:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)


def register_diagnostic_commands(app: typer.Typer):
    """
    Register diagnostic commands with the main CLI app.
    
    AI_CONTEXT: Registers the doctor, status, and mcp-server commands.
    Called from cli/__init__.py during app initialization.
    """
    app.command(name="doctor")(doctor)
    app.command(name="status")(status) 
    app.command(name="mcp-server")(mcp_server)