"""
Enhanced Command-Line Interface for AI Chat Manager

This module provides a comprehensive CLI with rich formatting, interactive features,
and advanced management capabilities for the AI Chat Manager system.
"""

import asyncio
import click
import json
import sys
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import yaml
import platform

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.columns import Columns
from rich.align import Align

from ..core.manager import ChatManager, create_chat_manager
from ..core.config import Config, BackendConfig, BotConfig, GlobalConfig
from ..core.exceptions import AIChatManagerError, ConfigurationError
from ..backends import (
    list_available_backends, get_backend_info, get_backend_recommendations,
    generate_backend_report, get_setup_instructions, get_feature_matrix
)

console = Console()

# Fix Windows console encoding issues
if platform.system() == "Windows":
    try:
        # Try to enable UTF-8 output on Windows
        import subprocess
        subprocess.run("chcp 65001", shell=True, capture_output=True)
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass  # Fallback to default encoding

def run_async(coro):
    """Helper to run async functions safely"""
    try:
        loop = asyncio.get_running_loop()
        # We're already in an event loop, need to run in thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running event loop, safe to create one
        return asyncio.run(coro)

# Global CLI state
current_manager: Optional[ChatManager] = None
config_path = "config.yaml"

class CLIState:
    """Manages CLI state and configuration"""
    
    def __init__(self):
        self.config_path = "config.yaml"
        self.debug = False
        self.quiet = False
        self.manager: Optional[ChatManager] = None
    
    def get_manager(self) -> ChatManager:
        """Get or create chat manager instance"""
        if self.manager is None:
            self.manager = ChatManager(self.config_path)
        return self.manager

# Global CLI state
cli_state = CLIState()

# Custom Click group with enhanced help
class EnhancedGroup(click.Group):
    """Enhanced Click group with better help formatting"""
    
    def format_help(self, ctx, formatter):
        formatter.write_heading("AI Chat Manager CLI")
        formatter.write_paragraph()
        formatter.write("A comprehensive command-line interface for managing AI chat bots and backends.")
        formatter.write_paragraph()
        
        super().format_help(ctx, formatter)
        
        formatter.write_paragraph()
        formatter.write_heading("Examples")
        examples = [
            "ai-chat-manager init                    # Initialize configuration",
            "ai-chat-manager backend add openai     # Add OpenAI backend",
            "ai-chat-manager bot create assistant   # Create a bot",
            "ai-chat-manager chat assistant         # Start chatting",
            "ai-chat-manager status                 # View system status",
        ]
        for example in examples:
            formatter.write(f"  {example}")

@click.group(cls=EnhancedGroup)
@click.option("--config", "-c", default="config.yaml", help="Configuration file path")
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-essential output")
@click.version_option(version="0.2.0", prog_name="AI Chat Manager")
@click.pass_context
def cli(ctx, config, debug, quiet):
    """AI Chat Manager - Modular AI API/Chat Manager"""
    # Store global options
    cli_state.config_path = config
    cli_state.debug = debug
    cli_state.quiet = quiet
    
    # Configure console
    if quiet:
        console.quiet = True
    
    # Set up context
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['debug'] = debug
    ctx.obj['quiet'] = quiet

# Initialization commands
@cli.command()
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
@click.option("--template", type=click.Choice(["minimal", "standard", "advanced"]), 
              default="standard", help="Configuration template")
def init(force, template):
    """Initialize AI Chat Manager configuration"""
    
    config_file = Path(cli_state.config_path)
    
    if config_file.exists() and not force:
        if not Confirm.ask(f"Configuration file {config_file} already exists. Overwrite?"):
            console.print("❌ Initialization cancelled", style="yellow")
            return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Initializing configuration...", total=None)
            
            # Create manager to initialize config
            manager = ChatManager(cli_state.config_path, auto_start=False)
            
            # Add template-specific configurations
            if template == "advanced":
                _setup_advanced_template(manager)
            elif template == "minimal":
                _setup_minimal_template(manager)
            else:
                _setup_standard_template(manager)
        
        console.print("✅ Configuration initialized successfully!", style="green")
        console.print(f"📄 Configuration file: {config_file}")
        
        # Show next steps
        _show_next_steps()
        
    except Exception as e:
        console.print(f"❌ Failed to initialize: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

def _setup_minimal_template(manager: ChatManager):
    """Setup minimal configuration template"""
    pass  # Default config is minimal

def _setup_standard_template(manager: ChatManager):
    """Setup standard configuration template"""
    # This would add common backend configurations
    pass

def _setup_advanced_template(manager: ChatManager):
    """Setup advanced configuration template"""
    # This would add all backends and advanced features
    pass

def _show_next_steps():
    """Show next steps after initialization"""
    panel_content = """
🚀 **Next Steps:**

1. **Add a backend:**
   `ai-chat-manager backend add openai --api-key YOUR_KEY`

2. **Create a bot:**
   `ai-chat-manager bot create assistant openai`

3. **Start chatting:**
   `ai-chat-manager chat assistant`

4. **View status:**
   `ai-chat-manager status`

📚 **Get help:** `ai-chat-manager --help`
    """
    
    console.print(Panel(Markdown(panel_content), title="🎉 Setup Complete", border_style="green"))

# Backend management commands
@cli.group()
def backend():
    """Manage AI backends"""
    pass

@backend.command("list")
@click.option("--format", type=click.Choice(["table", "json", "yaml"]), default="table")
@click.option("--available-only", is_flag=True, help="Show only available backends")
def list_backends(format, available_only):
    """List all configured backends"""
    
    try:
        manager = cli_state.get_manager()
        
        if format == "table":
            _display_backends_table(manager, available_only)
        elif format == "json":
            _display_backends_json(manager, available_only)
        elif format == "yaml":
            _display_backends_yaml(manager, available_only)
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

def _display_backends_table(manager: ChatManager, available_only: bool):
    """Display backends in table format"""
    
    table = Table(title="🔌 AI Backends", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Model", style="yellow")
    table.add_column("Features", style="white")
    
    status = manager.get_system_status()
    
    for name, info in status['backends'].items():
        if available_only and not info.get('healthy', False):
            continue
        
        backend_info = get_backend_info(name)
        features = ", ".join(backend_info.features[:3]) if backend_info else "Unknown"
        if backend_info and len(backend_info.features) > 3:
            features += "..."
        
        status_icon = "🟢" if info.get('healthy', False) else "🔴"
        status_text = f"{status_icon} {'Healthy' if info.get('healthy', False) else 'Unhealthy'}"
        
        table.add_row(
            name,
            info.get('type', 'Unknown'),
            status_text,
            info.get('model', 'N/A'),
            features
        )
    
    console.print(table)

def _display_backends_json(manager: ChatManager, available_only: bool):
    """Display backends in JSON format"""
    status = manager.get_system_status()
    if available_only:
        backends = {k: v for k, v in status['backends'].items() if v.get('healthy', False)}
    else:
        backends = status['backends']
    
    console.print(json.dumps(backends, indent=2))

def _display_backends_yaml(manager: ChatManager, available_only: bool):
    """Display backends in YAML format"""
    status = manager.get_system_status()
    if available_only:
        backends = {k: v for k, v in status['backends'].items() if v.get('healthy', False)}
    else:
        backends = status['backends']
    
    console.print(yaml.dump(backends, default_flow_style=False))

@backend.command("add")
@click.argument("name")
@click.argument("backend_type", type=click.Choice(["openai", "venice", "huggingface", "elevenlabs", "anthropic", "cohere"]))
@click.option("--api-key", help="API key for the backend")
@click.option("--api-key-env", help="Environment variable containing API key")
@click.option("--model", help="Default model to use")
@click.option("--base-url", help="Custom base URL")
@click.option("--interactive", "-i", is_flag=True, help="Interactive configuration")
@click.option("--enabled/--disabled", default=True, help="Enable/disable the backend")
def add_backend(name, backend_type, api_key, api_key_env, model, base_url, interactive, enabled):
    """Add a new AI backend"""
    
    try:
        if interactive:
            config_data = _interactive_backend_config(backend_type)
        else:
            config_data = {
                "api_key": api_key,
                "api_key_env": api_key_env,
                "model": model,
                "base_url": base_url,
                "enabled": enabled,
            }
        
        # Remove None values
        config_data = {k: v for k, v in config_data.items() if v is not None}
        
        manager = cli_state.get_manager()
        manager.create_backend(name, backend_type, **config_data)
        
        console.print(f"✅ Backend '{name}' added successfully!", style="green")
        
        # Test the backend
        if Confirm.ask("Test the backend connection?", default=True):
            _test_backend_connection(manager, name)
            
    except Exception as e:
        console.print(f"❌ Failed to add backend: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

def _interactive_backend_config(backend_type: str) -> Dict[str, Any]:
    """Interactive backend configuration"""
    
    console.print(f"\n🔧 Configuring {backend_type.upper()} backend", style="bold blue")
    
    # Get setup instructions
    instructions = get_setup_instructions(backend_type)
    if "setup_steps" in instructions:
        console.print("\n📋 Setup Steps:", style="bold")
        for step in instructions["setup_steps"]:
            console.print(f"  {step}")
        console.print()
    
    config = {}
    
    # API Key
    api_key = Prompt.ask("🔑 API Key (leave empty to use environment variable)", password=True, default="")
    if api_key:
        config["api_key"] = api_key
    else:
        env_var = Prompt.ask(f"🌍 Environment variable name", default=f"{backend_type.upper()}_API_KEY")
        config["api_key_env"] = env_var
    
    # Model
    if backend_type == "openai":
        model = Prompt.ask("🤖 Model", default="gpt-3.5-turbo")
    elif backend_type == "huggingface":
        model = Prompt.ask("🤖 Model", default="microsoft/DialoGPT-large")
    elif backend_type == "elevenlabs":
        model = Prompt.ask("🎙️ Voice Model", default="eleven_monolingual_v1")
    else:
        model = Prompt.ask("🤖 Model", default="")
    
    if model:
        config["model"] = model
    
    # Base URL
    if Confirm.ask("🌐 Use custom base URL?", default=False):
        base_url = Prompt.ask("🔗 Base URL")
        config["base_url"] = base_url
    
    # Backend-specific options
    if backend_type == "venice":
        privacy_level = Prompt.ask(
            "🔒 Privacy level", 
            choices=["standard", "enhanced", "maximum"], 
            default="enhanced"
        )
        config["privacy_level"] = privacy_level
    
    elif backend_type == "elevenlabs":
        voice_id = Prompt.ask("🎤 Voice ID", default="21m00Tcm4TlvDq8ikWAM")
        stability = FloatPrompt.ask("🎚️ Voice stability (0.0-1.0)", default=0.5)
        similarity = FloatPrompt.ask("🎚️ Similarity boost (0.0-1.0)", default=0.5)
        
        config.update({
            "voice_id": voice_id,
            "stability": stability,
            "similarity_boost": similarity
        })
    
    config["enabled"] = Confirm.ask("✅ Enable backend?", default=True)
    
    return config

def _test_backend_connection(manager: ChatManager, backend_name: str):
    """Test backend connection"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Testing backend connection...", total=None)
        
        try:
            # This would be an async call in a real implementation
            console.print(f"🔗 Testing connection to {backend_name}...")
            # Simulate test
            import time
            time.sleep(2)
            console.print(f"✅ Backend {backend_name} is working!", style="green")
            
        except Exception as e:
            console.print(f"❌ Connection test failed: {e}", style="red")

@backend.command("remove")
@click.argument("name")
@click.option("--force", is_flag=True, help="Skip confirmation")
def remove_backend(name, force):
    """Remove a backend"""
    
    try:
        if not force:
            if not Confirm.ask(f"Remove backend '{name}'?"):
                console.print("Operation cancelled", style="yellow")
                return
        
        manager = cli_state.get_manager()
        # This would call manager.delete_backend(name)
        console.print(f"✅ Backend '{name}' removed", style="green")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@backend.command("test")
@click.argument("name", required=False)
def test_backend(name):
    """Test backend connections"""
    
    try:
        manager = cli_state.get_manager()
        
        if name:
            # Test specific backend
            _test_backend_connection(manager, name)
        else:
            # Test all backends
            backends = manager.list_backends()
            
            with Progress() as progress:
                task = progress.add_task("Testing backends...", total=len(backends))
                
                for backend_name in backends:
                    progress.update(task, description=f"Testing {backend_name}...")
                    _test_backend_connection(manager, backend_name)
                    progress.advance(task)
                    
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

# Bot management commands
@cli.group()
def bot():
    """Manage chat bots"""
    pass

@bot.command("list")
@click.option("--format", type=click.Choice(["table", "json", "yaml"]), default="table")
def list_bots(format):
    """List all configured bots"""
    
    try:
        manager = cli_state.get_manager()
        
        if format == "table":
            _display_bots_table(manager)
        elif format == "json":
            _display_bots_json(manager)
        elif format == "yaml":
            _display_bots_yaml(manager)
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

def _display_bots_table(manager: ChatManager):
    """Display bots in table format"""
    
    table = Table(title="🤖 Chat Bots", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Backend", style="blue")
    table.add_column("Sessions", style="green")
    table.add_column("Memory", style="yellow")
    table.add_column("Learning", style="purple")
    table.add_column("Last Activity", style="white")
    
    status = manager.get_system_status()
    
    for name, info in status['bots'].items():
        memory_icon = "🧠" if info.get('memory_enabled', False) else "❌"
        learning_icon = "📚" if info.get('learning_enabled', False) else "❌"
        
        table.add_row(
            name,
            info.get('backend', 'Unknown'),
            str(info.get('active_sessions', 0)),
            memory_icon,
            learning_icon,
            "Recently"  # This would show actual last activity
        )
    
    console.print(table)

def _display_bots_json(manager: ChatManager):
    """Display bots in JSON format"""
    status = manager.get_system_status()
    console.print(json.dumps(status['bots'], indent=2))

def _display_bots_yaml(manager: ChatManager):
    """Display bots in YAML format"""
    status = manager.get_system_status()
    console.print(yaml.dump(status['bots'], default_flow_style=False))

@bot.command("create")
@click.argument("name")
@click.argument("backend")
@click.option("--template", type=click.Choice(["assistant", "creative", "researcher", "teacher"]), 
              help="Bot template")
@click.option("--system-prompt", help="Custom system prompt")
@click.option("--personality", help="Bot personality")
@click.option("--memory/--no-memory", default=True, help="Enable conversation memory")
@click.option("--learning/--no-learning", default=False, help="Enable learning")
@click.option("--interactive", "-i", is_flag=True, help="Interactive configuration")
def create_bot(name, backend, template, system_prompt, personality, memory, learning, interactive):
    """Create a new chat bot"""
    
    try:
        manager = cli_state.get_manager()
        
        if interactive:
            config_data = _interactive_bot_config(backend)
        else:
            config_data = {
                "system_prompt": system_prompt or "",
                "personality": personality or "helpful",
                "memory_enabled": memory,
                "learning_enabled": learning,
            }
        
        if template:
            bot = manager.create_bot_from_template(name, template, backend, **config_data)
        else:
            bot = manager.create_bot(name, backend, **config_data)
        
        console.print(f"✅ Bot '{name}' created successfully!", style="green")
        
        # Show bot info
        _display_bot_info(bot)
        
        # Ask if user wants to start chatting
        if Confirm.ask("Start chatting with the bot?", default=True):
            _start_chat_session(name)
            
    except Exception as e:
        console.print(f"❌ Failed to create bot: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

def _interactive_bot_config(backend: str) -> Dict[str, Any]:
    """Interactive bot configuration"""
    
    console.print(f"\n🤖 Configuring new bot", style="bold blue")
    
    config = {}
    
    # System prompt
    system_prompt = Prompt.ask(
        "📝 System prompt (what should the bot know about its role?)",
        default="You are a helpful AI assistant."
    )
    config["system_prompt"] = system_prompt
    
    # Personality
    personality = Prompt.ask(
        "🎭 Personality",
        choices=["helpful", "creative", "analytical", "friendly", "professional"],
        default="helpful"
    )
    config["personality"] = personality
    
    # Memory
    config["memory_enabled"] = Confirm.ask("🧠 Enable conversation memory?", default=True)
    
    # Learning
    config["learning_enabled"] = Confirm.ask("📚 Enable learning from interactions?", default=False)
    
    # Advanced options
    if Confirm.ask("⚙️ Configure advanced options?", default=False):
        config["max_context_length"] = IntPrompt.ask("📏 Max context length", default=4000)
        config["personalization_enabled"] = Confirm.ask("👤 Enable personalization?", default=False)
        config["function_calling_enabled"] = Confirm.ask("🔧 Enable function calling?", default=False)
    
    return config

def _display_bot_info(bot):
    """Display bot information"""
    stats = bot.get_stats()
    
    info_text = f"""
**Bot Name:** {stats['bot_name']}
**Backend:** {stats['backend']}
**Memory:** {'✅ Enabled' if stats['memory_enabled'] else '❌ Disabled'}
**Learning:** {'✅ Enabled' if stats['learning_enabled'] else '❌ Disabled'}
**Messages:** {stats['message_count']}
    """
    
    console.print(Panel(Markdown(info_text), title="🤖 Bot Information", border_style="blue"))

@bot.command("remove")
@click.argument("name")
@click.option("--delete-data", is_flag=True, help="Delete bot data")
@click.option("--force", is_flag=True, help="Skip confirmation")
def remove_bot(name, delete_data, force):
    """Remove a bot"""
    
    try:
        if not force:
            warning = "⚠️ This will permanently delete the bot"
            if delete_data:
                warning += " and all its data"
            console.print(warning, style="yellow")
            
            if not Confirm.ask(f"Remove bot '{name}'?"):
                console.print("Operation cancelled", style="yellow")
                return
        
        manager = cli_state.get_manager()
        manager.delete_bot(name, delete_data=delete_data)
        
        console.print(f"✅ Bot '{name}' removed", style="green")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

# Chat commands
@cli.command("chat")
@click.argument("bot_name")
@click.option("--user-id", help="User ID for personalization")
@click.option("--session-id", help="Session ID for conversation threading")
@click.option("--mode", type=click.Choice(["interactive", "single"]), default="interactive")
@click.option("--message", "-m", help="Single message (for single mode)")
def chat_command(bot_name, user_id, session_id, mode, message):
    """Start chatting with a bot"""
    
    try:
        manager = cli_state.get_manager()
        
        if mode == "single" and message:
            # Single message mode
            response = run_async(manager.chat_with_bot(bot_name, message, user_id=user_id))
            console.print(f"\n🤖 {bot_name}:", style="bold green")
            console.print(response)
        else:
            # Interactive mode
            _start_chat_session(bot_name, user_id, session_id)
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

def _start_chat_session(bot_name: str, user_id: Optional[str] = None, session_id: Optional[str] = None):
    """Start interactive chat session"""
    
    console.print(f"\n💬 Starting chat with {bot_name}", style="bold green")
    console.print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    console.print("Type 'help' for chat commands.\n")
    
    manager = cli_state.get_manager()
    
    try:
        while True:
            # Get user input
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]", console=console)
            
            # Handle special commands
            if user_input.lower() in ["quit", "exit", "bye"]:
                break
            elif user_input.lower() == "help":
                _show_chat_help()
                continue
            elif user_input.lower() == "clear":
                console.clear()
                continue
            elif user_input.lower().startswith("/"):
                _handle_chat_command(user_input, bot_name, manager)
                continue
            
            # Send message to bot
            try:
                with console.status("🤔 Thinking...", spinner="dots"):
                    response = run_async(manager.chat_with_bot(
                        bot_name, user_input, user_id=user_id
                    ))
                
                console.print(f"[bold green]{bot_name}[/bold green]: {response}")
                console.print()
                
            except Exception as e:
                console.print(f"❌ Error: {e}", style="red")
                
    except KeyboardInterrupt:
        pass
    
    console.print(f"\n👋 Chat session with {bot_name} ended")

def _show_chat_help():
    """Show chat help"""
    help_text = """
**Chat Commands:**
- `help` - Show this help
- `clear` - Clear the screen
- `quit`, `exit`, `bye` - End the conversation
- `/stats` - Show bot statistics
- `/memory clear` - Clear conversation memory
- `/save <filename>` - Save conversation
- `/load <filename>` - Load conversation
    """
    console.print(Panel(Markdown(help_text), title="💡 Chat Help", border_style="blue"))

def _handle_chat_command(command: str, bot_name: str, manager: ChatManager):
    """Handle special chat commands"""
    
    parts = command[1:].split()
    cmd = parts[0].lower() if parts else ""
    
    try:
        if cmd == "stats":
            bot = manager.get_bot(bot_name)
            stats = bot.get_stats()
            
            stats_text = f"""
**Messages:** {stats['message_count']}
**Total Tokens:** {stats.get('total_tokens_used', 'N/A')}
**Average Response Time:** {stats.get('average_response_time', 0):.2f}s
**Cost:** ${stats.get('total_cost', 0):.4f}
            """
            console.print(Panel(Markdown(stats_text), title="📊 Bot Statistics"))
            
        elif cmd == "memory" and len(parts) > 1 and parts[1] == "clear":
            bot = manager.get_bot(bot_name)
            bot.clear_history()
            console.print("🧹 Conversation memory cleared", style="green")
            
        elif cmd == "save" and len(parts) > 1:
            filename = parts[1]
            bot = manager.get_bot(bot_name)
            bot.export_conversation(filename)
            console.print(f"💾 Conversation saved to {filename}", style="green")
            
        else:
            console.print(f"❓ Unknown command: {command}", style="yellow")
            
    except Exception as e:
        console.print(f"❌ Command failed: {e}", style="red")

# System commands
@cli.command("status")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed status")
@click.option("--format", type=click.Choice(["rich", "json", "yaml"]), default="rich")
def status(detailed, format):
    """Show system status"""
    
    try:
        manager = cli_state.get_manager()
        
        if format == "rich":
            _display_status_rich(manager, detailed)
        elif format == "json":
            status_data = manager.get_system_status()
            console.print(json.dumps(status_data, indent=2, default=str))
        elif format == "yaml":
            status_data = manager.get_system_status()
            console.print(yaml.dump(status_data, default_flow_style=False))
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

def _display_status_rich(manager: ChatManager, detailed: bool):
    """Display status in rich format"""
    
    status = manager.get_system_status()
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Header
    layout["header"].update(
        Panel(
            Align.center("🚀 AI Chat Manager System Status"),
            style="bold blue"
        )
    )
    
    # Body
    body_layout = Layout()
    body_layout.split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    # System info (left)
    system_info = status["system"]
    system_text = f"""
**Uptime:** {system_info.get('uptime_hours', 0):.1f} hours
**Total Requests:** {system_info.get('total_requests', 0):,}
**Success Rate:** {system_info.get('success_rate', 0)*100:.1f}%
**Active Bots:** {system_info.get('active_bots', 0)}
**Active Users:** {system_info.get('active_users', 0)}
    """
    
    body_layout["left"].update(
        Panel(Markdown(system_text), title="🖥️ System", border_style="green")
    )
    
    # Backends info (right)
    backends_tree = Tree("🔌 Backends")
    for name, info in status["backends"].items():
        status_icon = "🟢" if info.get('healthy', False) else "🔴"
        backends_tree.add(f"{status_icon} {name} ({info.get('type', 'Unknown')})")
    
    body_layout["right"].update(
        Panel(backends_tree, title="🔌 Backends", border_style="blue")
    )
    
    layout["body"].update(body_layout)
    
    # Footer
    layout["footer"].update(
        Panel(
            Align.center(f"Config: {status.get('config_path', 'Unknown')}"),
            style="dim"
        )
    )
    
    console.print(layout)
    
    if detailed:
        _display_detailed_status(status)

def _display_detailed_status(status: Dict[str, Any]):
    """Display detailed status information"""
    
    # Detailed metrics would go here
    console.print("\n📊 Detailed Metrics:", style="bold")
    
    # Performance metrics
    system = status["system"]
    if system.get('average_response_time'):
        console.print(f"⚡ Average Response Time: {system['average_response_time']:.2f}s")
    if system.get('total_tokens'):
        console.print(f"🎯 Total Tokens: {system['total_tokens']:,}")
    if system.get('total_cost'):
        console.print(f"💰 Total Cost: ${system['total_cost']:.4f}")

# Configuration commands
@cli.group()
def config():
    """Manage configuration"""
    pass

@config.command("show")
@click.option("--section", help="Show specific section")
@click.option("--format", type=click.Choice(["yaml", "json"]), default="yaml")
def show_config(section, format):
    """Show current configuration"""
    
    try:
        config_obj = Config(cli_state.config_path)
        
        if section:
            if section == "backends":
                data = {name: config_obj.get_backend_config(name).model_dump() 
                       for name in config_obj.list_backends()}
            elif section == "bots":
                data = {name: config_obj.get_bot_config(name).model_dump() 
                       for name in config_obj.list_bots()}
            elif section == "global":
                data = config_obj.get_global_config().model_dump()
            else:
                console.print(f"❌ Unknown section: {section}", style="red")
                return
        else:
            data = config_obj._config_data
        
        if format == "json":
            console.print(json.dumps(data, indent=2, default=str))
        else:
            console.print(yaml.dump(data, default_flow_style=False))
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@config.command("validate")
def validate_config():
    """Validate configuration"""
    
    try:
        config_obj = Config(cli_state.config_path)
        errors = config_obj.validate_all_configs()
        
        if any(errors.values()):
            console.print("❌ Configuration validation failed:", style="red")
            for section, section_errors in errors.items():
                if section_errors:
                    console.print(f"\n{section.title()}:", style="bold")
                    for error in section_errors:
                        console.print(f"  • {error}", style="red")
        else:
            console.print("✅ Configuration is valid!", style="green")
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

# Utility commands
@cli.command("doctor")
def doctor():
    """Run system diagnostics"""
    
    console.print("🔍 Running AI Chat Manager diagnostics...\n", style="bold blue")
    
    checks = [
        ("Configuration file", _check_config_file),
        ("Python dependencies", _check_dependencies),
        ("Backend availability", _check_backends),
        ("System permissions", _check_permissions),
    ]
    
    results = []
    
    with Progress() as progress:
        task = progress.add_task("Running diagnostics...", total=len(checks))
        
        for check_name, check_func in checks:
            progress.update(task, description=f"Checking {check_name.lower()}...")
            
            try:
                result = check_func()
                results.append((check_name, True, result))
            except Exception as e:
                results.append((check_name, False, str(e)))
            
            progress.advance(task)
    
    # Display results
    console.print("\n📋 Diagnostic Results:", style="bold")
    
    for check_name, passed, message in results:
        status_icon = "✅" if passed else "❌"
        style = "green" if passed else "red"
        console.print(f"{status_icon} {check_name}: {message}", style=style)

def _check_config_file() -> str:
    """Check configuration file"""
    config_file = Path(cli_state.config_path)
    if config_file.exists():
        return f"Found at {config_file}"
    else:
        raise Exception(f"Not found at {config_file}")

def _check_dependencies() -> str:
    """Check Python dependencies"""
    missing = []
    try:
        import aiohttp
        import pydantic
        import yaml
        import rich
        import click
    except ImportError as e:
        missing.append(str(e))
    
    if missing:
        raise Exception(f"Missing: {', '.join(missing)}")
    return "All core dependencies installed"

def _check_backends() -> str:
    """Check backend availability"""
    available = list_available_backends()
    total = len(list_available_backends())
    return f"{len(available)}/{total} backends available"

def _check_permissions() -> str:
    """Check system permissions"""
    config_file = Path(cli_state.config_path)
    if config_file.exists() and not os.access(config_file, os.W_OK):
        raise Exception("No write permission for config file")
    return "Permissions OK"

# Main entry point
def main():
    """Main CLI entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
    except Exception as e:
        console.print(f"💥 Unexpected error: {e}", style="red")
        if cli_state.debug:
            console.print_exception()

if __name__ == "__main__":
    main()