"""
Backend implementations for various AI services

Contains base backend class and specific implementations for OpenAI, Venice AI,
HuggingFace, ElevenLabs, and other AI service providers.
"""

from .base import BaseBackend
from .openai_backend import OpenAIBackend
from .venice_backend import VeniceBackend
from .huggingface_backend import HuggingFaceBackend
from .elevenlabs_backend import ElevenLabsBackend

# Backend registry
AVAILABLE_BACKENDS = {
    "openai": OpenAIBackend,
    "venice": VeniceBackend,
    "huggingface": HuggingFaceBackend,
    "elevenlabs": ElevenLabsBackend,
}

def get_backend(name: str) -> type:
    """Get backend class by name"""
    if name not in AVAILABLE_BACKENDS:
        raise ValueError(f"Backend '{name}' not found. Available: {list(AVAILABLE_BACKENDS.keys())}")
    return AVAILABLE_BACKENDS[name]

def get_backend_class(name: str) -> type:
    """Get backend class by name (alias for get_backend for compatibility)"""
    return get_backend(name)

def list_available_backends():
    """List all available backend names"""
    return list(AVAILABLE_BACKENDS.keys())

def get_backend_info(backend_name: str):
    """Get information about a backend"""
    if backend_name not in AVAILABLE_BACKENDS:
        return None
    
    backend_class = AVAILABLE_BACKENDS[backend_name]
    return {
        "name": backend_name,
        "class": backend_class.__name__,
        "module": backend_class.__module__,
        "description": backend_class.__doc__ or "No description available"
    }

def get_backend_recommendations():
    """Get backend recommendations for different use cases"""
    return {
        "general_chat": ["openai", "venice"],
        "privacy_focused": ["venice"],
        "open_source": ["huggingface"],
        "text_to_speech": ["elevenlabs"],
        "function_calling": ["openai"],
        "vision": ["openai"]
    }

def generate_backend_report():
    """Generate a detailed report of all backends"""
    report = {}
    for name in AVAILABLE_BACKENDS:
        report[name] = get_backend_info(name)
    return report

def get_setup_instructions(backend_name: str):
    """Get setup instructions for a backend"""
    instructions = {
        "openai": "Set OPENAI_API_KEY environment variable with your OpenAI API key",
        "venice": "Set VENICE_API_KEY environment variable with your Venice AI API key", 
        "huggingface": "Set HUGGINGFACE_API_KEY environment variable with your HuggingFace API key",
        "elevenlabs": "Set ELEVENLABS_API_KEY environment variable with your ElevenLabs API key"
    }
    return instructions.get(backend_name, "No setup instructions available")

def get_feature_matrix():
    """Get feature support matrix for all backends"""
    return {
        "openai": {
            "streaming": True,
            "function_calling": True,
            "vision": True,
            "audio": False
        },
        "venice": {
            "streaming": True,
            "function_calling": False,
            "vision": False,
            "audio": False
        },
        "huggingface": {
            "streaming": False,
            "function_calling": False,
            "vision": False,
            "audio": False
        },
        "elevenlabs": {
            "streaming": True,
            "function_calling": False,
            "vision": False,
            "audio": True
        }
    }

__all__ = [
    "BaseBackend",
    "OpenAIBackend", 
    "VeniceBackend",
    "HuggingFaceBackend",
    "ElevenLabsBackend",
    "AVAILABLE_BACKENDS",
    "get_backend",
    "get_backend_class",
    "list_available_backends",
    "get_backend_info",
    "get_backend_recommendations",
    "generate_backend_report",
    "get_setup_instructions",
    "get_feature_matrix"
]
