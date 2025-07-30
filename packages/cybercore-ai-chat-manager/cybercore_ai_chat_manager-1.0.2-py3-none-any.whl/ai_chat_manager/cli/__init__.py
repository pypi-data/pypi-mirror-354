"""
Command Line Interface for AI Chat Manager

Provides CLI tools and wrappers for interacting with the chat manager.
"""

from .main import main, cli
from .wrapper import CLIWrapper

__all__ = [
    "main", 
    "cli",
    "CLIWrapper"
]
