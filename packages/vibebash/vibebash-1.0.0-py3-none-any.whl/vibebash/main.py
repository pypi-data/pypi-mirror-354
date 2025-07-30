#!/usr/bin/env python3

import json
import os
import platform
import shutil
import subprocess
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Suppress warnings from external packages
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

# Data models
class Command(BaseModel):
    command: str = Field(description="The shell command to execute", min_length=1)
    explanation: str = Field(description="Clear explanation of what this command does", min_length=1)
    risk_level: str = Field(description="Risk level: low, medium, high", pattern="^(low|medium|high)$")

class CommandList(BaseModel):
    commands: List[Command] = Field(description="List of commands to execute the requested action", min_length=1)

class ExecutedCommand(BaseModel):
    command: str = Field(min_length=1)
    explanation: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)
    success: bool
    output: str = Field(default="")
    user_comment: Optional[str] = Field(default=None)

class VibeBash:
    def __init__(self, model_name: str = "llama3.2"):
        self.console = Console()
        self.history_file = Path.home() / ".vibebash_history.json"
        self.config_file = Path.home() / ".vibebash_config.json"
        self.load_config()
        self.setup_llm(model_name)
        self.parser = PydanticOutputParser(pydantic_object=CommandList)
        self.history = self.load_history()
        
    def load_config(self):
        """Load API keys and configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
            self.create_config()
    
    def create_config(self):
        """Create initial configuration file"""
        self.console.print("[yellow]First time setup - configuring Ollama[/yellow]")
        
        config = {
            "ollama_base_url": Prompt.ask("Ollama Base URL", default="http://localhost:11434"),
            "default_model_name": Prompt.ask("Default model name", default="llama3.2")
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.config = config
        self.console.print(f"[green]Configuration saved to {self.config_file}[/green]")
    
    def setup_llm(self, model_name: str):
        """Setup ChatOllama language model"""
        try:
            base_url = self.config.get("ollama_base_url", "http://localhost:11434")
            self.llm = ChatOllama(
                model=model_name,
                base_url=base_url,
                temperature=0.1
            )
            self.console.print(f"[green]✓ Connected to ChatOllama model: {model_name}[/green]")
                
        except Exception as e:
            self.console.print(f"[red]Error setting up ChatOllama: {e}[/red]")
            self.console.print("[yellow]Make sure Ollama is running: ollama serve[/yellow]")
            sys.exit(1)
    
    def get_system_info(self) -> str:
        """Get current system information for context"""
        try:
            import platform
            return f"""
Current system: {platform.system()} {platform.release()}
Current directory: {os.getcwd()}
Shell: {os.getenv('SHELL', 'unknown')}
User: {os.getenv('USER', 'unknown')}
"""
        except:
            return "System info unavailable"
    
    def create_prompt(self, user_request: str, previous_commands: List[str] = None, error_context: str = None) -> str:
        """Create the prompt for the LLM"""
        system_info = self.get_system_info()
        
        base_prompt = f"""
You are a helpful shell command assistant. Given a user's request, generate a list of shell commands to accomplish the task.

System Information:
{system_info}

IMPORTANT GUIDELINES:
1. Only suggest safe, commonly used commands
2. Avoid destructive operations (rm -rf, format, etc.) unless explicitly requested
3. Provide clear explanations for each command
4. Rate each command's risk level as: low, medium, or high
5. For medium/high risk commands, suggest safer alternatives when possible
6. Consider the user's current system and directory context
7. If a command might not be available, suggest installation steps or alternatives first
8. CRITICAL: Each command must be complete and executable on its own. If you need to pipe commands together, write them as a single command with pipes (e.g., "ls | grep .py"). Do NOT split piped operations into separate commands.
9. CRITICAL: Each command should be a standalone shell command that can be executed independently. Avoid commands that depend on the output of a previous command unless explicitly using shell redirection or pipes within the same command.
10. CRITICAL: When encounter a command like "find all .py files in current directory", generate a single command that does this, such as "find . -name '*.py'". Do not split it into multiple commands like "cd" and "find".
11. Use pipes whenever it is convenient, but ensure the entire command is executable as a single line. Do not give commands that are supposed to be run in pipes separately. This breaks the flow and makes it output non-executable commands.
12. For tools that might not be installed (like nmap, docker, etc.), include installation commands first

Previous commands executed in this session:
{chr(10).join(previous_commands) if previous_commands else "None"}"""

        if error_context:
            base_prompt += f"""

Previous Error Context:
{error_context}

Please consider this error when generating new commands. Suggest alternatives or fixes for the failed command."""

        base_prompt += f"""

User Request: "{user_request}"

{self.parser.get_format_instructions()}

CRITICAL: You MUST respond with ONLY valid JSON that matches the schema. Do not include any explanatory text before or after the JSON. Do not include markdown code blocks. Start your response directly with the opening brace {{ and end with the closing brace }}.

Generate commands that will accomplish the user's request step by step.
"""
        return base_prompt
    
    async def get_commands(self, user_request: str, previous_commands: List[str] = None, error_context: str = None) -> List[Command]:
        """Get command suggestions from the LLM with streaming feedback"""
        try:
            prompt = self.create_prompt(user_request, previous_commands, error_context)
            
            # Show progress while generating
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Generating commands..."),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task("generating", total=None)
                
                # Try streaming first, fallback to regular invoke
                try:
                    # Use streaming if available
                    if hasattr(self.llm, 'astream'):
                        chunks = []
                        progress.update(task, description="[bold blue]Receiving response...")
                        async for chunk in self.llm.astream([HumanMessage(content=prompt)]):
                            if hasattr(chunk, 'content') and chunk.content:
                                chunks.append(chunk.content)
                        response_content = ''.join(chunks)
                    elif hasattr(self.llm, 'stream'):
                        chunks = []
                        progress.update(task, description="[bold blue]Receiving response...")
                        for chunk in self.llm.stream([HumanMessage(content=prompt)]):
                            if hasattr(chunk, 'content') and chunk.content:
                                chunks.append(chunk.content)
                        response_content = ''.join(chunks)
                    else:
                        # Fallback to regular invoke
                        progress.update(task, description="[bold blue]Processing request...")
                        if hasattr(self.llm, 'ainvoke'):
                            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                        else:
                            response = self.llm.invoke([HumanMessage(content=prompt)])
                        response_content = response.content
                
                except Exception as stream_error:
                    self.console.print(f"[yellow]Streaming failed, using standard mode: {stream_error}[/yellow]")
                    # Fallback to regular invoke
                    if hasattr(self.llm, 'ainvoke'):
                        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                    else:
                        response = self.llm.invoke([HumanMessage(content=prompt)])
                    response_content = response.content
                
                progress.update(task, description="[bold blue]Parsing response...")
            
            # Parse the response
            try:
                parsed_response = self.parser.parse(response_content)
                return parsed_response.commands
            except Exception as parse_error:
                self.console.print(f"[red]Error parsing LLM response: {parse_error}[/red]")
                self.console.print(f"[yellow]Raw response (first 500 chars):[/yellow]\n{response_content[:500]}")
                
                # Try to extract JSON from response if it's wrapped in text
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        parsed_response = self.parser.parse(json_str)
                        self.console.print("[green]Successfully extracted JSON from response[/green]")
                        return parsed_response.commands
                except Exception:
                    pass
                
                self.console.print("[red]Could not parse or extract valid JSON from response[/red]")
                return []
            
        except Exception as e:
            self.console.print(f"[red]Error getting commands from LLM: {e}[/red]")
            return []
    
    def check_command_availability(self, command: str) -> Tuple[bool, str]:
        """Check if a command is available and provide installation guidance if not"""
        # Extract the main command (first word)
        main_cmd = command.split()[0]
        
        # Skip built-in shell commands and basic utilities
        builtin_commands = {
            'cd', 'pwd', 'echo', 'ls', 'cat', 'cp', 'mv', 'rm', 'mkdir', 'rmdir',
            'chmod', 'chown', 'grep', 'find', 'which', 'whoami', 'df', 'du', 'ps',
            'kill', 'top', 'tail', 'head', 'sort', 'uniq', 'wc', 'history', 'alias'
        }
        
        if main_cmd in builtin_commands:
            return True, ""
        
        # Check if command exists
        if shutil.which(main_cmd):
            return True, ""
        
        # Command not found - provide installation guidance
        install_guide = self.get_installation_guide(main_cmd)
        return False, install_guide
    
    def get_installation_guide(self, command: str) -> str:
        """Get installation guidance for missing commands"""
        system = platform.system().lower()
        
        # Common command installation mappings
        install_commands = {
            # Development tools
            'git': {
                'darwin': 'brew install git',
                'linux': 'sudo apt install git (Ubuntu/Debian) or sudo yum install git (RHEL/CentOS)',
                'windows': 'winget install Git.Git'
            },
            'curl': {
                'darwin': 'curl is pre-installed',
                'linux': 'sudo apt install curl (Ubuntu/Debian) or sudo yum install curl (RHEL/CentOS)',
                'windows': 'curl is available in Windows 10+ or install via winget install cURL.cURL'
            },
            'wget': {
                'darwin': 'brew install wget',
                'linux': 'sudo apt install wget (Ubuntu/Debian) or sudo yum install wget (RHEL/CentOS)',
                'windows': 'winget install JernejSimoncic.Wget'
            },
            'python': {
                'darwin': 'brew install python',
                'linux': 'sudo apt install python3 (Ubuntu/Debian) or sudo yum install python3 (RHEL/CentOS)',
                'windows': 'winget install Python.Python.3'
            },
            'node': {
                'darwin': 'brew install node',
                'linux': 'sudo apt install nodejs npm (Ubuntu/Debian) or sudo yum install nodejs npm (RHEL/CentOS)',
                'windows': 'winget install OpenJS.NodeJS'
            },
            'docker': {
                'darwin': 'brew install --cask docker',
                'linux': 'Visit https://docs.docker.com/engine/install/ for installation instructions',
                'windows': 'winget install Docker.DockerDesktop'
            },
            'tree': {
                'darwin': 'brew install tree',
                'linux': 'sudo apt install tree (Ubuntu/Debian) or sudo yum install tree (RHEL/CentOS)',
                'windows': 'tree is built-in or install via winget install GnuWin32.Tree'
            },
            'htop': {
                'darwin': 'brew install htop',
                'linux': 'sudo apt install htop (Ubuntu/Debian) or sudo yum install htop (RHEL/CentOS)',
                'windows': 'Use Task Manager or install Windows Terminal with WSL'
            },
            'vim': {
                'darwin': 'vim is pre-installed or brew install vim',
                'linux': 'sudo apt install vim (Ubuntu/Debian) or sudo yum install vim (RHEL/CentOS)',
                'windows': 'winget install vim.vim'
            },
            'nano': {
                'darwin': 'nano is pre-installed',
                'linux': 'sudo apt install nano (Ubuntu/Debian) or sudo yum install nano (RHEL/CentOS)',
                'windows': 'Use notepad or install via WSL'
            },
            'jq': {
                'darwin': 'brew install jq',
                'linux': 'sudo apt install jq (Ubuntu/Debian) or sudo yum install jq (RHEL/CentOS)',
                'windows': 'winget install jqlang.jq'
            },
            'nmap': {
                'darwin': 'brew install nmap',
                'linux': 'sudo apt install nmap (Ubuntu/Debian) or sudo yum install nmap (RHEL/CentOS)',
                'windows': 'winget install Insecure.Nmap'
            }
        }
        
        if command in install_commands:
            cmd_info = install_commands[command]
            if system in cmd_info:
                return f"Command '{command}' not found. Install with: {cmd_info[system]}"
            else:
                return f"Command '{command}' not found. Check your package manager for installation."
        
        # Generic installation guidance
        if system == 'darwin':
            return f"Command '{command}' not found. Try: brew install {command} or brew search {command}"
        elif system == 'linux':
            return f"Command '{command}' not found. Try: sudo apt search {command} (Ubuntu/Debian) or sudo yum search {command} (RHEL/CentOS)"
        elif system == 'windows':
            return f"Command '{command}' not found. Try: winget search {command} or check if available in Windows Subsystem for Linux (WSL)"
        else:
            return f"Command '{command}' not found. Please check your system's package manager."

    def execute_command(self, command: str) -> tuple[bool, str]:
        """Execute a shell command and return success status and output"""
        # Check if command is available first
        is_available, install_guide = self.check_command_availability(command)
        if not is_available:
            return False, install_guide
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            return result.returncode == 0, output.strip()
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 30 seconds"
        except Exception as e:
            return False, f"Error executing command: {str(e)}"
    
    def save_to_history(self, executed_command: ExecutedCommand):
        """Save executed command to history"""
        self.history.append(executed_command.model_dump())
        
        # Keep only last 100 commands
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not save history: {e}[/yellow]")
    
    def load_history(self) -> List[Dict]:
        """Load command history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def display_command(self, cmd: Command, index: int):
        """Display a command with syntax highlighting"""
        from rich.console import Group
        from rich.text import Text
        
        risk_colors = {
            "low": "green",
            "medium": "yellow", 
            "high": "red"
        }
        
        risk_color = risk_colors.get(cmd.risk_level.lower(), "white")
        
        # Create components for the panel
        explanation = Text(cmd.explanation, style="bold")
        command_label = Text("\nCommand:")
        syntax_command = Syntax(cmd.command, "bash", theme="monokai", line_numbers=False)
        risk_text = Text(f"\nRisk Level: {cmd.risk_level.upper()}", style=risk_color)
        
        # Group all components together
        panel_content = Group(explanation, command_label, syntax_command, risk_text)
        
        self.console.print(Panel(
            panel_content,
            title=f"Command {index + 1}",
            border_style=risk_color
        ))
    
    async def process_request(self, user_request: str):
        """Main processing loop"""
        self.console.print(f"\n[bold blue]🤖 Processing request:[/bold blue] {user_request}")
        
        # Get previous commands for context
        recent_commands = [cmd["command"] for cmd in self.history[-5:]]
        
        # Get command suggestions
        commands = await self.get_commands(user_request, recent_commands)
        
        if not commands:
            self.console.print("[red]No commands generated. Please try rephrasing your request.[/red]")
            return
        
        self.console.print(f"\n[green]Generated {len(commands)} commands:[/green]")
        
        executed_commands = []
        user_comments = []
        
        # Process each command
        for i, cmd in enumerate(commands):
            self.display_command(cmd, i)
            
            while True:
                action = Prompt.ask(
                    "\n[bold]Action:[/bold]",
                    choices=["run", "skip", "comment", "quit", "regenerate"],
                    default="run"
                )
                
                if action == "run":
                    self.console.print(f"\n[yellow]Executing:[/yellow] {cmd.command}")
                    success, output = self.execute_command(cmd.command)
                    
                    # Save to history
                    executed_cmd = ExecutedCommand(
                        command=cmd.command,
                        explanation=cmd.explanation,
                        timestamp=datetime.now().isoformat(),
                        success=success,
                        output=output
                    )
                    
                    self.save_to_history(executed_cmd)
                    executed_commands.append(cmd.command)
                    
                    if success:
                        self.console.print("[green]✓ Command executed successfully[/green]")
                        if output:
                            self.console.print(f"Output:\n{output}")
                    else:
                        self.console.print(f"[red]✗ Command failed: {output}[/red]")
                        
                        # Ask if user wants to get alternative suggestions based on the error
                        if Confirm.ask("\nWould you like me to suggest alternatives based on this error?"):
                            error_context = f"Command '{cmd.command}' failed with error: {output}"
                            
                            # Get new suggestions with error context
                            alt_commands = await self.get_commands(user_request, recent_commands, error_context)
                            if alt_commands:
                                self.console.print(f"\n[green]Generated {len(alt_commands)} alternative commands:[/green]")
                                # Process the alternative commands
                                for j, alt_cmd in enumerate(alt_commands):
                                    self.display_command(alt_cmd, j)
                                    alt_action = Prompt.ask(
                                        "\n[bold]Action for alternative:[/bold]",
                                        choices=["run", "skip"],
                                        default="run"
                                    )
                                    if alt_action == "run":
                                        alt_success, alt_output = self.execute_command(alt_cmd.command)
                                        alt_executed_cmd = ExecutedCommand(
                                            command=alt_cmd.command,
                                            explanation=alt_cmd.explanation,
                                            timestamp=datetime.now().isoformat(),
                                            success=alt_success,
                                            output=alt_output
                                        )
                                        self.save_to_history(alt_executed_cmd)
                                        
                                        if alt_success:
                                            self.console.print("[green]✓ Alternative command executed successfully[/green]")
                                            if alt_output:
                                                self.console.print(f"Output:\n{alt_output}")
                                            break
                                        else:
                                            self.console.print(f"[red]✗ Alternative command also failed: {alt_output}[/red]")
                    
                    break
                
                elif action == "skip":
                    self.console.print("[yellow]Skipping command[/yellow]")
                    break
                
                elif action == "comment":
                    comment = Prompt.ask("Enter your comment for improvement")
                    user_comments.append(f"Command {i+1}: {comment}")
                    self.console.print("[blue]Comment saved for regeneration[/blue]")
                    continue
                
                elif action == "quit":
                    self.console.print("[red]Stopping execution[/red]")
                    return
                
                elif action == "regenerate":
                    if user_comments:
                        regenerate_prompt = f"{user_request}\n\nUser feedback on previous commands:\n" + "\n".join(user_comments)
                        await self.process_request(regenerate_prompt)
                        return
                    else:
                        self.console.print("[yellow]No comments to use for regeneration[/yellow]")
                        continue
        
        self.console.print("\n[green]✓ Request processing completed![/green]")

@click.command()
@click.argument('request', required=False)
@click.option('--model-name', default=None, help='Ollama model name (e.g., deepcoder, llama3.2)')
@click.option('--history', is_flag=True, help='Show command history')
@click.option('--config', is_flag=True, help='Reconfigure Ollama settings')
def main(request, model_name, history, config):
    """VibeBash - Offline natural language to shell commands with ChatOllama"""
    
    # Initialize VibeBash
    try:
        if config:
            # Force config recreation
            config_file = Path.home() / ".vibebash_config.json"
            if config_file.exists():
                config_file.unlink()
        
        # Use model name if specified, otherwise use config default
        if model_name:
            vb = VibeBash(model_name=model_name)
        else:
            vb = VibeBash()
        
        if history:
            vb.console.print("[bold]Command History:[/bold]")
            for cmd in vb.history[-10:]:  # Show last 10
                timestamp = cmd.get('timestamp', 'Unknown')
                command = cmd.get('command', 'Unknown')
                success = "✓" if cmd.get('success', False) else "✗"
                vb.console.print(f"{timestamp}: {success} {command}")
            return
        
        if config:
            # Config flag only recreates config, then exits
            vb.console.print("[green]Configuration updated successfully![/green]")
            return
        
        if not request:
            request = Prompt.ask("[bold blue]What would you like to do?[/bold blue]")
        
        # Process the request
        import asyncio
        asyncio.run(vb.process_request(request))
        
    except KeyboardInterrupt:
        print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()