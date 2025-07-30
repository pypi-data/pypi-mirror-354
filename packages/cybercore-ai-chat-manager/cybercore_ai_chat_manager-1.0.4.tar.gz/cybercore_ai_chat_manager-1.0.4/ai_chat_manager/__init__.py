"""
AI Chat Manager

A comprehensive Python package for managing AI-powered chat conversations
with support for multiple backends, enhanced features, and extensible architecture.
"""

__version__ = "1.0.4"
__author__ = "CyberCore Team"

from .core.manager import ChatManager
from .core.bot import Bot
from .core.types import Message, ConversationHistory, ChatResponse
from .core.config import Config
from .core.enhanced_bot_creation import (
    EnhancedBot,
    EnhancedBotConfig,
    EnhancedBotFactory,
    PersonalityProfile,
    PersonalityTrait,
    BotSkill,
    create_example_bots
)

__all__ = [
    "ChatManager",
    "Bot", 
    "Message",
    "ConversationHistory",
    "ChatResponse",
    "Config",
    "EnhancedBot",
    "EnhancedBotConfig", 
    "EnhancedBotFactory",
    "PersonalityProfile",
    "PersonalityTrait",
    "BotSkill",
    "create_example_bots"
]
