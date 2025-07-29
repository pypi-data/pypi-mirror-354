"""Terminal User Interface (TUI) for agtOS.

This module provides an interactive terminal interface for agtOS that allows
users to perform administrative tasks and launch the orchestrator agent.

AI_CONTEXT:
    The TUI is the main interface users see after running 'agtos'. It provides:
    - Quick administrative actions (project switching, credential management)
    - Launch point for AI orchestrator (Claude)
    - Status monitoring and cost tracking
    - An alternative to memorizing CLI commands
    
    Users can either use the TUI for quick tasks or launch Claude for complex work.

Future Command Ideas:
    Agent Management:
    - View agent capabilities
    - Set cost limits per agent
    - View usage history
    - Configure agent preferences
    - Test agent connectivity
    
    Tool Management:
    - Search tools by capability
    - View tool documentation
    - Test tool execution
    - Create custom tool
    - Import/export tools
    
    Monitoring:
    - Real-time log viewer
    - Performance metrics
    - Error diagnostics
    - Network traffic monitor
    - Resource usage
    
    Workflow:
    - Create workflow from history
    - Schedule workflow execution
    - Workflow marketplace
    - Share workflows
    
    Settings:
    - Theme customization
    - Keyboard shortcuts
    - Notification preferences
    - Auto-update settings
    - Backup/restore config
"""

import asyncio
import sys
import json
import subprocess
import os
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from pathlib import Path
from packaging import version

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window, FormattedTextControl
from prompt_toolkit.layout.containers import Container
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.filters import Condition

from .agents import AgentRegistry
from .project_store import ProjectStore
from .config import get_config_dir
from .providers import get_provider
from .workflows.library import WorkflowLibrary
from .utils import get_logger
from .orchestration.engine import OrchestrationEngine
from .auth import AuthManager

logger = get_logger(__name__)


class MenuItem:
    """Represents a menu item in the TUI."""
    
    def __init__(
        self, 
        label: str, 
        action: Optional[Callable] = None,
        submenu: Optional[List['MenuItem']] = None,
        cost_info: Optional[str] = None,
        separator: bool = False
    ):
        self.label = label
        self.action = action
        self.submenu = submenu
        self.cost_info = cost_info
        self.separator = separator


class AgtOSTUI:
    """Interactive Terminal User Interface for agtOS.
    
    AI_CONTEXT:
        This TUI provides a user-friendly interface for agtOS operations.
        It's designed to be intuitive with keyboard navigation and search.
        The TUI complements the AI orchestrator by handling quick admin tasks.
    """
    
    def __init__(self):
        """Initialize the TUI components."""
        self.selected_index = 0
        self.search_query = ""
        self.current_menu: List[MenuItem] = []
        self.menu_stack: List[List[MenuItem]] = []
        self.status_message = ""
        
        # Initialize components
        self.agent_registry = AgentRegistry()
        self.project_store = ProjectStore()
        self.workflow_library = WorkflowLibrary()
        self.provider = get_provider()
        self.auth_manager = AuthManager()
        
        # Check authentication
        self.current_user = None
        self.needs_auth = False
        
        # Load update preferences
        self.update_preferences = self._load_update_preferences()
        self.pending_update = None
        
        # Check authentication before building menu
        self._check_authentication()
        
        # Build main menu
        self.main_menu = self._build_main_menu()
        self.current_menu = self.main_menu
        
        # Create application
        self.app = self._create_application()
        
        # Check for updates on startup if enabled
        if self.update_preferences.get("check_on_startup", True):
            self._check_updates_startup()
    
    def _build_main_menu(self) -> List[MenuItem]:
        """Build the main menu structure."""
        # Get agent costs
        claude_cost = "$0.25/1K tokens"  # Example, would fetch real costs
        codex_cost = "$0.02/1K tokens"
        
        return [
            MenuItem("Open Claude (Orchestrator)", self._open_claude, cost_info=claude_cost),
            MenuItem("Select Primary Agent", submenu=self._build_agent_menu()),
            MenuItem("", separator=True),
            MenuItem("Browse Workflows", self._browse_workflows),
            MenuItem("Manage Projects", submenu=self._build_project_menu()),
            MenuItem("Configure Credentials", submenu=self._build_credential_menu()),
            MenuItem("", separator=True),
            MenuItem("View Agent Costs", self._view_agent_costs),
            MenuItem("Server Status", self._show_server_status),
            MenuItem("Check for Updates", self._check_updates),
            MenuItem("Help & Documentation", self._show_help),
        ]
    
    def _build_agent_menu(self) -> List[MenuItem]:
        """Build the agent selection submenu."""
        agents = self.agent_registry.get_available_agents()
        menu_items = []
        
        for agent in agents:
            cost_info = self._get_agent_cost_info(agent.name)
            menu_items.append(
                MenuItem(
                    f"{agent.name} - {agent.description}",
                    lambda a=agent: self._select_agent(a),
                    cost_info=cost_info
                )
            )
        
        return menu_items
    
    def _build_project_menu(self) -> List[MenuItem]:
        """Build the project management submenu."""
        return [
            MenuItem("Select Project", self._select_project),
            MenuItem("Create Project", self._create_project),
            MenuItem("List Projects", self._list_projects),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ]
    
    def _build_credential_menu(self) -> List[MenuItem]:
        """Build the credential management submenu."""
        return [
            MenuItem("Add API Key", self._add_api_key),
            MenuItem("Update Credential", self._update_credential),
            MenuItem("List Credentials", self._list_credentials),
            MenuItem("Test Connection", self._test_credential),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ]
    
    def _create_application(self) -> Application:
        """Create the prompt_toolkit application."""
        # Key bindings
        kb = KeyBindings()
        
        @kb.add('up')
        def move_up(event):
            self._move_selection(-1)
        
        @kb.add('down')
        def move_down(event):
            self._move_selection(1)
        
        @kb.add('enter')
        def select_item(event):
            self._execute_selected()
        
        @kb.add('escape')
        def go_back(event):
            self._go_back()
        
        @kb.add('/')
        def start_search(event):
            # TODO: Implement search focus
            pass
        
        @kb.add('c-c')
        def exit_app(event):
            event.app.exit()
        
        # Create layout
        layout = Layout(self._create_main_container())
        
        # Style
        style = Style.from_dict({
            'title': '#00ff00 bold',
            'status': '#888888',
            'selected': 'reverse',
            'separator': '#444444',
            'cost': '#ffaa00',
            'header': '#00aaff',
        })
        
        return Application(
            layout=layout,
            key_bindings=kb,
            style=style,
            full_screen=True,
            mouse_support=True,
        )
    
    def _create_main_container(self) -> Container:
        """Create the main container with all UI elements."""
        # ASCII art title
        title_text = """
                    ▄▀█ █▀▀ ▀█▀ █▀█ █▀
                    █▀█ █▄█  █  █▄█ ▄█
                    
                  Agent Operating System v0.3.2 (Beta)
        """
        
        # Status bar
        status = self._get_status_text()
        
        # Menu content
        menu_content = self._render_menu()
        
        # Build layout
        return HSplit([
            # Title section
            Window(
                FormattedTextControl(
                    FormattedText([('class:title', title_text)])
                ),
                height=7,
                align='center'
            ),
            # Status bar
            Window(
                FormattedTextControl(
                    FormattedText([('class:status', status)])
                ),
                height=1,
                style='class:status reverse'
            ),
            # Main menu area
            Window(
                FormattedTextControl(
                    text=menu_content,
                    focusable=True,
                ),
                wrap_lines=True,
            ),
            # Bottom help text
            Window(
                FormattedTextControl(
                    FormattedText([
                        ('', '  '),
                        ('class:header', 'Type to search...'),
                        ('', '                    '),
                        ('class:status', 'ESC: Back  ↑↓: Navigate  Enter: Select  Ctrl+C: Quit')
                    ])
                ),
                height=2,
            ),
        ])
    
    def _get_status_text(self) -> str:
        """Get the status bar text."""
        agents = len(self.agent_registry.get_available_agents())
        # In real implementation, would get actual tool count
        tools = 87
        
        # Check if server is running
        server_status = "● Active"  # Would check actual status
        
        return f"  Status: {server_status}    Agents: {agents}    Tools: {tools}     "
    
    def _render_menu(self) -> FormattedText:
        """Render the current menu as formatted text."""
        lines = []
        
        # Header
        lines.append(('', '\n'))
        lines.append(('', '  Select an action (↑↓ to navigate, Enter to select):\n'))
        lines.append(('', '\n'))
        
        # Filter menu items if searching
        visible_items = self._filter_menu_items()
        
        # Render each menu item
        for i, item in enumerate(visible_items):
            if item.separator:
                lines.append(('class:separator', '    ──────────────────────────────────────\n'))
            else:
                # Selection indicator
                if i == self.selected_index:
                    lines.append(('class:selected', '  > '))
                else:
                    lines.append(('', '    '))
                
                # Menu label
                lines.append(('class:selected' if i == self.selected_index else '', item.label))
                
                # Cost info if available
                if item.cost_info:
                    padding = 40 - len(item.label)
                    lines.append(('', ' ' * max(1, padding)))
                    lines.append(('class:cost', f'[{item.cost_info}]'))
                
                lines.append(('', '\n'))
        
        lines.append(('', '\n'))
        
        # Status message if any
        if self.status_message:
            lines.append(('class:header', f'  {self.status_message}\n'))
        
        return FormattedText(lines)
    
    def _filter_menu_items(self) -> List[MenuItem]:
        """Filter menu items based on search query."""
        if not self.search_query:
            return self.current_menu
        
        # Simple case-insensitive search
        query = self.search_query.lower()
        return [
            item for item in self.current_menu
            if query in item.label.lower() or item.separator
        ]
    
    def _move_selection(self, direction: int):
        """Move the selection up or down."""
        visible_items = [i for i in self._filter_menu_items() if not i.separator]
        if not visible_items:
            return
        
        max_index = len(visible_items) - 1
        self.selected_index = max(0, min(max_index, self.selected_index + direction))
    
    def _execute_selected(self):
        """Execute the selected menu item."""
        visible_items = [i for i in self._filter_menu_items() if not i.separator]
        if not visible_items or self.selected_index >= len(visible_items):
            return
        
        selected = visible_items[self.selected_index]
        
        if selected.submenu:
            # Enter submenu
            self.menu_stack.append(self.current_menu)
            self.current_menu = selected.submenu
            self.selected_index = 0
        elif selected.action:
            # Execute action
            selected.action()
    
    def _go_back(self):
        """Go back to previous menu."""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            self.selected_index = 0
    
    # Action handlers
    def _open_claude(self):
        """Open Claude orchestrator in new terminal."""
        self.status_message = "Launching Claude orchestrator..."
        self.app.invalidate()
        
        # Launch Claude in new terminal
        import subprocess
        import platform
        
        system = platform.system()
        claude_command = "claude chat"
        
        try:
            if system == "Darwin":  # macOS
                # Use osascript to open new Terminal
                script = f'''
                tell application "Terminal"
                    activate
                    do script "{claude_command}"
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                self.status_message = "Claude launched in new terminal!"
            else:
                # For other systems, try to run directly
                subprocess.Popen(claude_command.split())
                self.status_message = "Claude launched!"
        except Exception as e:
            self.status_message = f"Failed to launch Claude: {str(e)}"
            logger.error(f"Failed to launch Claude: {e}")
        
        self.app.invalidate()
    
    def _select_agent(self, agent):
        """Select an agent as primary."""
        self.status_message = f"Selected {agent.name} as primary agent"
        # Would save this preference
        self.app.invalidate()
    
    def _browse_workflows(self):
        """Browse available workflows."""
        workflows = self.workflow_library.list_workflows()
        submenu = []
        
        # Add header explaining how to use workflows
        submenu.append(MenuItem("📖 Workflows are executed through Claude", None))
        submenu.append(MenuItem("Ask Claude: 'run the deploy workflow'", None))
        submenu.append(MenuItem("", separator=True))
        
        # Show library workflows
        if workflows:
            submenu.append(MenuItem("Available Workflows:", None))
            for workflow in workflows[:10]:  # Limit to 10 for UI
                description = workflow.get('description', '')[:50]
                submenu.append(
                    MenuItem(
                        f"  • {workflow['name']} - {description}",
                        lambda w=workflow: self._show_workflow_info(w)
                    )
                )
            
            if len(workflows) > 10:
                submenu.append(MenuItem(f"  ... and {len(workflows) - 10} more", None))
        else:
            submenu.append(MenuItem("No workflows found", None))
        
        submenu.append(MenuItem("", separator=True))
        submenu.append(MenuItem("← Back", self._go_back))
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 0
    
    def _show_workflow_info(self, workflow):
        """Show workflow information."""
        self.status_message = f"Tell Claude: 'run the {workflow['name']} workflow'"
        self.app.invalidate()
    
    def _select_project(self):
        """Select a project."""
        projects = list(self.project_store.list())
        submenu = []
        
        for slug, project in projects:
            submenu.append(
                MenuItem(
                    f"{slug} - {project.path}",
                    lambda p=project: self._switch_project(p)
                )
            )
        
        submenu.append(MenuItem("", separator=True))
        submenu.append(MenuItem("← Back", self._go_back))
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 0
    
    def _switch_project(self, project):
        """Switch to selected project."""
        self.status_message = f"Switched to project: {project.slug}"
        # Would update context
        self.app.invalidate()
    
    def _create_project(self):
        """Create a new project."""
        # In real implementation, would show input dialog
        self.status_message = "Project creation not yet implemented"
        self.app.invalidate()
    
    def _list_projects(self):
        """List all projects."""
        projects = list(self.project_store.list())
        self.status_message = f"Found {len(projects)} projects"
        self.app.invalidate()
    
    def _add_api_key(self):
        """Add an API key."""
        # In real implementation, would show input dialog
        self.status_message = "API key addition not yet implemented"
        self.app.invalidate()
    
    def _update_credential(self):
        """Update a credential."""
        self.status_message = "Credential update not yet implemented"
        self.app.invalidate()
    
    def _list_credentials(self):
        """List stored credentials."""
        # Would list from provider
        self.status_message = "Listing credentials..."
        self.app.invalidate()
    
    def _test_credential(self):
        """Test a credential connection."""
        self.status_message = "Credential testing not yet implemented"
        self.app.invalidate()
    
    def _view_agent_costs(self):
        """View agent cost breakdown."""
        costs = [
            "Claude 3 Opus: $0.25/1K input, $1.25/1K output",
            "Codex: $0.02/1K tokens",
            "GPT-4: $0.03/1K input, $0.06/1K output",
            "Local LLMs: Free (requires GPU)",
        ]
        
        submenu = [MenuItem(cost) for cost in costs]
        submenu.append(MenuItem("", separator=True))
        submenu.append(MenuItem("← Back", self._go_back))
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 0
    
    def _show_server_status(self):
        """Show Meta-MCP server status."""
        self.status_message = "Server running on port 8585"
        # Would show detailed status
        self.app.invalidate()
    
    def _show_help(self):
        """Show help and documentation."""
        help_items = [
            "Documentation: https://agtos.ai/docs",
            "GitHub: https://github.com/agtos-ai/agtos",
            "Report Issues: https://github.com/agtos-ai/agtos/issues",
            "",
            "Keyboard Shortcuts:",
            "  ↑↓ - Navigate menu",
            "  Enter - Select item",
            "  / - Search",
            "  Esc - Go back",
            "  Ctrl+C - Quit",
        ]
        
        submenu = [MenuItem(item) for item in help_items]
        submenu.append(MenuItem("", separator=True))
        submenu.append(MenuItem("← Back", self._go_back))
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 0
    
    def _get_agent_cost_info(self, agent_name: str) -> str:
        """Get cost information for an agent."""
        # In real implementation, would fetch actual costs
        costs = {
            "claude": "$0.25/1K tokens",
            "codex": "$0.02/1K tokens",
            "gpt4": "$0.03/1K tokens",
            "ollama": "Free (local)",
        }
        return costs.get(agent_name.lower(), "Unknown")
    
    def _check_updates(self):
        """Check for agtOS updates with enhanced UI."""
        self.status_message = "Checking for updates..."
        self.app.invalidate()
        
        try:
            # Get current version
            current_version = self._get_current_version()
            
            # Check GitHub for latest release
            latest_version, download_url, release_info = self._get_latest_version()
            
            if latest_version and current_version:
                if version.parse(latest_version) > version.parse(current_version):
                    # Store update info
                    self.pending_update = {
                        "current": current_version,
                        "latest": latest_version,
                        "download_url": download_url,
                        "release_info": release_info
                    }
                    
                    # Check if this version was skipped
                    skipped = self.update_preferences.get("skipped_versions", [])
                    if latest_version not in skipped:
                        self._show_update_menu(current_version, latest_version, release_info)
                    else:
                        self.status_message = f"Update available: v{latest_version} (skipped)"
                else:
                    self.status_message = f"You're up to date! (v{current_version})"
            else:
                self.status_message = "Unable to check for updates"
                
        except Exception as e:
            self.status_message = f"Update check failed: {str(e)}"
            logger.error(f"Update check error: {e}")
        
        self.app.invalidate()
    
    def _get_current_version(self) -> str:
        """Get current agtOS version."""
        try:
            # Try to get from pyproject.toml
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                import toml
                data = toml.load(pyproject_path)
                return data["tool"]["poetry"]["version"]
        except:
            pass
        
        # Fallback to package version
        try:
            import pkg_resources
            return pkg_resources.get_distribution("agtos").version
        except:
            return "0.3.2-dev"  # Fallback version
    
    def _get_latest_version(self) -> tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        """Get latest version from GitHub releases."""
        try:
            from .github_auth import get_github_auth
            
            # Get authenticated access for private repo
            github_auth = get_github_auth()
            release_info = github_auth.get_latest_release()
            
            if release_info:
                tag = release_info.get("tag_name", "").lstrip("v")
                
                # Find wheel asset
                download_url = None
                for asset in release_info.get("assets", []):
                    if asset["name"].endswith(".whl"):
                        download_url = asset["browser_download_url"]
                        break
                
                # Extract release info
                formatted_info = {
                    "name": release_info.get("name", f"v{tag}"),
                    "body": release_info.get("body", "No release notes available"),
                    "published_at": release_info.get("published_at", ""),
                    "html_url": release_info.get("html_url", "")
                }
                
                return tag, download_url, formatted_info
            
        except Exception as e:
            logger.error(f"Failed to check GitHub releases: {e}")
        
        return None, None, None
    
    def _load_update_preferences(self) -> Dict[str, Any]:
        """Load update preferences from config."""
        config_path = get_config_dir() / "update_preferences.json"
        
        default_prefs = {
            "check_on_startup": True,
            "skipped_versions": [],
            "last_check": None,
            "auto_update": False,
        }
        
        if config_path.exists():
            try:
                with open(config_path) as f:
                    prefs = json.load(f)
                    default_prefs.update(prefs)
            except Exception as e:
                logger.warning(f"Failed to load update preferences: {e}")
        
        return default_prefs
    
    def _save_update_preferences(self):
        """Save update preferences to config."""
        config_path = get_config_dir() / "update_preferences.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(self.update_preferences, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save update preferences: {e}")
    
    def _check_updates_startup(self):
        """Check for updates on startup (non-blocking)."""
        try:
            # Quick check without blocking UI
            import threading
            
            def check():
                current = self._get_current_version()
                latest, url, info = self._get_latest_version()
                
                if latest and current and version.parse(latest) > version.parse(current):
                    skipped = self.update_preferences.get("skipped_versions", [])
                    if latest not in skipped:
                        self.status_message = f"🎉 Update available: v{latest} (Select 'Check for Updates' to install)"
                        self.app.invalidate()
            
            # Run in background
            threading.Thread(target=check, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Startup update check failed: {e}")
    
    def _show_update_menu(self, current_version: str, new_version: str, release_info: Dict[str, Any]):
        """Show update options submenu."""
        submenu = [
            MenuItem(f"🎉 Update Available: v{new_version}", None),
            MenuItem(f"📦 Current version: v{current_version}", None),
            MenuItem("", separator=True),
            MenuItem("✨ Install Update Now", lambda: self._install_update(new_version)),
            MenuItem("📋 View Release Notes", lambda: self._view_release_notes(release_info)),
            MenuItem("⏭️  Skip This Version", lambda: self._skip_version(new_version)),
            MenuItem("🔔 Update Settings", submenu=self._build_update_settings_menu()),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ]
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 3  # Default to "Install Update Now"
    
    def _install_update(self, new_version: str):
        """Install the update using pip."""
        self.status_message = f"Installing v{new_version}..."
        self.app.invalidate()
        
        try:
            # Determine the download URL
            if self.pending_update and self.pending_update.get("download_url"):
                download_url = self.pending_update["download_url"]
                
                # For private repos, we need to download the asset first
                from .github_auth import get_github_auth
                github_auth = get_github_auth()
                
                # Download to temp location
                import tempfile
                temp_dir = Path(tempfile.mkdtemp())
                wheel_file = temp_dir / f"agtos-{new_version}-py3-none-any.whl"
                
                try:
                    self.status_message = f"Downloading v{new_version}..."
                    self.app.invalidate()
                    
                    github_auth.download_private_asset(download_url, wheel_file)
                    package_spec = str(wheel_file)
                except Exception as e:
                    # If download fails, try with token in URL
                    token = github_auth.get_token()
                    if token:
                        package_spec = f"{download_url}#egg=agtos&token={token}"
                    else:
                        raise RuntimeError(
                            "Cannot download from private repository. "
                            "Please set GitHub token using:\n"
                            "  export GITHUB_TOKEN=your_token"
                        )
            else:
                # Fallback to PyPI (when available)
                package_spec = f"agtos=={new_version}"
            
            # Run pip upgrade
            self.status_message = f"Installing v{new_version}..."
            self.app.invalidate()
            
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package_spec],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.status_message = "✅ Update successful! Please restart agtOS."
            self.app.invalidate()
            
            # Show restart option
            self._show_restart_menu()
            
            # Cleanup temp file if used
            if 'temp_dir' in locals():
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            
        except subprocess.CalledProcessError as e:
            self.status_message = f"❌ Update failed: {e.stderr}"
            logger.error(f"Update failed: {e}")
        except Exception as e:
            self.status_message = f"❌ Update error: {str(e)}"
            logger.error(f"Update error: {e}")
    
    def _show_restart_menu(self):
        """Show restart options after update."""
        submenu = [
            MenuItem("✅ Update Complete!", None),
            MenuItem("", separator=True),
            MenuItem("🔄 Restart agtOS Now", self._restart_application),
            MenuItem("⏸️  Restart Later", self._go_back),
        ]
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 2
    
    def _restart_application(self):
        """Restart the application after update."""
        self.status_message = "Restarting agtOS..."
        self.app.invalidate()
        
        # Exit the current app
        self.app.exit()
        
        # Restart based on platform
        if sys.platform == 'win32':
            # Windows: Start new process
            subprocess.Popen([sys.executable, "-m", "agtos"])
        else:
            # Unix/Linux/macOS: Replace current process
            os.execl(sys.executable, sys.executable, "-m", "agtos")
    
    def _view_release_notes(self, release_info: Dict[str, Any]):
        """View release notes in a submenu."""
        # Parse release notes
        body = release_info.get("body", "No release notes available")
        lines = body.split('\n')
        
        # Create menu items from release notes
        submenu = [
            MenuItem(f"📝 {release_info.get('name', 'Release Notes')}", None),
            MenuItem("", separator=True),
        ]
        
        # Add each line as a menu item (truncated if needed)
        for line in lines[:20]:  # Limit to 20 lines
            if line.strip():
                # Truncate long lines
                display_line = line[:80] + "..." if len(line) > 80 else line
                submenu.append(MenuItem(display_line, None))
        
        if len(lines) > 20:
            submenu.append(MenuItem("... (truncated)", None))
        
        submenu.extend([
            MenuItem("", separator=True),
            MenuItem(f"🔗 View on GitHub: {release_info.get('html_url', 'N/A')}", None),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ])
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = submenu
        self.selected_index = 0
    
    def _skip_version(self, version_to_skip: str):
        """Skip a specific version."""
        skipped = self.update_preferences.get("skipped_versions", [])
        if version_to_skip not in skipped:
            skipped.append(version_to_skip)
            self.update_preferences["skipped_versions"] = skipped
            self._save_update_preferences()
        
        self.status_message = f"Version {version_to_skip} will be skipped"
        self._go_back()
    
    def _build_update_settings_menu(self) -> List[MenuItem]:
        """Build update settings submenu."""
        check_startup = self.update_preferences.get("check_on_startup", True)
        
        return [
            MenuItem(
                f"{'✅' if check_startup else '⬜'} Check for updates on startup",
                self._toggle_startup_check
            ),
            MenuItem("🗑️  Clear skipped versions", self._clear_skipped_versions),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ]
    
    def _toggle_startup_check(self):
        """Toggle check for updates on startup."""
        current = self.update_preferences.get("check_on_startup", True)
        self.update_preferences["check_on_startup"] = not current
        self._save_update_preferences()
        
        self.status_message = f"Startup update check: {'enabled' if not current else 'disabled'}"
        # Refresh the current menu
        self.current_menu = self._build_update_settings_menu()
        self.app.invalidate()
    
    def _clear_skipped_versions(self):
        """Clear all skipped versions."""
        self.update_preferences["skipped_versions"] = []
        self._save_update_preferences()
        
        self.status_message = "Cleared all skipped versions"
        self._go_back()
    
    def _check_authentication(self):
        """Check if user is authenticated."""
        self.current_user = self.auth_manager.get_current_user()
        self.needs_auth = self.auth_manager.check_auth_required()
        
        if self.needs_auth:
            self.status_message = "Authentication required - Please sign in"
        else:
            self.status_message = f"Welcome {self.current_user.name or self.current_user.email}!"
    
    def _show_auth_menu(self):
        """Show authentication menu for sign in/sign up."""
        auth_menu = [
            MenuItem("🔐 Sign In with Existing Account", self._sign_in),
            MenuItem("🎟️ Sign Up with Invite Code", self._sign_up),
            MenuItem("", separator=True),
            MenuItem("📖 Learn About agtOS Beta", self._show_beta_info),
            MenuItem("🌐 Visit agtos.ai", self._open_website),
            MenuItem("", separator=True),
            MenuItem("Exit", lambda: self.app.exit()),
        ]
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = auth_menu
        self.selected_index = 0
    
    def _sign_in(self):
        """Handle sign in flow."""
        # Exit TUI temporarily for authentication
        self.app.exit()
        
        # Use CLI auth command
        import subprocess
        subprocess.run([sys.executable, "-m", "agtos", "auth", "login"])
        
        # Re-check authentication and restart TUI
        print("\nRestarting agtOS...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    def _sign_up(self):
        """Handle sign up with invite code."""
        # Exit TUI temporarily for authentication
        self.app.exit()
        
        # Use CLI auth command
        import subprocess
        subprocess.run([sys.executable, "-m", "agtos", "auth", "signup"])
        
        # Re-check authentication and restart TUI
        print("\nRestarting agtOS...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    def _show_beta_info(self):
        """Show information about the beta program."""
        info_menu = [
            MenuItem("🚀 agtOS Beta Program", None),
            MenuItem("", separator=True),
            MenuItem("agtOS is the Agent Operating System that orchestrates", None),
            MenuItem("multiple AI agents through a unified interface.", None),
            MenuItem("", separator=True),
            MenuItem("Beta Access includes:", None),
            MenuItem("  • Natural language tool creation", None),
            MenuItem("  • Multi-agent orchestration", None),
            MenuItem("  • Secure credential management", None),
            MenuItem("  • Workflow automation", None),
            MenuItem("", separator=True),
            MenuItem("Request an invite at agtos.ai", None),
            MenuItem("", separator=True),
            MenuItem("← Back", self._go_back),
        ]
        
        self.menu_stack.append(self.current_menu)
        self.current_menu = info_menu
        self.selected_index = 0
    
    def _open_website(self):
        """Open agtos.ai in browser."""
        import webbrowser
        webbrowser.open("https://agtos.ai")
        self.status_message = "Opening agtos.ai..."
        self.app.invalidate()
    
    def run(self):
        """Run the TUI application."""
        try:
            self.app.run()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.error(f"TUI error: {e}")
            raise


def launch_tui():
    """Launch the agtOS Terminal User Interface."""
    tui = AgtOSTUI()
    
    # Check if authentication is required
    if tui.needs_auth:
        # Show auth menu instead of main menu
        tui._show_auth_menu()
    
    tui.run()


if __name__ == "__main__":
    launch_tui()