"""
AI Chat Manager

A comprehensive Python package for managing AI-powered chat conversations
with support for multiple backends, enhanced features, and extensible architecture.
"""

__version__ = "1.0.0"
__author__ = "CyberCore Team"

from .core.manager import ChatManager
from .core.bot import Bot
from .core.types import Message, ConversationHistory, ChatResponse
from .core.config import Config

__all__ = [
    "ChatManager",
    "Bot", 
    "Message",
    "ConversationHistory",
    "ChatResponse",
    "Config"
]
