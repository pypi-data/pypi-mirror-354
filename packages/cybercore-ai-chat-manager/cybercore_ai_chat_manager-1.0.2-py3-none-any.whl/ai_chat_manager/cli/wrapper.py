#!/usr/bin/env python3
"""
Enhanced CLI Wrapper for AI Chat Manager

This wrapper provides simplified commands, automation features, configuration wizards,
and convenience functions for easier interaction with the AI Chat Manager system.
"""

import asyncio
import click
import json
import os
import sys
import yaml
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.tree import Tree
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns

# Import main CLI and core components
from .main import cli as main_cli
from ..core.manager import ChatManager
from ..core.config import Config, BackendConfig, BotConfig
from ..backends import list_available_backends, get_backend_info

console = Console()

class CLIWrapper:
    """Enhanced CLI wrapper with convenience features"""
    
    def __init__(self):
        self.config_profiles = {}
        self.shortcuts = {}
        self.automation_scripts = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load configuration profiles"""
        profiles_file = Path.home() / ".ai_chat_manager" / "profiles.json"
        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    self.config_profiles = json.load(f)
            except Exception as e:
                console.print(f"⚠️ Failed to load profiles: {e}", style="yellow")
    
    def save_profiles(self):
        """Save configuration profiles"""
        profiles_dir = Path.home() / ".ai_chat_manager"
        profiles_dir.mkdir(exist_ok=True)
        profiles_file = profiles_dir / "profiles.json"
        
        try:
            with open(profiles_file, 'w') as f:
                json.dump(self.config_profiles, f, indent=2, default=str)
        except Exception as e:
            console.print(f"⚠️ Failed to save profiles: {e}", style="yellow")

# Global wrapper instance
wrapper = CLIWrapper()

# Custom Click group for wrapper commands
class WrapperGroup(click.Group):
    """Enhanced Click group for wrapper commands"""
    
    def format_help(self, ctx, formatter):
        formatter.write_heading("AI Chat Manager - Enhanced CLI Wrapper")
        formatter.write_paragraph()
        formatter.write("Simplified commands and automation tools for AI Chat Manager.")
        formatter.write_paragraph()
        
        super().format_help(ctx, formatter)

@click.group(cls=WrapperGroup)
@click.version_option(version="0.2.0", prog_name="AI Chat Manager Wrapper")
def cli():
    """AI Chat Manager Enhanced CLI Wrapper"""
    pass

# Quick setup commands
@cli.group()
def quick():
    """Quick setup and common operations"""
    pass

@quick.command("start")
@click.option("--provider", type=click.Choice(["openai", "venice", "huggingface"]), 
              help="AI provider to use")
@click.option("--profile", help="Configuration profile to use")
def quick_start(provider, profile):
    """Quick start setup wizard"""
    
    console.print("🚀 Welcome to AI Chat Manager Quick Start!", style="bold blue")
    console.print()
    
    # Check if already configured
    config_file = Path("config.yaml")
    if config_file.exists() and not Confirm.ask("Configuration exists. Reconfigure?"):
        console.print("✅ Using existing configuration", style="green")
        return
    
    # Use profile if specified
    if profile and profile in wrapper.config_profiles:
        _apply_profile(profile)
        return
    
    # Interactive setup
    console.print("Let's set up your first AI backend and bot!\n")
    
    # Choose provider
    if not provider:
        providers = {
            "1": "openai",
            "2": "venice", 
            "3": "huggingface"
        }
        
        console.print("Available providers:")
        console.print("1. OpenAI (GPT-3.5, GPT-4)")
        console.print("2. Venice AI (Privacy-focused)")
        console.print("3. HuggingFace (Open source models)")
        
        choice = Prompt.ask("Choose provider", choices=["1", "2", "3"], default="1")
        provider = providers[choice]
    
    # Get API key
    api_key_env = f"{provider.upper()}_API_KEY"
    api_key = os.getenv(api_key_env)
    
    if not api_key:
        console.print(f"💡 Set your API key: export {api_key_env}=your_key")
        api_key = Prompt.ask(f"Or enter {provider} API key", password=True)
        
        if not api_key:
            console.print("❌ API key required for setup", style="red")
            return
    
    # Quick setup
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Setting up AI Chat Manager...", total=None)
        
        try:
            # Initialize
            progress.update(task, description="Initializing configuration...")
            manager = ChatManager("config.yaml")
            
            # Add backend
            progress.update(task, description=f"Adding {provider} backend...")
            backend_config = _get_provider_config(provider, api_key)
            manager.create_backend(provider, provider, **backend_config)
            
            # Create default bot
            progress.update(task, description="Creating assistant bot...")
            manager.create_bot(
                name="assistant",
                backend=provider,
                system_prompt="You are a helpful AI assistant. Be friendly and informative.",
                memory_enabled=True
            )
            
            progress.update(task, description="Finalizing setup...")
            
        except Exception as e:
            console.print(f"❌ Setup failed: {e}", style="red")
            return
    
    console.print("✅ Setup complete!", style="green")
    console.print("\n🎯 Quick commands to try:")
    console.print("• acm-wrapper chat assistant")
    console.print("• acm-wrapper quick status")
    console.print("• acm-wrapper templates list")
    
    # Save as profile
    if Confirm.ask("Save this setup as a profile?", default=True):
        profile_name = Prompt.ask("Profile name", default=f"{provider}_default")
        _save_current_as_profile(profile_name, provider, api_key)

def _get_provider_config(provider: str, api_key: str) -> Dict[str, Any]:
    """Get provider-specific configuration"""
    configs = {
        "openai": {
            "api_key": api_key,
            "model": "gpt-3.5-turbo",
            "supports_streaming": True,
            "supports_functions": True
        },
        "venice": {
            "api_key": api_key,
            "privacy_level": "enhanced",
            "anonymous_mode": True
        },
        "huggingface": {
            "api_key": api_key,
            "model": "microsoft/DialoGPT-large"
        }
    }
    return configs.get(provider, {"api_key": api_key})

def _apply_profile(profile_name: str):
    """Apply a saved configuration profile"""
    profile = wrapper.config_profiles.get(profile_name)
    if not profile:
        console.print(f"❌ Profile '{profile_name}' not found", style="red")
        return
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Applying profile...", total=None)
        
        try:
            manager = ChatManager("config.yaml")
            
            # Apply backend configuration
            for backend_name, backend_config in profile.get("backends", {}).items():
                progress.update(task, description=f"Setting up {backend_name}...")
                manager.create_backend(backend_name, backend_config["type"], **backend_config["config"])
            
            # Apply bot configuration
            for bot_name, bot_config in profile.get("bots", {}).items():
                progress.update(task, description=f"Creating {bot_name}...")
                manager.create_bot(bot_name, **bot_config)
            
        except Exception as e:
            console.print(f"❌ Failed to apply profile: {e}", style="red")
            return
    
    console.print(f"✅ Profile '{profile_name}' applied successfully!", style="green")

def _save_current_as_profile(name: str, provider: str, api_key: str):
    """Save current configuration as a profile"""
    profile = {
        "name": name,
        "created": datetime.now().isoformat(),
        "backends": {
            provider: {
                "type": provider,
                "config": _get_provider_config(provider, api_key)
            }
        },
        "bots": {
            "assistant": {
                "backend": provider,
                "system_prompt": "You are a helpful AI assistant.",
                "memory_enabled": True
            }
        }
    }
    
    wrapper.config_profiles[name] = profile
    wrapper.save_profiles()
    console.print(f"💾 Profile '{name}' saved!", style="green")

@quick.command("chat")
@click.argument("bot_name", default="assistant")
@click.option("--model", help="Override model for this session")
@click.option("--system", help="Override system prompt")
@click.option("--bot", "-b", help="Bot to use (alternative to bot_name argument)")
def quick_chat(bot_name, model, system, bot):
    """Start quick chat session with enhanced features"""
    
    # Use --bot flag if provided, otherwise use argument
    if bot:
        bot_name = bot
    
    try:
        manager = ChatManager("config.yaml")
        
        # Check if bot exists
        if bot_name not in manager.list_bots():
            console.print(f"❌ Bot '{bot_name}' not found", style="red")
            
            available_bots = manager.list_bots()
            if available_bots:
                console.print("Available bots:")
                for bot in available_bots:
                    console.print(f"  • {bot}")
            else:
                console.print("💡 Run 'acm-wrapper quick start' to create your first bot")
            return
        
        # Enhanced chat interface
        _start_enhanced_chat(manager, bot_name, model, system)
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

def _start_enhanced_chat(manager: ChatManager, bot_name: str, model: Optional[str], system: Optional[str]):
    """Start enhanced chat session with additional features"""
    
    console.print(f"💬 Enhanced Chat with {bot_name}", style="bold green")
    console.print("Enhanced features: /help, /save, /load, /stats, /retry, /model")
    console.print("Type 'quit' to exit\n")
    
    chat_history = []
    current_model = model
    
    try:
        while True:
            # Get user input with enhanced prompt
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]", console=console)
            
            # Handle enhanced commands
            if user_input.lower() in ["quit", "exit", "bye"]:
                break
            elif user_input.startswith("/"):
                result = _handle_enhanced_command(user_input, manager, bot_name, chat_history, current_model)
                if result:
                    current_model = result.get("model", current_model)
                continue
            
            # Store user message
            chat_history.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            
            # Send to bot with enhanced features
            try:
                with console.status("🤔 Thinking...", spinner="dots"):
                    kwargs = {}
                    if current_model:
                        kwargs["model"] = current_model
                    
                    response = asyncio.run(manager.chat_with_bot(bot_name, user_input, **kwargs))
                
                # Display response with formatting
                console.print(f"[bold green]{bot_name}[/bold green]: {response}")
                console.print()
                
                # Store response
                chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                
            except Exception as e:
                console.print(f"❌ Error: {e}", style="red")
                
                # Offer retry
                if Confirm.ask("Retry with different settings?", default=False):
                    # Could implement retry logic here
                    pass
                
    except KeyboardInterrupt:
        pass
    
    console.print(f"\n👋 Chat with {bot_name} ended")
    
    # Offer to save chat
    if chat_history and Confirm.ask("Save this conversation?", default=False):
        filename = f"chat_{bot_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(chat_history, f, indent=2, default=str)
        console.print(f"💾 Conversation saved to {filename}", style="green")

def _handle_enhanced_command(command: str, manager: ChatManager, bot_name: str, 
                           chat_history: List[Dict], current_model: Optional[str]) -> Optional[Dict]:
    """Handle enhanced chat commands"""
    
    parts = command[1:].split()
    cmd = parts[0].lower() if parts else ""
    
    try:
        if cmd == "help":
            help_text = """
**Enhanced Chat Commands:**
- `/help` - Show this help
- `/stats` - Show conversation statistics
- `/save <filename>` - Save conversation
- `/load <filename>` - Load conversation
- `/retry` - Retry last message
- `/model <model_name>` - Switch model
- `/clear` - Clear conversation history
- `/export` - Export in different formats
- `/summary` - Get conversation summary
            """
            console.print(Panel(Markdown(help_text), title="💡 Enhanced Commands"))
            
        elif cmd == "stats":
            _show_chat_stats(chat_history, bot_name)
            
        elif cmd == "save" and len(parts) > 1:
            filename = parts[1]
            with open(filename, 'w') as f:
                json.dump(chat_history, f, indent=2, default=str)
            console.print(f"💾 Saved to {filename}", style="green")
            
        elif cmd == "load" and len(parts) > 1:
            filename = parts[1]
            if Path(filename).exists():
                with open(filename, 'r') as f:
                    loaded_history = json.load(f)
                chat_history.extend(loaded_history)
                console.print(f"📂 Loaded from {filename}", style="green")
            else:
                console.print(f"❌ File {filename} not found", style="red")
                
        elif cmd == "model":
            if len(parts) > 1:
                new_model = parts[1]
                console.print(f"🔄 Switched to model: {new_model}", style="green")
                return {"model": new_model}
            else:
                console.print(f"📋 Current model: {current_model or 'default'}")
                
        elif cmd == "clear":
            if Confirm.ask("Clear conversation history?"):
                chat_history.clear()
                console.print("🧹 History cleared", style="green")
                
        elif cmd == "export":
            _export_conversation(chat_history, bot_name)
            
        elif cmd == "summary":
            _show_conversation_summary(chat_history)
            
        else:
            console.print(f"❓ Unknown command: {command}", style="yellow")
            
    except Exception as e:
        console.print(f"❌ Command failed: {e}", style="red")
    
    return None

def _show_chat_stats(chat_history: List[Dict], bot_name: str):
    """Show conversation statistics"""
    if not chat_history:
        console.print("📊 No messages yet", style="yellow")
        return
    
    user_messages = [msg for msg in chat_history if msg["role"] == "user"]
    bot_messages = [msg for msg in chat_history if msg["role"] == "assistant"]
    
    total_chars = sum(len(msg["content"]) for msg in chat_history)
    avg_user_length = sum(len(msg["content"]) for msg in user_messages) / len(user_messages) if user_messages else 0
    avg_bot_length = sum(len(msg["content"]) for msg in bot_messages) / len(bot_messages) if bot_messages else 0
    
    if chat_history:
        duration = chat_history[-1]["timestamp"] - chat_history[0]["timestamp"]
        duration_minutes = duration.total_seconds() / 60
    else:
        duration_minutes = 0
    
    stats_text = f"""
**Conversation Statistics**

📈 **Messages**: {len(chat_history)} total ({len(user_messages)} user, {len(bot_messages)} {bot_name})
⏱️ **Duration**: {duration_minutes:.1f} minutes
📝 **Characters**: {total_chars:,} total
📏 **Average Length**: User {avg_user_length:.0f}, {bot_name} {avg_bot_length:.0f} chars
🤖 **Bot**: {bot_name}
    """
    
    console.print(Panel(Markdown(stats_text), title="📊 Chat Statistics"))

def _export_conversation(chat_history: List[Dict], bot_name: str):
    """Export conversation in different formats"""
    if not chat_history:
        console.print("📊 No conversation to export", style="yellow")
        return
    
    formats = {
        "1": ("JSON", "json"),
        "2": ("Markdown", "md"),
        "3": ("Plain Text", "txt"),
        "4": ("CSV", "csv")
    }
    
    console.print("Export formats:")
    for key, (name, ext) in formats.items():
        console.print(f"{key}. {name}")
    
    choice = Prompt.ask("Choose format", choices=list(formats.keys()), default="1")
    format_name, ext = formats[choice]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"chat_{bot_name}_{timestamp}.{ext}"
    
    try:
        if ext == "json":
            with open(filename, 'w') as f:
                json.dump(chat_history, f, indent=2, default=str)
        
        elif ext == "md":
            with open(filename, 'w') as f:
                f.write(f"# Conversation with {bot_name}\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for msg in chat_history:
                    role = "**You**" if msg["role"] == "user" else f"**{bot_name}**"
                    f.write(f"{role}: {msg['content']}\n\n")
        
        elif ext == "txt":
            with open(filename, 'w') as f:
                f.write(f"Conversation with {bot_name}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for msg in chat_history:
                    role = "You" if msg["role"] == "user" else bot_name
                    f.write(f"{role}: {msg['content']}\n\n")
        
        elif ext == "csv":
            import csv
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "role", "content"])
                for msg in chat_history:
                    writer.writerow([msg["timestamp"], msg["role"], msg["content"]])
        
        console.print(f"✅ Exported to {filename}", style="green")
        
    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="red")

def _show_conversation_summary(chat_history: List[Dict]):
    """Show AI-generated conversation summary"""
    if not chat_history:
        console.print("📊 No conversation to summarize", style="yellow")
        return
    
    # Simple keyword-based summary (could be enhanced with AI)
    user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]
    
    # Extract common words/topics
    all_text = " ".join(user_messages).lower()
    words = all_text.split()
    
    # Simple topic extraction
    topics = []
    common_topics = ["python", "programming", "ai", "help", "question", "problem", "code", "data", "machine learning"]
    for topic in common_topics:
        if topic in all_text:
            topics.append(topic)
    
    summary_text = f"""
**Conversation Summary**

📝 **Total Messages**: {len(chat_history)}
🎯 **Topics Discussed**: {', '.join(topics[:5]) if topics else 'General conversation'}
💬 **User Questions**: {len(user_messages)}
⏱️ **Duration**: {(chat_history[-1]['timestamp'] - chat_history[0]['timestamp']).total_seconds() / 60:.1f} minutes
    """
    
    console.print(Panel(Markdown(summary_text), title="📋 Summary"))

@quick.command("status")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed status")
@click.option("--bot", "-b", help="Show status for specific bot")
def quick_status(detailed, bot):
    """Show quick system status"""
    
    try:
        manager = ChatManager("config.yaml")
        status = manager.get_system_status()
        
        # If specific bot requested, show bot-specific status
        if bot:
            if bot not in status["bots"]:
                console.print(f"❌ Bot '{bot}' not found", style="red")
                available_bots = list(status["bots"].keys())
                if available_bots:
                    console.print(f"Available bots: {', '.join(available_bots)}")
                return
            
            _show_bot_status(manager, bot, detailed)
            return
        
        # Quick status display
        console.print("🚀 AI Chat Manager Status", style="bold blue")
        console.print()
        
        # System overview
        system = status["system"]
        console.print(f"⏱️ Uptime: {system.get('uptime_hours', 0):.1f} hours")
        console.print(f"📊 Requests: {system.get('total_requests', 0):,} ({system.get('success_rate', 0)*100:.1f}% success)")
        console.print(f"🤖 Active Bots: {system.get('active_bots', 0)}")
        console.print(f"👥 Active Users: {system.get('active_users', 0)}")
        
        # Backends status
        console.print(f"\n🔌 Backends ({len(status['backends'])}):")
        for name, info in status["backends"].items():
            status_icon = "🟢" if info.get('healthy', False) else "🔴"
            console.print(f"  {status_icon} {name} ({info.get('type', 'Unknown')})")
        
        # Bots status  
        console.print(f"\n🤖 Bots ({len(status['bots'])}):")
        for name, info in status["bots"].items():
            memory_icon = "🧠" if info.get('memory_enabled', False) else "💭"
            console.print(f"  {memory_icon} {name} → {info.get('backend', 'Unknown')}")
        
        if detailed:
            console.print(f"\n📁 Config: {status.get('config_path', 'Unknown')}")
            
            # Additional metrics
            if system.get('average_response_time'):
                console.print(f"⚡ Avg Response: {system['average_response_time']:.2f}s")
            if system.get('total_cost'):
                console.print(f"💰 Total Cost: ${system['total_cost']:.4f}")
        
    except Exception as e:
        console.print(f"❌ Error getting status: {e}", style="red")

# Template management
@cli.group()
def templates():
    """Bot template management"""
    pass

@templates.command("list")
def list_templates():
    """List available bot templates"""
    
    templates_info = {
        "assistant": {
            "description": "General purpose helpful assistant",
            "features": ["memory", "general knowledge", "helpful responses"],
            "use_case": "General assistance and Q&A"
        },
        "creative": {
            "description": "Creative writing and ideation assistant",
            "features": ["creative writing", "brainstorming", "storytelling"],
            "use_case": "Content creation, writing help"
        },
        "researcher": {
            "description": "Research and analysis specialist",
            "features": ["fact-checking", "analysis", "citations"],
            "use_case": "Research projects, data analysis"
        },
        "teacher": {
            "description": "Educational tutor and explainer",
            "features": ["explanations", "examples", "patient teaching"],
            "use_case": "Learning, education, skill development"
        }
    }
    
    console.print("🎭 Available Bot Templates", style="bold blue")
    console.print()
    
    for name, info in templates_info.items():
        console.print(f"**{name.title()}**", style="bold green")
        console.print(f"  📝 {info['description']}")
        console.print(f"  ✨ Features: {', '.join(info['features'])}")
        console.print(f"  🎯 Use case: {info['use_case']}")
        console.print()

@templates.command("create")
@click.argument("bot_name")
@click.argument("template", type=click.Choice(["assistant", "creative", "researcher", "teacher"]))
@click.option("--backend", help="Backend to use", default="openai")
@click.option("--customize", "-c", is_flag=True, help="Customize template settings")
def create_from_template(bot_name, template, backend, customize):
    """Create bot from template with optional customization"""
    
    try:
        manager = ChatManager("config.yaml")
        
        # Check if backend exists
        if backend not in manager.list_backends():
            console.print(f"❌ Backend '{backend}' not found", style="red")
            available = manager.list_backends()
            if available:
                console.print(f"Available backends: {', '.join(available)}")
            return
        
        # Get template customizations
        overrides = {}
        if customize:
            overrides = _get_template_customizations(template)
        
        # Create bot
        with console.status(f"Creating {template} bot..."):
            bot = manager.create_bot_from_template(
                name=bot_name,
                template=template,
                backend=backend,
                **overrides
            )
        
        console.print(f"✅ Created {template} bot '{bot_name}'!", style="green")
        
        # Show bot info
        stats = bot.get_stats()
        info_text = f"""
**Bot Created Successfully!**

🤖 **Name**: {bot_name}
🎭 **Template**: {template}
🔌 **Backend**: {backend}
🧠 **Memory**: {'✅' if stats['memory_enabled'] else '❌'}
📚 **Learning**: {'✅' if stats['learning_enabled'] else '❌'}
        """
        
        console.print(Panel(Markdown(info_text), title="🎉 Bot Ready"))
        
        # Offer to start chatting
        if Confirm.ask(f"Start chatting with {bot_name}?", default=True):
            _start_enhanced_chat(manager, bot_name, None, None)
            
    except Exception as e:
        console.print(f"❌ Failed to create bot: {e}", style="red")

def _get_template_customizations(template: str) -> Dict[str, Any]:
    """Get customizations for a template"""
    console.print(f"\n🎨 Customizing {template} template")
    
    overrides = {}
    
    # Common customizations
    if Confirm.ask("Customize system prompt?", default=False):
        prompt = Prompt.ask("System prompt")
        overrides["system_prompt"] = prompt
    
    if Confirm.ask("Enable learning from interactions?", default=False):
        overrides["learning_enabled"] = True
    
    if Confirm.ask("Enable personalization?", default=False):
        overrides["personalization_enabled"] = True
    
    # Template-specific customizations
    if template == "creative":
        if Confirm.ask("High creativity (temperature 0.9)?", default=True):
            overrides["temperature"] = 0.9
    
    elif template == "researcher":
        if Confirm.ask("Enable web search capabilities?", default=False):
            overrides["web_search_enabled"] = True
    
    elif template == "teacher":
        if Confirm.ask("Enable adaptive difficulty?", default=True):
            overrides["personalization_enabled"] = True
    
    return overrides

# Profile management
@cli.group()
def profiles():
    """Configuration profile management"""
    pass

@profiles.command("list")
def list_profiles():
    """List saved configuration profiles"""
    
    if not wrapper.config_profiles:
        console.print("📋 No profiles saved yet", style="yellow")
        console.print("💡 Create profiles with 'acm-wrapper profiles save <name>'")
        return
    
    table = Table(title="📋 Configuration Profiles")
    table.add_column("Name", style="cyan")
    table.add_column("Backends", style="blue")
    table.add_column("Bots", style="green")
    table.add_column("Created", style="white")
    
    for name, profile in wrapper.config_profiles.items():
        backends = ", ".join(profile.get("backends", {}).keys())
        bots = ", ".join(profile.get("bots", {}).keys())
        created = profile.get("created", "Unknown")
        
        if isinstance(created, str) and "T" in created:
            created = datetime.fromisoformat(created).strftime("%Y-%m-%d")
        
        table.add_row(name, backends, bots, created)
    
    console.print(table)

@profiles.command("save")
@click.argument("name")
@click.option("--description", help="Profile description")
def save_profile(name, description):
    """Save current configuration as profile"""
    
    try:
        config = Config("config.yaml")
        
        # Build profile from current config
        profile = {
            "name": name,
            "description": description or f"Profile saved on {datetime.now().strftime('%Y-%m-%d')}",
            "created": datetime.now().isoformat(),
            "backends": {},
            "bots": {}
        }
        
        # Save backend configs
        for backend_name in config.list_backends():
            backend_config = config.get_backend_config(backend_name)
            if backend_config:
                profile["backends"][backend_name] = {
                    "type": backend_config.backend_type.value,
                    "config": {
                        "model": backend_config.model,
                        "enabled": backend_config.enabled,
                        # Don't save API keys in profiles
                        "api_key_env": backend_config.api_key_env
                    }
                }
        
        # Save bot configs
        for bot_name in config.list_bots():
            bot_config = config.get_bot_config(bot_name)
            if bot_config:
                profile["bots"][bot_name] = {
                    "backend": bot_config.backend,
                    "system_prompt": bot_config.system_prompt,
                    "personality": bot_config.personality,
                    "memory_enabled": bot_config.memory_enabled,
                    "learning_enabled": bot_config.learning_enabled
                }
        
        # Save profile
        wrapper.config_profiles[name] = profile
        wrapper.save_profiles()
        
        console.print(f"✅ Profile '{name}' saved!", style="green")
        console.print(f"📊 Saved {len(profile['backends'])} backends and {len(profile['bots'])} bots")
        
    except Exception as e:
        console.print(f"❌ Failed to save profile: {e}", style="red")

@profiles.command("apply")
@click.argument("name")
@click.option("--merge", is_flag=True, help="Merge with existing config")
def apply_profile(name, merge):
    """Apply a saved configuration profile"""
    
    if name not in wrapper.config_profiles:
        console.print(f"❌ Profile '{name}' not found", style="red")
        console.print("💡 List profiles with 'acm-wrapper profiles list'")
        return
    
    if not merge and Path("config.yaml").exists():
        if not Confirm.ask("This will overwrite current configuration. Continue?"):
            console.print("❌ Operation cancelled", style="yellow")
            return
    
    _apply_profile(name)

@profiles.command("delete")
@click.argument("name")
def delete_profile(name):
    """Delete a saved profile"""
    
    if name not in wrapper.config_profiles:
        console.print(f"❌ Profile '{name}' not found", style="red")
        return
    
    if Confirm.ask(f"Delete profile '{name}'?"):
        del wrapper.config_profiles[name]
        wrapper.save_profiles()
        console.print(f"✅ Profile '{name}' deleted", style="green")

# Automation commands
@cli.group()
def auto():
    """Automation and batch operations"""
    pass

def _show_bot_status(manager: ChatManager, bot_name: str, detailed: bool):
    """Show detailed status for a specific bot"""
    
    try:
        bot = manager.get_bot(bot_name)
        stats = bot.get_stats()
        
        console.print(f"🤖 Status for Bot: {bot_name}", style="bold blue")
        console.print()
        
        # Basic info
        console.print(f"🔌 Backend: {stats['backend']}")
        console.print(f"💬 Messages: {stats['message_count']}")
        console.print(f"🧠 Memory: {'✅ Enabled' if stats['memory_enabled'] else '❌ Disabled'}")
        console.print(f"📚 Learning: {'✅ Enabled' if stats['learning_enabled'] else '❌ Disabled'}")
        console.print(f"👤 Personalization: {'✅ Enabled' if stats.get('personalization_enabled', False) else '❌ Disabled'}")
        
        if detailed:
            console.print(f"\n📊 Detailed Statistics:")
            console.print(f"⚡ Avg Response Time: {stats.get('average_response_time', 0):.2f}s")
            console.print(f"🎯 Total Tokens: {stats.get('total_tokens_used', 'N/A')}")
            console.print(f"💰 Total Cost: ${stats.get('total_cost', 0):.4f}")
            console.print(f"😊 User Satisfaction: {stats.get('user_satisfaction', 0)*100:.1f}%")
            console.print(f"❌ Error Count: {stats.get('error_count', 0)}")
            
            # Conversation info
            if stats['message_count'] > 0:
                console.print(f"\n💭 Conversation Info:")
                console.print(f"📅 Created: {stats.get('created_at', 'Unknown')}")
                console.print(f"🕐 Last Activity: {stats.get('last_activity', 'Unknown')}")
                
                # Learning data
                learning_interactions = stats.get('learning_interactions', 0)
                if learning_interactions > 0:
                    console.print(f"📈 Learning Interactions: {learning_interactions}")
                
                # Common topics
                common_topics = stats.get('common_topics', [])
                if common_topics:
                    console.print(f"🏷️ Common Topics: {', '.join(common_topics[:5])}")
        
    except Exception as e:
        console.print(f"❌ Error getting bot status: {e}", style="red")

@auto.command("batch-chat")
@click.argument("input_file")
@click.option("--bot", "-b", default="assistant", help="Bot to use for batch processing")
@click.option("--output", "-o", help="Output file")
@click.option("--format", type=click.Choice(["json", "csv", "txt"]), default="json")
def batch_chat(input_file, bot, output, format):
    """Process multiple messages in batch"""
    
    try:
        # Read input file
        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"❌ Input file {input_file} not found", style="red")
            return
        
        if input_path.suffix == ".json":
            with open(input_path, 'r') as f:
                messages = json.load(f)
        elif input_path.suffix == ".txt":
            with open(input_path, 'r') as f:
                messages = [line.strip() for line in f if line.strip()]
        else:
            console.print(f"❌ Unsupported input format: {input_path.suffix}", style="red")
            return
        
        # Process messages
        manager = ChatManager("config.yaml")
        results = []
        
        with Progress() as progress:
            task = progress.add_task("Processing messages...", total=len(messages))
            
            for i, message in enumerate(messages):
                try:
                    response = asyncio.run(manager.chat_with_bot(bot_name, message))
                    results.append({
                        "index": i,
                        "input": message,
                        "output": response,
                        "timestamp": datetime.now().isoformat(),
                        "bot": bot_name
                    })
                except Exception as e:
                    results.append({
                        "index": i,
                        "input": message,
                        "output": f"ERROR: {e}",
                        "timestamp": datetime.now().isoformat(),
                        "bot": bot_name
                    })
                
                progress.advance(task)
        
        # Save results
        output_file = output or f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == "json":
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        elif format == "csv":
            import csv
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["index", "input", "output", "timestamp", "bot"])
                writer.writeheader()
                writer.writerows(results)
        elif format == "txt":
            with open(output_file, 'w') as f:
                for result in results:
                    f.write(f"Input: {result['input']}\n")
                    f.write(f"Output: {result['output']}\n")
                    f.write(f"---\n\n")
        
        console.print(f"✅ Processed {len(messages)} messages", style="green")
        console.print(f"📁 Results saved to {output_file}")
        
    except Exception as e:
        console.print(f"❌ Batch processing failed: {e}", style="red")

@auto.command("backup")
@click.option("--destination", "-d", help="Backup destination directory")
@click.option("--compress", is_flag=True, help="Compress backup")
def backup_system(destination, compress):
    """Create system backup"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"ai_chat_manager_backup_{timestamp}"
    
    if destination:
        backup_dir = Path(destination) / backup_name
    else:
        backup_dir = Path("backups") / backup_name
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    with Progress() as progress:
        task = progress.add_task("Creating backup...", total=4)
        
        try:
            # Backup configuration
            progress.update(task, description="Backing up configuration...")
            if Path("config.yaml").exists():
                shutil.copy2("config.yaml", backup_dir / "config.yaml")
            progress.advance(task)
            
            # Backup data directory
            progress.update(task, description="Backing up data...")
            data_dir = Path("data")
            if data_dir.exists():
                shutil.copytree(data_dir, backup_dir / "data", dirs_exist_ok=True)
            progress.advance(task)
            
            # Backup profiles
            progress.update(task, description="Backing up profiles...")
            profiles_file = Path.home() / ".ai_chat_manager" / "profiles.json"
            if profiles_file.exists():
                shutil.copy2(profiles_file, backup_dir / "profiles.json")
            progress.advance(task)
            
            # Create backup info
            progress.update(task, description="Creating backup info...")
            backup_info = {
                "created": datetime.now().isoformat(),
                "version": "0.2.0",
                "contents": {
                    "config": Path("config.yaml").exists(),
                    "data": Path("data").exists(),
                    "profiles": profiles_file.exists()
                }
            }
            
            with open(backup_dir / "backup_info.json", 'w') as f:
                json.dump(backup_info, f, indent=2)
            progress.advance(task)
            
            # Compress if requested
            if compress:
                progress.update(task, description="Compressing backup...")
                shutil.make_archive(str(backup_dir), 'zip', backup_dir.parent, backup_dir.name)
                shutil.rmtree(backup_dir)
                backup_file = f"{backup_dir}.zip"
                console.print(f"✅ Compressed backup created: {backup_file}", style="green")
            else:
                console.print(f"✅ Backup created: {backup_dir}", style="green")
                
        except Exception as e:
            console.print(f"❌ Backup failed: {e}", style="red")

# Development and testing commands
@cli.group()
def dev():
    """Development and testing utilities"""
    pass

@dev.command("test-backends")
def test_backends():
    """Test all configured backends"""
    
    try:
        manager = ChatManager("config.yaml")
        backends = manager.list_backends()
        
        if not backends:
            console.print("❌ No backends configured", style="red")
            return
        
        console.print(f"🧪 Testing {len(backends)} backends...\n")
        
        results = []
        
        with Progress() as progress:
            task = progress.add_task("Testing backends...", total=len(backends))
            
            for backend_name in backends:
                progress.update(task, description=f"Testing {backend_name}...")
                
                try:
                    # Simple test message
                    test_message = "Hello, this is a test message. Please respond briefly."
                    start_time = datetime.now()
                    
                    response = asyncio.run(manager.chat_with_bot(
                        "test_bot", test_message, preferred_backend=backend_name
                    ))
                    
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    results.append({
                        "backend": backend_name,
                        "status": "✅ Success",
                        "response_time": f"{response_time:.2f}s",
                        "response_length": len(response),
                        "error": None
                    })
                    
                except Exception as e:
                    results.append({
                        "backend": backend_name,
                        "status": "❌ Failed",
                        "response_time": "N/A",
                        "response_length": 0,
                        "error": str(e)
                    })
                
                progress.advance(task)
        
        # Display results
        table = Table(title="🧪 Backend Test Results")
        table.add_column("Backend", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Response Time", style="green")
        table.add_column("Response Length", style="blue")
        table.add_column("Error", style="red")
        
        for result in results:
            table.add_row(
                result["backend"],
                result["status"],
                result["response_time"],
                str(result["response_length"]),
                result["error"] or ""
            )
        
        console.print(table)
        
        # Summary
        successful = sum(1 for r in results if "Success" in r["status"])
        console.print(f"\n📊 Summary: {successful}/{len(results)} backends working")
        
    except Exception as e:
        console.print(f"❌ Backend testing failed: {e}", style="red")

@dev.command("benchmark")
@click.option("--backend", help="Backend to benchmark")
@click.option("--messages", "-n", default=10, help="Number of test messages")
@click.option("--concurrent", "-c", default=1, help="Concurrent requests")
def benchmark_backend(backend, messages, concurrent):
    """Benchmark backend performance"""
    asyncio.run(_benchmark_backend_async(backend, messages, concurrent))

async def _benchmark_backend_async(backend, messages, concurrent):
    """Benchmark backend performance"""
    
    console.print(f"🏃 Benchmarking backend performance", style="bold blue")
    console.print(f"Messages: {messages}, Concurrent: {concurrent}\n")
    
    # Test messages of varying lengths
    test_messages = [
        "Hi",
        "How are you today?",
        "Can you explain artificial intelligence in simple terms?",
        "Write a short story about a robot learning to paint.",
        "What are the key differences between machine learning and deep learning, and how do they relate to artificial intelligence as a whole field?"
    ]
    
    try:
        manager = ChatManager("config.yaml")
        
        # Select backend
        if not backend:
            available_backends = manager.list_backends()
            if not available_backends:
                console.print("❌ No backends available", style="red")
                return
            backend = available_backends[0]
            console.print(f"Using backend: {backend}")
        
        # Run benchmark
        results = []
        start_time = datetime.now()
        
        async def send_message(message_idx):
            message = test_messages[message_idx % len(test_messages)]
            msg_start = datetime.now()
            
            try:
                response = await manager.chat_with_bot("benchmark_bot", message, preferred_backend=backend)
                msg_end = datetime.now()
                
                return {
                    "success": True,
                    "response_time": (msg_end - msg_start).total_seconds(),
                    "message_length": len(message),
                    "response_length": len(response),
                    "error": None
                }
            except Exception as e:
                msg_end = datetime.now()
                return {
                    "success": False,
                    "response_time": (msg_end - msg_start).total_seconds(),
                    "message_length": len(message),
                    "response_length": 0,
                    "error": str(e)
                }
        
        # Run concurrent requests
        with Progress() as progress:
            task = progress.add_task("Running benchmark...", total=messages)
            
            for batch_start in range(0, messages, concurrent):
                batch_end = min(batch_start + concurrent, messages)
                batch_tasks = []
                
                for i in range(batch_start, batch_end):
                    batch_tasks.append(send_message(i))
                
                batch_results = await asyncio.gather(*batch_tasks)
                results.extend(batch_results)
                
                progress.update(task, advance=len(batch_tasks))
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Analyze results
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        if successful:
            avg_response_time = sum(r["response_time"] for r in successful) / len(successful)
            min_response_time = min(r["response_time"] for r in successful)
            max_response_time = max(r["response_time"] for r in successful)
            avg_response_length = sum(r["response_length"] for r in successful) / len(successful)
        else:
            avg_response_time = min_response_time = max_response_time = avg_response_length = 0
        
        # Display results
        console.print(f"\n📊 Benchmark Results for {backend}", style="bold")
        console.print(f"Total time: {total_time:.2f}s")
        console.print(f"Messages sent: {len(results)}")
        console.print(f"Successful: {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
        console.print(f"Failed: {len(failed)}")
        console.print(f"Requests/second: {len(results)/total_time:.2f}")
        
        if successful:
            console.print(f"\nResponse Times:")
            console.print(f"  Average: {avg_response_time:.2f}s")
            console.print(f"  Min: {min_response_time:.2f}s")
            console.print(f"  Max: {max_response_time:.2f}s")
            console.print(f"  Avg response length: {avg_response_length:.0f} chars")
        
        if failed:
            console.print(f"\n❌ Errors:")
            error_counts = {}
            for r in failed:
                error = r["error"][:50] + "..." if len(r["error"]) > 50 else r["error"]
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in error_counts.items():
                console.print(f"  {error}: {count} times")
        
    except Exception as e:
        console.print(f"❌ Benchmark failed: {e}", style="red")

# Main CLI integration
@cli.command("main")
@click.pass_context
def run_main_cli(ctx):
    """Run the main AI Chat Manager CLI"""
    # Forward to main CLI
    main_cli.main(standalone_mode=False)

# Entry point
def main():
    """Main entry point for the CLI wrapper"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
    except Exception as e:
        console.print(f"💥 Unexpected error: {e}", style="red")

if __name__ == "__main__":
    main()