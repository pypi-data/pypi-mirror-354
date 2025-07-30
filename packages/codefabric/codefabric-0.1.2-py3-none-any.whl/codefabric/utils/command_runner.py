import subprocess
import os
from dataclasses import dataclass
from typing import List, Union

@dataclass
class CommandResult:
    """Represents the result of a single command execution"""
    command: Union[str, List[str]]
    is_success: bool
    output: str
    error: str
    
    def __str__(self) -> str:
        """Returns a formatted string representation of the command execution result."""
        status = "Success" if self.is_success else "Failed"
        
        # Ensure output and error messages are clean
        output = self.output.strip() if self.output else "No output"
        error = self.error.strip() if self.error else "No error"

        return (
            f"Command Executed: {self.command}\n"
            f"Command Output: {output}\n"
            f"Execution Status: {status}\n"
            f"Error Message: {error}"
        )

class CommandRunner:
    def __init__(self,cwd:str):
        self.cwd = cwd
        
    def run_commands(self,commands: List[List[str]]) -> List[CommandResult]:
        """
        Runs multiple shell commands in the specified working directory, ensuring sequential execution.
        
        Args:
            commands (List[Union[str, List[str]]]): List of commands, each can be a string or list of arguments
            cwd (str): The working directory path to run the commands in
            
        Returns:
            List[CommandResult]: List of command execution results
            
        Raises:
            FileNotFoundError: If the specified directory doesn't exist
        """
        cwd = self.cwd

        # Verify the directory exists
        if not os.path.isdir(cwd):
            raise FileNotFoundError(f"Directory not found: {cwd}")
        
        results: List[CommandResult] = []
        
        # Process each command sequentially
        for cmd in commands:
            try:
                # Ensure cmd is properly formatted
                if not isinstance(cmd, (str, list)):
                    raise ValueError(f"Invalid command format: {cmd}")
                
                env = os.environ.copy()
                for item in ['VIRTUAL_ENV','VIRTUAL_ENV_PROMPT']:
                    env.pop(item, None)
                
                # Run the command sequentially
                process = subprocess.run(
                    cmd,
                    cwd=cwd,
                    shell=True,  # Since we are passing string commands
                    text=True,
                    env=env,
                    capture_output=True  # Ensures output capturing without separate communicate()
                )
                
                # Store results
                result = CommandResult(
                    command=cmd,
                    is_success=(process.returncode == 0),
                    output=process.stdout,
                    error=process.stderr
                )
                results.append(result)
                    
            except subprocess.SubprocessError as e:
                results.append(CommandResult(
                    command=cmd,
                    is_success=False,
                    output="",
                    error=f"Subprocess error: {str(e)}"
                ))
            except PermissionError as e:
                results.append(CommandResult(
                    command=cmd,
                    is_success=False,
                    output="",
                    error=f"Permission denied: {str(e)}"
                ))
            except FileNotFoundError as e:
                results.append(CommandResult(
                    command=cmd,
                    is_success=False,
                    output="",
                    error=f"Command not found: {str(e)}"
                ))
            except Exception as e:
                results.append(CommandResult(
                    command=cmd,
                    is_success=False,
                    output="",
                    error=f"Unexpected error: {str(e)}"
                ))
        
        return results