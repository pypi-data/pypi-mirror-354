#!/usr/bin/env python3
"""
Enhanced CLI Wrapper for AI Chat Manager

Advanced features including sophisticated bot creation, personality system,
multi-bot conversations, performance analytics, and marketplace functionality.
"""

import asyncio
import click
import json
import os
import sys
import yaml
import subprocess
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil
import uuid
import hashlib
import importlib.util
from dataclasses import dataclass, field

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
from rich.text import Text
from rich.status import Status

# Import main CLI and core components
from .main import cli as main_cli
from ..core.manager import ChatManager
from ..core.config import Config, BackendConfig, BotConfig
from ..backends import list_available_backends, get_backend_info

console = Console()

@dataclass
class BotPersonality:
    """Enhanced bot personality definition"""
    name: str
    description: str
    traits: Dict[str, float]  # personality traits (0.0 to 1.0)
    speaking_style: str
    expertise_areas: List[str]
    temperature: float = 0.7
    system_prompt_template: str = ""
    example_responses: List[str] = field(default_factory=list)
    
    def generate_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Generate system prompt based on personality and context"""
        if not self.system_prompt_template:
            return f"You are {self.name}. {self.description} {self.speaking_style}"
        
        template_vars = {
            "name": self.name,
            "description": self.description,
            "speaking_style": self.speaking_style,
            "expertise": ", ".join(self.expertise_areas),
            **(context or {})
        }
        
        return self.system_prompt_template.format(**template_vars)

@dataclass 
class BotTemplate:
    """Enhanced bot template with skills and capabilities"""
    name: str
    category: str
    description: str
    personality: BotPersonality
    skills: List[str]
    required_backends: List[str]
    optional_backends: List[str]
    use_cases: List[str]
    configuration: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    estimated_setup_time: str = "2 minutes"
    
    def is_compatible_with_backend(self, backend: str) -> bool:
        """Check if template is compatible with backend"""
        return backend in self.required_backends or backend in self.optional_backends

@dataclass
class ConversationAnalytics:
    """Analytics for conversations and bot performance"""
    bot_name: str
    total_conversations: int = 0
    total_messages: int = 0
    average_response_time: float = 0.0
    user_satisfaction_scores: List[float] = field(default_factory=list)
    common_topics: Dict[str, int] = field(default_factory=dict)
    error_count: int = 0
    most_active_hours: Dict[int, int] = field(default_factory=dict)
    user_engagement_score: float = 0.0
    
    @property
    def average_satisfaction(self) -> float:
        if not self.user_satisfaction_scores:
            return 0.0
        return sum(self.user_satisfaction_scores) / len(self.user_satisfaction_scores)

class EnhancedCLIWrapper:
    """Enhanced CLI wrapper with advanced features"""
    
    def __init__(self):
        self.config_profiles = {}
        self.bot_templates = {}
        self.bot_marketplace = {}
        self.conversation_analytics = {}
        self.automation_scripts = {}
        self.plugin_registry = {}
        
        # Load data
        self.load_all_data()
        
        # Initialize built-in personalities and templates
        self._initialize_personalities()
        self._initialize_templates()
    
    def load_all_data(self):
        """Load all persistent data"""
        data_dir = Path.home() / ".ai_chat_manager"
        data_dir.mkdir(exist_ok=True)
        
        # Load profiles
        profiles_file = data_dir / "profiles.json"
        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    self.config_profiles = json.load(f)
            except Exception as e:
                console.print(f"⚠️ Failed to load profiles: {e}", style="yellow")
        
        # Load analytics
        analytics_file = data_dir / "analytics.json"
        if analytics_file.exists():
            try:
                with open(analytics_file, 'r') as f:
                    analytics_data = json.load(f)
                    self.conversation_analytics = {
                        k: ConversationAnalytics(**v) for k, v in analytics_data.items()
                    }
            except Exception as e:
                console.print(f"⚠️ Failed to load analytics: {e}", style="yellow")
        
        # Load marketplace
        marketplace_file = data_dir / "marketplace.json"
        if marketplace_file.exists():
            try:
                with open(marketplace_file, 'r') as f:
                    self.bot_marketplace = json.load(f)
            except Exception as e:
                console.print(f"⚠️ Failed to load marketplace: {e}", style="yellow")
    
    def save_all_data(self):
        """Save all persistent data"""
        data_dir = Path.home() / ".ai_chat_manager"
        data_dir.mkdir(exist_ok=True)
        
        try:
            # Save profiles
            with open(data_dir / "profiles.json", 'w') as f:
                json.dump(self.config_profiles, f, indent=2, default=str)
            
            # Save analytics
            analytics_data = {
                k: v.__dict__ for k, v in self.conversation_analytics.items()
            }
            with open(data_dir / "analytics.json", 'w') as f:
                json.dump(analytics_data, f, indent=2, default=str)
            
            # Save marketplace
            with open(data_dir / "marketplace.json", 'w') as f:
                json.dump(self.bot_marketplace, f, indent=2, default=str)
                
        except Exception as e:
            console.print(f"⚠️ Failed to save data: {e}", style="yellow")
    
    def _initialize_personalities(self):
        """Initialize built-in bot personalities"""
        self.personalities = {
            "helpful_assistant": BotPersonality(
                name="Helpful Assistant",
                description="A friendly and knowledgeable assistant ready to help with any task.",
                traits={"helpfulness": 0.9, "friendliness": 0.8, "patience": 0.8, "creativity": 0.6},
                speaking_style="Speak in a warm, professional tone with clear explanations.",
                expertise_areas=["general knowledge", "problem solving", "task assistance"],
                temperature=0.7,
                system_prompt_template="You are {name}, {description} {speaking_style} Your expertise includes {expertise}. Always be patient and thorough in your responses."
            ),
            
            "creative_writer": BotPersonality(
                name="Creative Muse",
                description="An imaginative and inspiring creative writing companion.",
                traits={"creativity": 0.95, "expressiveness": 0.9, "inspiration": 0.85, "playfulness": 0.8},
                speaking_style="Use vivid language, metaphors, and engaging storytelling techniques.",
                expertise_areas=["creative writing", "storytelling", "poetry", "character development"],
                temperature=0.9,
                system_prompt_template="You are {name}, {description} {speaking_style} Inspire creativity and help bring ideas to life through words."
            ),
            
            "analytical_advisor": BotPersonality(
                name="Logic Master",
                description="A methodical and precise analytical thinking partner.",
                traits={"analytical": 0.95, "precision": 0.9, "objectivity": 0.85, "patience": 0.8},
                speaking_style="Use clear, logical reasoning with step-by-step explanations.",
                expertise_areas=["data analysis", "logical reasoning", "research", "critical thinking"],
                temperature=0.3,
                system_prompt_template="You are {name}, {description} {speaking_style} Always provide evidence-based insights and methodical approaches."
            ),
            
            "empathetic_counselor": BotPersonality(
                name="Compassionate Guide",
                description="A caring and understanding emotional support companion.",
                traits={"empathy": 0.95, "compassion": 0.9, "patience": 0.95, "wisdom": 0.8},
                speaking_style="Speak with warmth, understanding, and gentle guidance.",
                expertise_areas=["emotional support", "active listening", "motivation", "wellness"],
                temperature=0.7,
                system_prompt_template="You are {name}, {description} {speaking_style} Always validate feelings and provide supportive, non-judgmental guidance."
            ),
            
            "technical_expert": BotPersonality(
                name="Tech Guru",
                description="A knowledgeable and precise technical expert.",
                traits={"expertise": 0.95, "precision": 0.9, "innovation": 0.8, "thoroughness": 0.85},
                speaking_style="Provide detailed technical explanations with practical examples.",
                expertise_areas=["programming", "technology", "software development", "troubleshooting"],
                temperature=0.4,
                system_prompt_template="You are {name}, {description} {speaking_style} Always provide accurate technical information with code examples when relevant."
            ),
            
            "witty_companion": BotPersonality(
                name="Clever Friend",
                description="A humorous and entertaining conversational partner.",
                traits={"humor": 0.9, "wit": 0.85, "playfulness": 0.9, "spontaneity": 0.8},
                speaking_style="Use humor, wordplay, and entertaining observations while remaining helpful.",
                expertise_areas=["entertainment", "conversation", "jokes", "trivia"],
                temperature=0.8,
                system_prompt_template="You are {name}, {description} {speaking_style} Keep conversations light and engaging while being genuinely helpful."
            )
        }
    
    def _initialize_templates(self):
        """Initialize built-in bot templates"""
        self.bot_templates = {
            "personal_assistant": BotTemplate(
                name="Personal Assistant",
                category="productivity",
                description="A comprehensive personal productivity assistant",
                personality=self.personalities["helpful_assistant"],
                skills=["scheduling", "reminders", "email_drafting", "research", "planning"],
                required_backends=["openai"],
                optional_backends=["venice", "anthropic"],
                use_cases=["daily planning", "task management", "information lookup"],
                configuration={
                    "memory_enabled": True,
                    "learning_enabled": True,
                    "personalization_enabled": True,
                    "function_calling_enabled": True
                },
                tags=["productivity", "assistant", "personal"],
                difficulty="beginner"
            ),
            
            "creative_studio": BotTemplate(
                name="Creative Studio",
                category="creativity",
                description="A multi-talented creative companion for all artistic endeavors",
                personality=self.personalities["creative_writer"],
                skills=["writing", "brainstorming", "storytelling", "poetry", "world_building"],
                required_backends=["openai", "anthropic"],
                optional_backends=["venice"],
                use_cases=["creative writing", "content creation", "artistic inspiration"],
                configuration={
                    "memory_enabled": True,
                    "learning_enabled": True,
                    "temperature": 0.9,
                    "creativity_boost": True
                },
                tags=["creativity", "writing", "inspiration"],
                difficulty="intermediate"
            ),
            
            "data_scientist": BotTemplate(
                name="Data Science Companion",
                category="analysis",
                description="An expert data analysis and research partner",
                personality=self.personalities["analytical_advisor"],
                skills=["data_analysis", "statistics", "visualization", "research", "reporting"],
                required_backends=["openai"],
                optional_backends=["anthropic"],
                use_cases=["data analysis", "research projects", "statistical consulting"],
                configuration={
                    "memory_enabled": True,
                    "precision_mode": True,
                    "function_calling_enabled": True,
                    "code_generation": True
                },
                tags=["analysis", "data", "research"],
                difficulty="advanced"
            ),
            
            "wellness_coach": BotTemplate(
                name="Wellness & Mindfulness Coach",
                category="health",
                description="A supportive wellness and mental health companion",
                personality=self.personalities["empathetic_counselor"],
                skills=["emotional_support", "mindfulness", "goal_setting", "motivation"],
                required_backends=["openai", "anthropic"],
                optional_backends=["venice"],
                use_cases=["mental health support", "wellness tracking", "motivation"],
                configuration={
                    "memory_enabled": True,
                    "personalization_enabled": True,
                    "empathy_mode": True,
                    "safety_guidelines": "wellness"
                },
                tags=["wellness", "support", "mindfulness"],
                difficulty="intermediate"
            ),
            
            "coding_mentor": BotTemplate(
                name="Programming Mentor",
                category="development",
                description="An expert programming teacher and code reviewer",
                personality=self.personalities["technical_expert"],
                skills=["code_review", "debugging", "teaching", "best_practices", "architecture"],
                required_backends=["openai"],
                optional_backends=["anthropic"],
                use_cases=["code review", "learning programming", "debugging help"],
                configuration={
                    "memory_enabled": True,
                    "code_analysis": True,
                    "function_calling_enabled": True,
                    "teaching_mode": True
                },
                tags=["coding", "education", "development"],
                difficulty="advanced"
            )
        }

# Global wrapper instance
enhanced_wrapper = EnhancedCLIWrapper()

# Enhanced Click group
class EnhancedWrapperGroup(click.Group):
    """Enhanced Click group for wrapper commands"""
    
    def format_help(self, ctx, formatter):
        formatter.write_heading("🚀 AI Chat Manager - Enhanced CLI Wrapper")
        formatter.write_paragraph()
        formatter.write("Advanced bot creation, management, and conversation tools.")
        formatter.write_paragraph()
        
        super().format_help(ctx, formatter)

@click.group(cls=EnhancedWrapperGroup)
@click.version_option(version="0.3.0", prog_name="AI Chat Manager Enhanced Wrapper")
def cli():
    """AI Chat Manager Enhanced CLI Wrapper"""
    pass

# ============================================================================
# ENHANCED BOT CREATION AND MANAGEMENT
# ============================================================================

@cli.group()
def bot():
    """Enhanced bot creation and management"""
    pass

@bot.command("create-advanced")
@click.option("--interactive", "-i", is_flag=True, help="Interactive bot creation wizard")
@click.option("--template", help="Use a bot template")
@click.option("--personality", help="Bot personality type")
@click.option("--skills", help="Comma-separated list of skills")
@click.option("--backend", help="Preferred backend")
def create_advanced_bot(interactive, template, personality, skills, backend):
    """Create an advanced bot with enhanced capabilities"""
    
    if interactive:
        _run_bot_creation_wizard()
    elif template:
        _create_from_enhanced_template(template, backend)
    else:
        _create_custom_bot(personality, skills, backend)

def _run_bot_creation_wizard():
    """Interactive bot creation wizard"""
    console.print("🧙‍♂️ Welcome to the Enhanced Bot Creation Wizard!", style="bold blue")
    console.print()
    
    # Step 1: Bot purpose and identity
    console.print("📝 Step 1: Define Your Bot's Identity", style="bold cyan")
    console.print()
    
    bot_name = Prompt.ask("🤖 Bot name")
    bot_purpose = Prompt.ask("🎯 What's the main purpose of this bot?")
    bot_domain = Prompt.ask("🏢 Domain/field of expertise", default="general")
    
    # Step 2: Personality selection
    console.print("\n🎭 Step 2: Choose a Personality", style="bold cyan")
    _display_personality_options()
    
    personality_choice = Prompt.ask(
        "Select personality", 
        choices=list(enhanced_wrapper.personalities.keys()) + ["custom"],
        default="helpful_assistant"
    )
    
    if personality_choice == "custom":
        personality = _create_custom_personality()
    else:
        personality = enhanced_wrapper.personalities[personality_choice]
    
    # Step 3: Skills and capabilities
    console.print("\n🛠️ Step 3: Configure Skills and Capabilities", style="bold cyan")
    skills = _select_bot_skills()
    
    # Step 4: Backend and model selection
    console.print("\n🔌 Step 4: Choose Backend and Model", style="bold cyan")
    backend, model = _select_backend_and_model()
    
    # Step 5: Advanced configuration
    console.print("\n⚙️ Step 5: Advanced Configuration", style="bold cyan")
    advanced_config = _configure_advanced_settings()
    
    # Step 6: Review and create
    console.print("\n📋 Step 6: Review Your Bot Configuration", style="bold cyan")
    if _review_bot_configuration(bot_name, bot_purpose, personality, skills, backend, advanced_config):
        _create_bot_from_wizard_config(bot_name, bot_purpose, personality, skills, backend, advanced_config)

def _display_personality_options():
    """Display available personality options"""
    table = Table(title="🎭 Available Personalities")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Best For", style="green")
    
    for key, personality in enhanced_wrapper.personalities.items():
        best_for = ", ".join(personality.expertise_areas[:2])
        table.add_row(
            personality.name,
            personality.description[:60] + "...",
            best_for
        )
    
    console.print(table)
    console.print()

def _create_custom_personality() -> BotPersonality:
    """Create a custom personality"""
    console.print("🎨 Creating Custom Personality", style="bold yellow")
    
    name = Prompt.ask("Personality name")
    description = Prompt.ask("Description")
    speaking_style = Prompt.ask("Speaking style/tone")
    
    # Trait configuration
    console.print("\n🧠 Configure personality traits (0.0 to 1.0):")
    traits = {}
    trait_options = ["creativity", "analytical", "empathy", "humor", "patience", "precision"]
    
    for trait in trait_options:
        if Confirm.ask(f"Include {trait} trait?", default=True):
            value = FloatPrompt.ask(f"{trait.title()} level (0.0-1.0)", default=0.7)
            traits[trait] = max(0.0, min(1.0, value))
    
    expertise_areas = Prompt.ask("Expertise areas (comma-separated)").split(",")
    expertise_areas = [area.strip() for area in expertise_areas if area.strip()]
    
    return BotPersonality(
        name=name,
        description=description,
        traits=traits,
        speaking_style=speaking_style,
        expertise_areas=expertise_areas
    )

def _select_bot_skills() -> List[str]:
    """Select bot skills and capabilities"""
    available_skills = [
        "research", "writing", "analysis", "coding", "math", "planning", 
        "creativity", "problem_solving", "education", "entertainment",
        "emotional_support", "technical_support", "data_visualization",
        "language_translation", "summarization", "brainstorming"
    ]
    
    console.print("Available skills:")
    columns = Columns([f"• {skill}" for skill in available_skills], equal=True)
    console.print(columns)
    console.print()
    
    selected_skills = []
    
    if Confirm.ask("Select skills interactively?", default=True):
        for skill in available_skills:
            if Confirm.ask(f"Include {skill}?", default=False):
                selected_skills.append(skill)
    else:
        skills_input = Prompt.ask("Enter skills (comma-separated)")
        selected_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    
    return selected_skills

def _select_backend_and_model():
    """Select backend and model"""
    try:
        manager = ChatManager("config.yaml", auto_start=False)
        available_backends = manager.list_backends()
        
        if not available_backends:
            console.print("⚠️ No backends configured. Setting up default backend...", style="yellow")
            backend = "openai"
            model = "gpt-3.5-turbo"
        else:
            console.print("Available backends:")
            for i, backend_name in enumerate(available_backends, 1):
                console.print(f"{i}. {backend_name}")
            
            choice = IntPrompt.ask("Select backend", default=1)
            backend = available_backends[choice - 1]
            
            # Model selection based on backend
            model_suggestions = {
                "openai": ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                "anthropic": ["claude-3-sonnet", "claude-3-haiku"],
                "venice": ["gpt-3.5-turbo", "gpt-4"],
                "huggingface": ["microsoft/DialoGPT-large", "google/flan-t5-large"]
            }
            
            suggestions = model_suggestions.get(backend, ["default"])
            console.print(f"\nRecommended models for {backend}:")
            for model in suggestions:
                console.print(f"• {model}")
            
            model = Prompt.ask("Model name", default=suggestions[0])
        
        return backend, model
        
    except Exception as e:
        console.print(f"⚠️ Error selecting backend: {e}", style="yellow")
        return "openai", "gpt-3.5-turbo"

def _configure_advanced_settings() -> Dict[str, Any]:
    """Configure advanced bot settings"""
    config = {}
    
    console.print("🔧 Advanced Settings Configuration")
    
    # Memory settings
    config["memory_enabled"] = Confirm.ask("Enable conversation memory?", default=True)
    if config["memory_enabled"]:
        config["max_context_length"] = IntPrompt.ask("Max context length", default=4000)
        config["memory_decay"] = Confirm.ask("Enable memory decay over time?", default=False)
    
    # Learning settings
    config["learning_enabled"] = Confirm.ask("Enable learning from interactions?", default=False)
    if config["learning_enabled"]:
        config["feedback_learning"] = Confirm.ask("Learn from user feedback?", default=True)
    
    # Personalization
    config["personalization_enabled"] = Confirm.ask("Enable user personalization?", default=True)
    
    # Safety and moderation
    config["content_filter_enabled"] = Confirm.ask("Enable content filtering?", default=True)
    if config["content_filter_enabled"]:
        safety_levels = ["low", "medium", "high"]
        safety_choice = Prompt.ask("Safety level", choices=safety_levels, default="medium")
        config["safety_level"] = safety_choice
    
    # Function calling
    config["function_calling_enabled"] = Confirm.ask("Enable function calling?", default=False)
    
    # Response settings
    response_styles = ["concise", "balanced", "detailed"]
    config["response_style"] = Prompt.ask("Response style", choices=response_styles, default="balanced")
    
    config["temperature"] = FloatPrompt.ask("Temperature (creativity level 0.0-2.0)", default=0.7)
    
    return config

def _review_bot_configuration(bot_name, bot_purpose, personality, skills, backend, config) -> bool:
    """Review bot configuration before creation"""
    
    review_text = f"""
**🤖 Bot Configuration Review**

**Basic Information:**
• Name: {bot_name}
• Purpose: {bot_purpose}
• Backend: {backend}

**Personality:**
• Type: {personality.name}
• Description: {personality.description}
• Speaking Style: {personality.speaking_style}

**Skills:** {', '.join(skills)}

**Configuration:**
• Memory: {'✅' if config.get('memory_enabled') else '❌'}
• Learning: {'✅' if config.get('learning_enabled') else '❌'}
• Personalization: {'✅' if config.get('personalization_enabled') else '❌'}
• Function Calling: {'✅' if config.get('function_calling_enabled') else '❌'}
• Safety Level: {config.get('safety_level', 'medium')}
• Response Style: {config.get('response_style', 'balanced')}
• Temperature: {config.get('temperature', 0.7)}
    """
    
    console.print(Panel(Markdown(review_text), title="📋 Configuration Review", border_style="blue"))
    
    return Confirm.ask("Create this bot?", default=True)

def _create_bot_from_wizard_config(bot_name, bot_purpose, personality, skills, backend, config):
    """Create bot from wizard configuration"""
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Creating your enhanced bot...", total=None)
        
        try:
            manager = ChatManager("config.yaml")
            
            # Build system prompt
            system_prompt = personality.generate_system_prompt({
                "purpose": bot_purpose,
                "skills": ", ".join(skills)
            })
            
            # Create bot with enhanced configuration
            bot = manager.create_bot(
                name=bot_name,
                backend=backend,
                system_prompt=system_prompt,
                personality=personality.name.lower().replace(" ", "_"),
                **config
            )
            
            # Store additional metadata
            enhanced_wrapper.conversation_analytics[bot_name] = ConversationAnalytics(bot_name=bot_name)
            enhanced_wrapper.save_all_data()
            
            console.print(f"✅ Enhanced bot '{bot_name}' created successfully!", style="green")
            
            # Show next steps
            _show_bot_next_steps(bot_name)
            
        except Exception as e:
            console.print(f"❌ Failed to create bot: {e}", style="red")

def _show_bot_next_steps(bot_name: str):
    """Show next steps after bot creation"""
    next_steps = f"""
🎉 **Bot Created Successfully!**

**Quick Actions:**
• `acm-wrapper chat {bot_name}` - Start chatting
• `acm-wrapper bot analyze {bot_name}` - View analytics
• `acm-wrapper bot tune {bot_name}` - Fine-tune personality
• `acm-wrapper bot export {bot_name}` - Export configuration

**Advanced Features:**
• Multi-bot conversations
• Performance monitoring
• Personality adjustment
• Skill development
    """
    
    console.print(Panel(Markdown(next_steps), title="🚀 What's Next?", border_style="green"))

@bot.command("templates")
def list_bot_templates():
    """List available bot templates with details"""
    
    console.print("🎭 Available Bot Templates", style="bold blue")
    console.print()
    
    categories = {}
    for template_id, template in enhanced_wrapper.bot_templates.items():
        if template.category not in categories:
            categories[template.category] = []
        categories[template.category].append((template_id, template))
    
    for category, templates in categories.items():
        console.print(f"📁 {category.title()}", style="bold cyan")
        
        for template_id, template in templates:
            console.print(f"  🤖 {template.name}")
            console.print(f"     {template.description}")
            console.print(f"     Skills: {', '.join(template.skills[:3])}{'...' if len(template.skills) > 3 else ''}")
            console.print(f"     Difficulty: {template.difficulty} | Setup: {template.estimated_setup_time}")
            console.print()

@bot.command("create-from-template")
@click.argument("template_name")
@click.option("--bot-name", help="Name for the new bot")
@click.option("--backend", help="Backend to use")
@click.option("--customize", "-c", is_flag=True, help="Customize template settings")
def create_from_template(template_name, bot_name, backend, customize):
    """Create bot from template with optional customization"""
    
    # Find template
    template = None
    for tid, tpl in enhanced_wrapper.bot_templates.items():
        if tid == template_name or tpl.name.lower() == template_name.lower():
            template = tpl
            break
    
    if not template:
        console.print(f"❌ Template '{template_name}' not found", style="red")
        console.print("💡 Use 'acm-wrapper bot templates' to see available templates")
        return
    
    bot_name = bot_name or Prompt.ask("Bot name", default=template.name.replace(" ", "_").lower())
    
    # Backend selection
    if not backend:
        available_backends = template.required_backends + template.optional_backends
        if len(available_backends) == 1:
            backend = available_backends[0]
        else:
            console.print(f"Available backends for {template.name}:")
            for i, be in enumerate(available_backends, 1):
                req_status = "required" if be in template.required_backends else "optional"
                console.print(f"{i}. {be} ({req_status})")
            
            choice = IntPrompt.ask("Select backend", default=1)
            backend = available_backends[choice - 1]
    
    # Customization
    config = template.configuration.copy()
    if customize:
        config.update(_customize_template_settings(template))
    
    # Create bot
    _create_bot_from_template_config(bot_name, template, backend, config)

def _customize_template_settings(template: BotTemplate) -> Dict[str, Any]:
    """Customize template settings"""
    console.print(f"🎨 Customizing {template.name}", style="bold cyan")
    
    customizations = {}
    
    # Personality adjustments
    if Confirm.ask("Adjust personality traits?", default=False):
        for trait, value in template.personality.traits.items():
            new_value = FloatPrompt.ask(f"{trait.title()} (current: {value})", default=value)
            if new_value != value:
                # Store personality adjustments
                if "personality_adjustments" not in customizations:
                    customizations["personality_adjustments"] = {}
                customizations["personality_adjustments"][trait] = new_value
    
    # Skill modifications
    if Confirm.ask("Modify skills?", default=False):
        console.print(f"Current skills: {', '.join(template.skills)}")
        additional_skills = Prompt.ask("Additional skills (comma-separated)", default="")
        if additional_skills:
            customizations["additional_skills"] = [s.strip() for s in additional_skills.split(",")]
    
    # Temperature adjustment
    current_temp = template.personality.temperature
    new_temp = FloatPrompt.ask(f"Temperature (current: {current_temp})", default=current_temp)
    if new_temp != current_temp:
        customizations["temperature"] = new_temp
    
    return customizations

def _create_bot_from_template_config(bot_name: str, template: BotTemplate, backend: str, config: Dict[str, Any]):
    """Create bot from template configuration"""
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(f"Creating {template.name} bot...", total=None)
        
        try:
            manager = ChatManager("config.yaml")
            
            # Apply customizations to personality
            personality = template.personality
            if "personality_adjustments" in config:
                personality.traits.update(config["personality_adjustments"])
            
            if "temperature" in config:
                personality.temperature = config["temperature"]
            
            # Generate enhanced system prompt
            system_prompt = personality.generate_system_prompt({
                "template": template.name,
                "skills": ", ".join(template.skills + config.get("additional_skills", [])),
                "use_cases": ", ".join(template.use_cases)
            })
            
            # Create bot
            bot_config = template.configuration.copy()
            bot_config.update({
                "system_prompt": system_prompt,
                "personality": personality.name.lower().replace(" ", "_"),
                "temperature": personality.temperature,
                "tags": template.tags,
                "template_used": template.name
            })
            
            bot = manager.create_bot(
                name=bot_name,
                backend=backend,
                **bot_config
            )
            
            # Initialize analytics
            enhanced_wrapper.conversation_analytics[bot_name] = ConversationAnalytics(bot_name=bot_name)
            enhanced_wrapper.save_all_data()
            
            console.print(f"✅ {template.name} bot '{bot_name}' created successfully!", style="green")
            
            # Show template-specific guidance
            _show_template_guidance(template, bot_name)
            
        except Exception as e:
            console.print(f"❌ Failed to create bot from template: {e}", style="red")

def _show_template_guidance(template: BotTemplate, bot_name: str):
    """Show template-specific guidance"""
    guidance = f"""
🎯 **{template.name} Bot Ready!**

**Optimized for:** {', '.join(template.use_cases)}

**Key Skills:** {', '.join(template.skills[:5])}

**Suggested First Interactions:**
    """
    
    # Add template-specific suggestions
    if "writing" in template.skills:
        guidance += "\n• Ask it to help you write something creative"
    if "analysis" in template.skills:
        guidance += "\n• Share data or a problem to analyze"
    if "coding" in template.skills:
        guidance += "\n• Ask for code review or programming help"
    if "emotional_support" in template.skills:
        guidance += "\n• Share what's on your mind for supportive guidance"
    
    guidance += f"\n\n**Start chatting:** `acm-wrapper chat {bot_name}`"
    
    console.print(Panel(Markdown(guidance), title="🎉 Template Deployed!", border_style="green"))

# ============================================================================
# ADVANCED CONVERSATION FEATURES
# ============================================================================

@cli.group()
def conversation():
    """Advanced conversation management and analytics"""
    pass

@conversation.command("multi-bot")
@click.option("--bots", help="Comma-separated list of bots")
@click.option("--topic", help="Conversation topic")
@click.option("--mode", type=click.Choice(["panel", "debate", "collaboration"]), default="panel")
def multi_bot_conversation(bots, topic, mode):
    """Start a conversation with multiple bots"""
    
    if not bots:
        # Show available bots and let user select
        try:
            manager = ChatManager("config.yaml")
            available_bots = manager.list_bots()
            
            if len(available_bots) < 2:
                console.print("❌ Need at least 2 bots for multi-bot conversation", style="red")
                console.print("💡 Create more bots with 'acm-wrapper bot create-advanced'")
                return
            
            console.print("Available bots:")
            for i, bot in enumerate(available_bots, 1):
                console.print(f"{i}. {bot}")
            
            bot_choices = Prompt.ask("Select bots (comma-separated numbers)", default="1,2")
            bot_indices = [int(x.strip()) - 1 for x in bot_choices.split(",")]
            selected_bots = [available_bots[i] for i in bot_indices if 0 <= i < len(available_bots)]
            
        except Exception as e:
            console.print(f"❌ Error loading bots: {e}", style="red")
            return
    else:
        selected_bots = [bot.strip() for bot in bots.split(",")]
    
    if len(selected_bots) < 2:
        console.print("❌ Need at least 2 bots for conversation", style="red")
        return
    
    topic = topic or Prompt.ask("Conversation topic/question")
    
    asyncio.run(_run_multi_bot_conversation(selected_bots, topic, mode))

async def _run_multi_bot_conversation(bots: List[str], topic: str, mode: str):
    """Run multi-bot conversation"""
    
    console.print(f"🎭 Starting {mode} conversation with: {', '.join(bots)}", style="bold blue")
    console.print(f"📝 Topic: {topic}")
    console.print("Type 'quit' to end, 'next' for next round\n")
    
    try:
        manager = ChatManager("config.yaml")
        conversation_history = []
        round_count = 0
        
        while True:
            round_count += 1
            console.print(f"🔄 Round {round_count}", style="bold cyan")
            console.print("-" * 50)
            
            for i, bot_name in enumerate(bots):
                try:
                    # Prepare context for this bot
                    if mode == "debate" and i > 0:
                        context = f"You are in a debate about: {topic}\n\nPrevious responses:\n"
                        context += "\n".join([f"{h['bot']}: {h['response']}" for h in conversation_history[-len(bots):]])
                        context += f"\n\nNow present your perspective (you are {bot_name}):"
                        message = context
                    elif mode == "collaboration":
                        context = f"You are collaborating on: {topic}\n\nBuilding on previous ideas:\n"
                        context += "\n".join([f"{h['bot']}: {h['response']}" for h in conversation_history[-3:]])
                        context += f"\n\nAdd your contribution:"
                        message = context
                    else:  # panel mode
                        message = f"Panel discussion topic: {topic}\n\nYour perspective as {bot_name}:"
                    
                    # Get response
                    with console.status(f"🤔 {bot_name} is thinking..."):
                        response = await manager.chat_with_bot(bot_name, message)
                    
                    # Display response
                    console.print(f"[bold green]{bot_name}[/bold green]: {response}")
                    console.print()
                    
                    # Store in conversation history
                    conversation_history.append({
                        "round": round_count,
                        "bot": bot_name,
                        "message": message,
                        "response": response,
                        "timestamp": datetime.now()
                    })
                    
                except Exception as e:
                    console.print(f"❌ Error with {bot_name}: {e}", style="red")
                    continue
            
            # User input for next action
            user_input = Prompt.ask("\nNext action", choices=["next", "quit", "save"], default="next")
            
            if user_input == "quit":
                break
            elif user_input == "save":
                _save_multi_bot_conversation(conversation_history, topic, mode)
            
            console.print()
    
    except KeyboardInterrupt:
        console.print("\n👋 Multi-bot conversation ended")
    
    # Offer to save conversation
    if conversation_history and Confirm.ask("Save conversation?", default=True):
        _save_multi_bot_conversation(conversation_history, topic, mode)

def _save_multi_bot_conversation(history: List[Dict], topic: str, mode: str):
    """Save multi-bot conversation"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"multi_bot_{mode}_{timestamp}.json"
    
    conversation_data = {
        "topic": topic,
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "participants": list(set([h["bot"] for h in history])),
        "rounds": max([h["round"] for h in history]),
        "history": history
    }
    
    with open(filename, 'w') as f:
        json.dump(conversation_data, f, indent=2, default=str)
    
    console.print(f"💾 Conversation saved to {filename}", style="green")

@conversation.command("analyze")
@click.argument("bot_name")
@click.option("--days", default=7, help="Days to analyze")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed analytics")
def analyze_conversation(bot_name, days, detailed):
    """Analyze conversation patterns and bot performance"""
    
    if bot_name not in enhanced_wrapper.conversation_analytics:
        console.print(f"❌ No analytics data for bot '{bot_name}'", style="red")
        return
    
    analytics = enhanced_wrapper.conversation_analytics[bot_name]
    
    # Display analytics dashboard
    console.print(f"📊 Conversation Analytics for {bot_name}", style="bold blue")
    console.print()
    
    # Basic metrics
    metrics_table = Table(title="📈 Key Metrics")
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green")
    
    metrics_table.add_row("Total Conversations", str(analytics.total_conversations))
    metrics_table.add_row("Total Messages", str(analytics.total_messages))
    metrics_table.add_row("Avg Response Time", f"{analytics.average_response_time:.2f}s")
    metrics_table.add_row("User Satisfaction", f"{analytics.average_satisfaction:.1%}")
    metrics_table.add_row("Engagement Score", f"{analytics.user_engagement_score:.1%}")
    metrics_table.add_row("Error Rate", f"{analytics.error_count / max(analytics.total_messages, 1):.1%}")
    
    console.print(metrics_table)
    console.print()
    
    # Top topics
    if analytics.common_topics:
        topics_table = Table(title="🏷️ Most Discussed Topics")
        topics_table.add_column("Topic", style="cyan")
        topics_table.add_column("Frequency", style="green")
        
        sorted_topics = sorted(analytics.common_topics.items(), key=lambda x: x[1], reverse=True)[:10]
        for topic, count in sorted_topics:
            topics_table.add_row(topic, str(count))
        
        console.print(topics_table)
        console.print()
    
    # Activity patterns
    if analytics.most_active_hours:
        console.print("⏰ Most Active Hours:", style="bold cyan")
        sorted_hours = sorted(analytics.most_active_hours.items(), key=lambda x: x[1], reverse=True)[:5]
        for hour, count in sorted_hours:
            console.print(f"  {hour:02d}:00 - {count} conversations")
        console.print()
    
    if detailed:
        _show_detailed_analytics(analytics)

def _show_detailed_analytics(analytics: ConversationAnalytics):
    """Show detailed analytics"""
    
    console.print("🔍 Detailed Analytics", style="bold cyan")
    
    # Satisfaction distribution
    if analytics.user_satisfaction_scores:
        satisfaction_dist = {}
        for score in analytics.user_satisfaction_scores:
            bucket = int(score * 10) / 10  # Round to nearest 0.1
            satisfaction_dist[bucket] = satisfaction_dist.get(bucket, 0) + 1
        
        console.print("\n📊 Satisfaction Score Distribution:")
        for score, count in sorted(satisfaction_dist.items()):
            bar = "█" * min(count, 20)
            console.print(f"  {score:.1f}: {bar} ({count})")
    
    # Performance trends
    console.print(f"\n📈 Performance Insights:")
    
    if analytics.average_response_time > 5.0:
        console.print("  ⚠️ Response time is high - consider optimizing", style="yellow")
    elif analytics.average_response_time < 1.0:
        console.print("  ✅ Excellent response time", style="green")
    
    if analytics.average_satisfaction > 0.8:
        console.print("  ✅ High user satisfaction", style="green")
    elif analytics.average_satisfaction < 0.6:
        console.print("  ⚠️ Low user satisfaction - review bot configuration", style="yellow")
    
    if analytics.error_count / max(analytics.total_messages, 1) > 0.05:
        console.print("  ⚠️ High error rate - check backend connectivity", style="yellow")

# ============================================================================
# BOT MARKETPLACE AND SHARING
# ============================================================================

@cli.group()
def marketplace():
    """Bot marketplace for sharing and discovering bots"""
    pass

@marketplace.command("browse")
@click.option("--category", help="Filter by category")
@click.option("--search", help="Search term")
def browse_marketplace(category, search):
    """Browse available bots in the marketplace"""
    
    console.print("🏪 Bot Marketplace", style="bold blue")
    console.print()
    
    # Filter marketplace entries
    filtered_bots = enhanced_wrapper.bot_marketplace.copy()
    
    if category:
        filtered_bots = {k: v for k, v in filtered_bots.items() 
                        if v.get("category", "").lower() == category.lower()}
    
    if search:
        search_lower = search.lower()
        filtered_bots = {k: v for k, v in filtered_bots.items() 
                        if search_lower in v.get("name", "").lower() or 
                           search_lower in v.get("description", "").lower()}
    
    if not filtered_bots:
        console.print("🔍 No bots found matching your criteria", style="yellow")
        console.print("💡 Try 'acm-wrapper marketplace featured' to see popular bots")
        return
    
    # Display marketplace bots
    for bot_id, bot_data in filtered_bots.items():
        _display_marketplace_bot(bot_id, bot_data)

def _display_marketplace_bot(bot_id: str, bot_data: Dict[str, Any]):
    """Display a marketplace bot entry"""
    
    rating_stars = "⭐" * int(bot_data.get("rating", 0))
    downloads = bot_data.get("downloads", 0)
    
    bot_info = f"""
**{bot_data.get('name', bot_id)}** {rating_stars} ({bot_data.get('rating', 0):.1f})

{bot_data.get('description', 'No description')}

**Category:** {bot_data.get('category', 'Unknown')}
**Author:** {bot_data.get('author', 'Anonymous')}
**Downloads:** {downloads:,}
**Updated:** {bot_data.get('updated', 'Unknown')}

**Install:** `acm-wrapper marketplace install {bot_id}`
    """
    
    console.print(Panel(Markdown(bot_info), border_style="cyan"))

@marketplace.command("install")
@click.argument("bot_id")
@click.option("--name", help="Custom name for the bot")
def install_marketplace_bot(bot_id, name):
    """Install a bot from the marketplace"""
    
    if bot_id not in enhanced_wrapper.bot_marketplace:
        console.print(f"❌ Bot '{bot_id}' not found in marketplace", style="red")
        return
    
    bot_data = enhanced_wrapper.bot_marketplace[bot_id]
    bot_name = name or bot_data.get("name", bot_id)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(f"Installing {bot_data.get('name', bot_id)}...", total=None)
        
        try:
            # Download and install bot configuration
            _install_bot_from_marketplace_data(bot_name, bot_data)
            
            # Update download count
            enhanced_wrapper.bot_marketplace[bot_id]["downloads"] = bot_data.get("downloads", 0) + 1
            enhanced_wrapper.save_all_data()
            
            console.print(f"✅ Bot '{bot_name}' installed successfully!", style="green")
            console.print(f"🚀 Start chatting: acm-wrapper chat {bot_name}")
            
        except Exception as e:
            console.print(f"❌ Installation failed: {e}", style="red")

def _install_bot_from_marketplace_data(bot_name: str, bot_data: Dict[str, Any]):
    """Install bot from marketplace data"""
    
    manager = ChatManager("config.yaml")
    
    # Extract configuration
    config = bot_data.get("configuration", {})
    backend = bot_data.get("backend", "openai")
    
    # Create bot
    bot = manager.create_bot(
        name=bot_name,
        backend=backend,
        **config
    )
    
    # Initialize analytics
    enhanced_wrapper.conversation_analytics[bot_name] = ConversationAnalytics(bot_name=bot_name)

@marketplace.command("publish")
@click.argument("bot_name")
@click.option("--description", help="Bot description")
@click.option("--category", help="Bot category")
def publish_bot(bot_name, description, category):
    """Publish your bot to the marketplace"""
    
    try:
        manager = ChatManager("config.yaml")
        
        if bot_name not in manager.list_bots():
            console.print(f"❌ Bot '{bot_name}' not found", style="red")
            return
        
        # Get bot configuration
        bot_config = manager.config.get_bot_config(bot_name)
        
        description = description or Prompt.ask("Bot description")
        category = category or Prompt.ask("Bot category", default="general")
        
        # Create marketplace entry
        marketplace_entry = {
            "name": bot_name,
            "description": description,
            "category": category,
            "author": os.getenv("USER", "Anonymous"),
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "configuration": bot_config.model_dump() if bot_config else {},
            "backend": bot_config.backend if bot_config else "openai",
            "downloads": 0,
            "rating": 0.0,
            "version": "1.0.0"
        }
        
        # Add to marketplace
        bot_id = f"{bot_name}_{uuid.uuid4().hex[:8]}"
        enhanced_wrapper.bot_marketplace[bot_id] = marketplace_entry
        enhanced_wrapper.save_all_data()
        
        console.print(f"✅ Bot '{bot_name}' published to marketplace!", style="green")
        console.print(f"📦 Bot ID: {bot_id}")
        
    except Exception as e:
        console.print(f"❌ Publishing failed: {e}", style="red")

# ============================================================================
# ENHANCED UTILITIES AND TOOLS
# ============================================================================

@cli.group()
def tools():
    """Advanced tools and utilities"""
    pass

@tools.command("voice-chat")
@click.argument("bot_name")
@click.option("--voice-backend", default="elevenlabs", help="Voice backend to use")
def voice_chat(bot_name, voice_backend):
    """Start voice conversation with a bot"""
    
    console.print(f"🎤 Starting voice chat with {bot_name}", style="bold blue")
    console.print("Note: This requires a voice-enabled backend (ElevenLabs)")
    
    try:
        manager = ChatManager("config.yaml")
        
        if voice_backend not in manager.list_backends():
            console.print(f"❌ Voice backend '{voice_backend}' not configured", style="red")
            console.print("💡 Set up ElevenLabs backend for voice features")
            return
        
        console.print("🎙️ Voice chat mode activated")
        console.print("Type 'quit' to end, 'mute' for text-only")
        
        asyncio.run(_run_voice_chat_session(manager, bot_name, voice_backend))
        
    except Exception as e:
        console.print(f"❌ Voice chat failed: {e}", style="red")

async def _run_voice_chat_session(manager: ChatManager, bot_name: str, voice_backend: str):
    """Run voice chat session"""
    
    console.print("Voice chat simulation - in a real implementation, this would:")
    console.print("• Use speech recognition for voice input")
    console.print("• Send text to the bot")
    console.print("• Convert bot response to speech using ElevenLabs")
    console.print("• Play audio response")
    
    # Simulated voice chat
    while True:
        user_input = Prompt.ask("👤 Say something (or type)")
        
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # Get bot response
        response = await manager.chat_with_bot(bot_name, user_input)
        
        console.print(f"🤖 {bot_name}: {response}")
        
        # In real implementation, would convert to speech
        console.print("🔊 [Audio response would play here]")

@tools.command("bot-trainer")
@click.argument("bot_name")
@click.option("--training-file", help="Training data file")
def bot_trainer(bot_name, training_file):
    """Advanced bot training and fine-tuning interface"""
    
    console.print(f"🏋️‍♂️ Bot Training Interface for {bot_name}", style="bold blue")
    
    try:
        manager = ChatManager("config.yaml")
        
        if bot_name not in manager.list_bots():
            console.print(f"❌ Bot '{bot_name}' not found", style="red")
            return
        
        console.print("Training options:")
        console.print("1. 📚 Conversation examples training")
        console.print("2. 🎯 Personality adjustment training")
        console.print("3. 📊 Performance optimization")
        
        choice = IntPrompt.ask("Select training type", default=1)
        
        if choice == 1:
            _train_with_conversations(manager, bot_name, training_file)
        elif choice == 2:
            _train_personality_adjustment(manager, bot_name)
        elif choice == 3:
            _optimize_performance(manager, bot_name)
        
    except Exception as e:
        console.print(f"❌ Training failed: {e}", style="red")

def _train_with_conversations(manager: ChatManager, bot_name: str, training_file: Optional[str]):
    """Train bot with conversation examples"""
    
    console.print("📚 Conversation Training", style="bold cyan")
    
    if training_file:
        console.print(f"Loading training data from {training_file}")
        # Load and process training file
        # This would implement actual training logic
    else:
        console.print("Interactive conversation training:")
        
        examples = []
        while True:
            user_input = Prompt.ask("Training input (or 'done' to finish)")
            if user_input.lower() == 'done':
                break
            
            expected_response = Prompt.ask("Expected response")
            examples.append({"input": user_input, "response": expected_response})
        
        console.print(f"📝 Collected {len(examples)} training examples")
        console.print("🎯 Training simulation - in real implementation would fine-tune the bot")

def _train_personality_adjustment(manager: ChatManager, bot_name: str):
    """Train personality adjustments"""
    
    console.print("🎭 Personality Adjustment Training", style="bold cyan")
    
    # Get current bot configuration
    bot = manager.get_bot(bot_name)
    
    console.print("Current personality traits to adjust:")
    console.print("• Friendliness • Formality • Creativity • Verbosity")
    
    adjustments = {}
    traits = ["friendliness", "formality", "creativity", "verbosity"]
    
    for trait in traits:
        if Confirm.ask(f"Adjust {trait}?", default=False):
            current = 0.5  # Default
            new_value = FloatPrompt.ask(f"{trait.title()} level (0.0-1.0)", default=current)
            adjustments[trait] = new_value
    
    if adjustments:
        console.print(f"✅ Personality adjustments recorded: {adjustments}")
        console.print("🎯 In real implementation, these would modify the system prompt")

def _optimize_performance(manager: ChatManager, bot_name: str):
    """Optimize bot performance"""
    
    console.print("📊 Performance Optimization", style="bold cyan")
    
    if bot_name in enhanced_wrapper.conversation_analytics:
        analytics = enhanced_wrapper.conversation_analytics[bot_name]
        
        console.print("Performance analysis:")
        console.print(f"• Response time: {analytics.average_response_time:.2f}s")
        console.print(f"• User satisfaction: {analytics.average_satisfaction:.1%}")
        console.print(f"• Error rate: {analytics.error_count / max(analytics.total_messages, 1):.1%}")
        
        # Suggest optimizations
        optimizations = []
        
        if analytics.average_response_time > 3.0:
            optimizations.append("Reduce context length for faster responses")
        
        if analytics.average_satisfaction < 0.7:
            optimizations.append("Adjust personality for better user engagement")
        
        if analytics.error_count > analytics.total_messages * 0.05:
            optimizations.append("Review backend configuration for stability")
        
        if optimizations:
            console.print("\n🎯 Recommended optimizations:")
            for opt in optimizations:
                console.print(f"• {opt}")
        else:
            console.print("\n✅ Bot performance is optimal!")
    else:
        console.print("❌ No performance data available for this bot")

@tools.command("export-bot")
@click.argument("bot_name")
@click.option("--format", type=click.Choice(["json", "yaml", "python"]), default="json")
@click.option("--output", help="Output file")
def export_bot(bot_name, format, output):
    """Export bot configuration and personality"""
    
    try:
        manager = ChatManager("config.yaml")
        
        if bot_name not in manager.list_bots():
            console.print(f"❌ Bot '{bot_name}' not found", style="red")
            return
        
        bot_config = manager.config.get_bot_config(bot_name)
        
        # Create export data
        export_data = {
            "bot_name": bot_name,
            "configuration": bot_config.model_dump() if bot_config else {},
            "analytics": enhanced_wrapper.conversation_analytics.get(bot_name, ConversationAnalytics(bot_name)).__dict__,
            "export_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Generate output filename if not provided
        if not output:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output = f"{bot_name}_export_{timestamp}.{format}"
        
        # Export in requested format
        if format == "json":
            with open(output, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
        elif format == "yaml":
            with open(output, 'w') as f:
                yaml.dump(export_data, f, default_flow_style=False)
        elif format == "python":
            _export_as_python_code(export_data, output)
        
        console.print(f"✅ Bot exported to {output}", style="green")
        
    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="red")

def _export_as_python_code(export_data: Dict[str, Any], output: str):
    """Export bot as Python code"""
    
    code = f'''#!/usr/bin/env python3
"""
Bot Configuration: {export_data["bot_name"]}
Generated on: {export_data["export_date"]}
"""

from ai_chat_manager.core.manager import ChatManager
from ai_chat_manager.core.config import BotConfig

def create_{export_data["bot_name"].lower().replace("-", "_")}_bot(manager: ChatManager):
    """Create and configure the {export_data["bot_name"]} bot"""
    
    bot_config = {json.dumps(export_data["configuration"], indent=8)}
    
    bot = manager.create_bot(
        name="{export_data["bot_name"]}",
        **bot_config
    )
    
    return bot

if __name__ == "__main__":
    manager = ChatManager()
    bot = create_{export_data["bot_name"].lower().replace("-", "_")}_bot(manager)
    print(f"Bot {{bot.name}} created successfully!")
'''
    
    with open(output, 'w') as f:
        f.write(code)

# Main entry point
def main():
    """Main entry point for the enhanced CLI wrapper"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
    except Exception as e:
        console.print(f"💥 Unexpected error: {e}", style="red")
    finally:
        enhanced_wrapper.save_all_data()

if __name__ == "__main__":
    main()