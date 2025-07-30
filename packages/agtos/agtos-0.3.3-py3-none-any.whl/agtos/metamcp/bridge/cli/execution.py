"""Command execution module for CLI Bridge.

This module handles building command lines from parameters and executing
them safely in subprocesses.

AI_CONTEXT:
    The CommandExecutor class is responsible for the execution phase:
    1. Building command lines from MCP parameters
    2. Validating working directories and arguments
    3. Executing commands in subprocesses with timeouts
    4. Capturing and formatting output
    5. Handling errors and edge cases
    
    Security is a key concern - all commands are executed with proper
    escaping and timeouts to prevent injection and hanging.
"""

import subprocess
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Executes CLI commands safely and returns structured results.
    
    AI_CONTEXT:
        This class handles the critical task of executing commands safely.
        It uses subprocess with proper argument handling (no shell=True),
        enforces timeouts, validates paths, and captures all output.
        
        The executor is designed to handle various CLI patterns while
        preventing common security issues like command injection.
    """
    
    def __init__(self, default_timeout: int = 30):
        """Initialize executor with default settings.
        
        Args:
            default_timeout: Default timeout in seconds for command execution
        """
        self.default_timeout = default_timeout
    
    def execute_cli_command(
        self, 
        cli_name: str, 
        subcommand: Optional[str], 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a CLI command with given parameters.
        
        Args:
            cli_name: Main CLI command name
            subcommand: Optional subcommand
            params: Parameters from MCP request
            
        Returns:
            Dictionary with output, exit_code, and error if any
            
        AI_CONTEXT:
            Main entry point for command execution. Builds the command
            line and delegates to _execute_command for actual execution.
            Returns a consistent result format regardless of success/failure.
        """
        try:
            # Build command from parameters
            command = self._build_command(cli_name, subcommand, params)
            
            # Extract working directory if provided
            working_directory = params.get("working_directory")
            
            # Execute and return result
            return self._execute_command(command, working_directory)
            
        except Exception as e:
            logger.error(f"Error preparing command execution: {e}")
            return {
                "output": "",
                "exit_code": -1,
                "error": f"Failed to prepare command: {str(e)}"
            }
    
    def _build_command(self, cli_name: str, subcommand: Optional[str], params: Dict[str, Any]) -> List[str]:
        """Build command line from parameters.
        
        Args:
            cli_name: Main CLI command
            subcommand: Optional subcommand
            params: Parameters from MCP request
            
        Returns:
            Command as list of arguments
            
        AI_CONTEXT:
            Builds commands in the safest way possible - as a list of
            arguments rather than a string. This prevents shell injection.
            Handles various parameter types:
            - Subcommands (positional)
            - Boolean flags (--flag)
            - Value flags (--flag value)
            - Positional arguments
            - Extra arguments
        """
        command = [cli_name]
        
        # Add subcommand
        self._add_subcommand(command, subcommand, params)
        
        # Add various types of parameters
        self._add_flag_array(command, params)
        self._add_named_parameters(command, params)
        self._add_positional_arguments(command, params)
        
        return command
    
    def _add_subcommand(self, command: List[str], subcommand: Optional[str], params: Dict[str, Any]) -> None:
        """Add subcommand to the command list.
        
        Args:
            command: Command list to append to
            subcommand: Explicit subcommand
            params: Parameters that might contain subcommand
        """
        if subcommand:
            command.append(subcommand)
        elif params.get("subcommand"):
            command.append(params["subcommand"])
    
    def _add_flag_array(self, command: List[str], params: Dict[str, Any]) -> None:
        """Add flags from the flags array parameter.
        
        Args:
            command: Command list to append to
            params: Parameters containing flags array
            
        AI_CONTEXT:
            Handles the 'flags' array parameter where users can specify
            multiple flags. Normalizes flag format by adding dashes.
        """
        if params.get("flags"):
            for flag in params["flags"]:
                formatted_flag = self._format_flag(flag)
                command.append(formatted_flag)
    
    def _format_flag(self, flag: str) -> str:
        """Format a flag with proper dash prefixes.
        
        Args:
            flag: Flag name with or without dashes
            
        Returns:
            Properly formatted flag
        """
        if not flag.startswith("-"):
            return f"--{flag}" if len(flag) > 1 else f"-{flag}"
        return flag
    
    def _add_named_parameters(self, command: List[str], params: Dict[str, Any]) -> None:
        """Add named parameters as command line flags.
        
        Args:
            command: Command list to append to
            params: Parameters to process
            
        AI_CONTEXT:
            Converts parameter names to flag format (underscore to dash).
            Handles boolean flags (only added if True) and value flags.
        """
        special_params = {"subcommand", "flags", "arguments", "extra_args", "working_directory"}
        
        for key, value in params.items():
            if key in special_params:
                continue
                
            flag_name = key.replace("_", "-")
            self._add_parameter_as_flag(command, flag_name, value)
    
    def _add_parameter_as_flag(self, command: List[str], flag_name: str, value: Any) -> None:
        """Add a single parameter as a command line flag.
        
        Args:
            command: Command list to append to
            flag_name: Flag name (without dashes)
            value: Flag value
        """
        if isinstance(value, bool):
            # Boolean flag - only add if True
            if value:
                command.append(f"--{flag_name}")
        elif value is not None:
            # Value flag - add flag and value
            command.append(f"--{flag_name}")
            command.append(str(value))
    
    def _add_positional_arguments(self, command: List[str], params: Dict[str, Any]) -> None:
        """Add positional and extra arguments to the command.
        
        Args:
            command: Command list to append to
            params: Parameters containing arguments
        """
        # Add positional arguments
        if params.get("arguments"):
            command.extend(str(arg) for arg in params["arguments"])
            
        # Add extra arguments
        if params.get("extra_args"):
            command.extend(str(arg) for arg in params["extra_args"])
    
    def _execute_command(self, command: List[str], working_directory: Optional[str] = None) -> Dict[str, Any]:
        """Execute a command and return results.
        
        Args:
            command: Command as list of arguments
            working_directory: Optional working directory
            
        Returns:
            Dictionary with output, exit code, and error if any
            
        AI_CONTEXT:
            Core execution method with safety features:
            1. Validates working directory exists
            2. Uses subprocess.run (not shell=True)
            3. Enforces timeout to prevent hanging
            4. Captures both stdout and stderr
            5. Returns structured results for consistency
            
            The timeout prevents runaway commands, and the working
            directory validation prevents navigation errors.
        """
        try:
            # Validate working directory
            cwd = self._validate_working_directory(working_directory)
            if isinstance(cwd, dict):  # Error response
                return cwd
            
            # Log command execution
            self._log_command_execution(command, cwd)
            
            # Execute command with timeout
            result = self._run_subprocess(command, cwd)
            
            # Build success response
            return self._build_success_response(result)
            
        except subprocess.TimeoutExpired:
            return self._build_timeout_error()
        except FileNotFoundError:
            return self._build_command_not_found_error(command[0])
        except PermissionError:
            return self._build_permission_error(command[0])
        except Exception as e:
            return self._build_generic_error(e)
    
    def _validate_working_directory(self, working_directory: Optional[str]) -> Optional[Path]:
        """Validate and resolve working directory.
        
        Args:
            working_directory: Directory path to validate
            
        Returns:
            Resolved Path object or error dict if invalid
        """
        if not working_directory:
            return None
            
        cwd = Path(working_directory).expanduser().resolve()
        
        if not cwd.exists():
            return {
                "output": "",
                "exit_code": 1,
                "error": f"Working directory does not exist: {working_directory}"
            }
            
        if not cwd.is_dir():
            return {
                "output": "",
                "exit_code": 1,
                "error": f"Working directory is not a directory: {working_directory}"
            }
            
        return cwd
    
    def _log_command_execution(self, command: List[str], cwd: Optional[Path]) -> None:
        """Log command execution for debugging.
        
        Args:
            command: Command being executed
            cwd: Working directory if any
        """
        logger.debug(f"Executing command: {' '.join(command)}")
        if cwd:
            logger.debug(f"Working directory: {cwd}")
    
    def _run_subprocess(self, command: List[str], cwd: Optional[Path]) -> subprocess.CompletedProcess:
        """Run the subprocess with safety features.
        
        Args:
            command: Command to execute
            cwd: Working directory
            
        Returns:
            Completed process result
        """
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=self.default_timeout,
            cwd=cwd
        )
    
    def _build_success_response(self, result: subprocess.CompletedProcess) -> Dict[str, Any]:
        """Build response for successful command execution.
        
        Args:
            result: Subprocess result
            
        Returns:
            Response dictionary
        """
        output = self._format_output(result.stdout, result.stderr, result.returncode)
        
        return {
            "output": output,
            "exit_code": result.returncode,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def _build_timeout_error(self) -> Dict[str, Any]:
        """Build error response for timeout."""
        return {
            "output": "",
            "exit_code": -1,
            "error": f"Command execution timed out after {self.default_timeout} seconds"
        }
    
    def _build_command_not_found_error(self, command: str) -> Dict[str, Any]:
        """Build error response for command not found."""
        return {
            "output": "",
            "exit_code": -1,
            "error": f"Command not found: {command}"
        }
    
    def _build_permission_error(self, command: str) -> Dict[str, Any]:
        """Build error response for permission denied."""
        return {
            "output": "",
            "exit_code": -1,
            "error": f"Permission denied executing: {command}"
        }
    
    def _build_generic_error(self, exception: Exception) -> Dict[str, Any]:
        """Build error response for generic exceptions."""
        logger.error(f"Unexpected error executing command: {exception}")
        return {
            "output": "",
            "exit_code": -1,
            "error": f"Failed to execute command: {str(exception)}"
        }
    
    def _format_output(self, stdout: str, stderr: str, returncode: int) -> str:
        """Format command output for return.
        
        Args:
            stdout: Standard output from command
            stderr: Standard error from command
            returncode: Exit code from command
            
        Returns:
            Formatted output string
            
        AI_CONTEXT:
            Combines stdout and stderr in a readable format.
            For successful commands, returns just stdout.
            For failures, includes stderr with clear labeling.
        """
        output = stdout.strip()
        
        # For failed commands, include stderr if present
        if returncode != 0 and stderr.strip():
            if output:
                output += "\n\nError output:\n"
            else:
                output = "Error output:\n"
            output += stderr.strip()
        
        return output