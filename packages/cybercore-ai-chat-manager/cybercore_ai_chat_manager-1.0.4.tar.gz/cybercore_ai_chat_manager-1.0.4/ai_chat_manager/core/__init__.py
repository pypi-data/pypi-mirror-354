"""
Core module for AI Chat Manager

Contains the fundamental types, configuration, and core functionality.
"""

from .types import *
from .config import Config, BackendConfig, BotConfig, GlobalConfig
from .bot import Bot
from .manager import ChatManager, create_chat_manager

__all__ = [
    "Config",
    "BackendConfig",
    "BotConfig", 
    "GlobalConfig",
    "Bot", 
    "ChatManager",
    "create_chat_manager",
    # Re-export from types
    "Message",
    "ConversationHistory", 
    "ChatResponse",
    "MessageRole",
    "MessageType",
    "ContentType",
    "FinishReason",
    "ModelCapability"
]
