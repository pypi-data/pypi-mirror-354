#!/usr/bin/env python3
"""
AI Chat Manager SDK Wrapper

A simplified Python SDK that provides easy-to-use interfaces for common
AI Chat Manager operations. Perfect for rapid prototyping, scripts, and
applications that need straightforward AI chat functionality.
"""

import asyncio
import json
import os
from typing import Dict, Any, List, Optional, Union, AsyncGenerator, Callable
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import logging

# Import core AI Chat Manager components
from ai_chat_manager.core.manager import ChatManager
from ai_chat_manager.core.bot import Bot
from ai_chat_manager.core.config import Config, BackendConfig, BotConfig
from ai_chat_manager.core.types import Message, ChatResponse, ConversationHistory, MessageRole
from ai_chat_manager.core.exceptions import AIChatManagerError
from ai_chat_manager.backends import list_available_backends

logger = logging.getLogger(__name__)

@dataclass
class QuickConfig:
    """Quick configuration for rapid setup"""
    provider: str = "openai"
    api_key: Optional[str] = None
    model: Optional[str] = None
    config_file: str = "quick_config.yaml"
    data_dir: str = "./data"
    
    def __post_init__(self):
        # Auto-detect API key from environment
        if not self.api_key:
            env_var = f"{self.provider.upper()}_API_KEY"
            self.api_key = os.getenv(env_var)

@dataclass
class ChatSession:
    """Represents an active chat session"""
    bot_name: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_message(self, role: str, content: str, **kwargs):
        """Add message to session history"""
        self.message_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        })

class QuickChat:
    """Simplified chat interface for rapid development"""
    
    def __init__(self, config: Union[QuickConfig, str, Dict[str, Any]] = None):
        """Initialize QuickChat with simplified configuration"""
        
        if isinstance(config, str):
            # String path to config file
            self.config_file = config
            self.manager = ChatManager(config)
            self.quick_config = None
        elif isinstance(config, dict):
            # Dictionary configuration
            self.quick_config = QuickConfig(**config)
            self.manager = None
            self._setup_from_quick_config()
        elif isinstance(config, QuickConfig):
            # QuickConfig object
            self.quick_config = config
            self.manager = None
            self._setup_from_quick_config()
        else:
            # Default configuration
            self.quick_config = QuickConfig()
            self.manager = None
            self._setup_from_quick_config()
    
    def _setup_from_quick_config(self):
        """Setup manager from QuickConfig"""
        if not self.quick_config.api_key:
            raise ValueError(f"API key required. Set {self.quick_config.provider.upper()}_API_KEY environment variable or pass api_key parameter")
        
        # Create manager
        self.manager = ChatManager(self.quick_config.config_file, auto_start=False)
        
        # Add backend
        self.add_backend(
            name=self.quick_config.provider,
            provider=self.quick_config.provider,
            api_key=self.quick_config.api_key,
            model=self.quick_config.model
        )
        
        # Initialize manager
        self.manager.initialize()
    
    def add_backend(self, name: str, provider: str, api_key: str, model: str = None, **kwargs):
        """Add a backend with simplified parameters"""
        
        # Provider-specific defaults
        provider_defaults = {
            "openai": {"model": "gpt-3.5-turbo", "supports_streaming": True, "supports_functions": True},
            "venice": {"privacy_level": "enhanced", "anonymous_mode": True},
            "huggingface": {"model": "microsoft/DialoGPT-large"},
            "elevenlabs": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "save_audio": True}
        }
        
        backend_config = provider_defaults.get(provider, {})
        backend_config.update(kwargs)
        backend_config["api_key"] = api_key
        
        if model:
            backend_config["model"] = model
        
        self.manager.create_backend(name, provider, **backend_config)
        return self
    
    def create_bot(self, name: str, backend: str = None, personality: str = "helpful", **kwargs):
        """Create a bot with simplified configuration"""
        
        backend = backend or self.quick_config.provider if self.quick_config else list(self.manager.backends.keys())[0]
        
        # Personality-based system prompts
        personality_prompts = {
            "helpful": "You are a helpful AI assistant. Be friendly, informative, and concise.",
            "creative": "You are a creative AI assistant. Be imaginative, inspiring, and think outside the box.",
            "analytical": "You are an analytical AI assistant. Be precise, logical, and data-driven.",
            "casual": "You are a casual AI assistant. Be relaxed, conversational, and approachable.",
            "professional": "You are a professional AI assistant. Be formal, accurate, and business-oriented.",
            "teacher": "You are an educational AI assistant. Be patient, clear, and encouraging.",
            "researcher": "You are a research AI assistant. Be thorough, factual, and cite sources when possible."
        }
        
        system_prompt = personality_prompts.get(personality, personality_prompts["helpful"])
        
        bot_config = {
            "system_prompt": system_prompt,
            "personality": personality,
            "memory_enabled": True,
            **kwargs
        }
        
        return self.manager.create_bot(name, backend, **bot_config)
    
    async def chat(self, message: str, bot: str = "assistant", user_id: str = None, **kwargs) -> str:
        """Send a message and get response (async)"""
        
        # Create bot if it doesn't exist
        if bot not in self.manager.list_bots():
            self.create_bot(bot)
        
        response = await self.manager.chat_with_bot(bot, message, user_id=user_id, **kwargs)
        return response
    
    def chat_sync(self, message: str, bot: str = "assistant", user_id: str = None, **kwargs) -> str:
        """Send a message and get response (sync)"""
        return asyncio.run(self.chat(message, bot, user_id, **kwargs))
    
    async def stream_chat(self, message: str, bot: str = "assistant", user_id: str = None, **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        
        # Create bot if it doesn't exist
        if bot not in self.manager.list_bots():
            self.create_bot(bot)
        
        bot_instance = self.manager.get_bot(bot, user_id=user_id)
        
        # Prepare messages
        messages = [Message(role=MessageRole.USER, content=message)]
        
        async for chunk in bot_instance.backend.stream_completion(messages, **kwargs):
            if chunk.content:
                yield chunk.content
    
    def get_bots(self) -> List[str]:
        """Get list of available bots"""
        return self.manager.list_bots()
    
    def get_backends(self) -> List[str]:
        """Get list of available backends"""
        return self.manager.list_backends()
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return self.manager.get_system_status()

class ConversationManager:
    """Manages conversations with persistence and advanced features"""
    
    def __init__(self, quick_chat: QuickChat):
        self.quick_chat = quick_chat
        self.sessions: Dict[str, ChatSession] = {}
    
    def create_session(self, bot_name: str, user_id: str = None, session_id: str = None) -> ChatSession:
        """Create a new conversation session"""
        
        session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = ChatSession(
            bot_name=bot_name,
            user_id=user_id,
            session_id=session_id
        )
        
        self.sessions[session_id] = session
        return session
    
    async def chat_in_session(self, session_id: str, message: str, **kwargs) -> str:
        """Send message in a specific session"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Add user message to session
        session.add_message("user", message)
        
        # Get bot response
        response = await self.quick_chat.chat(
            message, 
            bot=session.bot_name, 
            user_id=session.user_id,
            **kwargs
        )
        
        # Add bot response to session
        session.add_message("assistant", response)
        
        return response
    
    def save_session(self, session_id: str, file_path: str = None):
        """Save session to file"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        file_path = file_path or f"{session_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump({
                "session_id": session.session_id,
                "bot_name": session.bot_name,
                "user_id": session.user_id,
                "metadata": session.metadata,
                "messages": session.message_history
            }, f, indent=2)
    
    def load_session(self, file_path: str) -> str:
        """Load session from file"""
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        session = ChatSession(
            bot_name=data["bot_name"],
            user_id=data.get("user_id"),
            session_id=data["session_id"],
            metadata=data.get("metadata", {}),
            message_history=data.get("messages", [])
        )
        
        self.sessions[session.session_id] = session
        return session.session_id

class BatchProcessor:
    """Process multiple messages in batch"""
    
    def __init__(self, quick_chat: QuickChat):
        self.quick_chat = quick_chat
    
    async def process_batch(self, messages: List[str], bot: str = "assistant", 
                          max_concurrent: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Process multiple messages concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_single(msg, index):
            async with semaphore:
                try:
                    response = await self.quick_chat.chat(msg, bot=bot, **kwargs)
                    return {
                        "index": index,
                        "input": msg,
                        "output": response,
                        "success": True,
                        "error": None,
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    return {
                        "index": index,
                        "input": msg,
                        "output": None,
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
        
        tasks = [process_single(msg, i) for i, msg in enumerate(messages)]
        results = await asyncio.gather(*tasks)
        
        return sorted(results, key=lambda x: x["index"])
    
    def process_batch_sync(self, messages: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Process batch synchronously"""
        return asyncio.run(self.process_batch(messages, **kwargs))
    
    async def process_file(self, input_file: str, output_file: str = None, **kwargs):
        """Process messages from file"""
        
        # Read input file
        input_path = Path(input_file)
        
        if input_path.suffix == ".json":
            with open(input_path, 'r') as f:
                messages = json.load(f)
        elif input_path.suffix in [".txt", ".md"]:
            with open(input_path, 'r') as f:
                messages = [line.strip() for line in f if line.strip()]
        else:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")
        
        # Process messages
        results = await self.process_batch(messages, **kwargs)
        
        # Save results
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = input_path.with_suffix('.results.json')
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

class ModelComparer:
    """Compare responses across different models/backends"""
    
    def __init__(self, quick_chat: QuickChat):
        self.quick_chat = quick_chat
    
    async def compare_models(self, message: str, models: List[str], 
                           bot: str = "assistant") -> Dict[str, Any]:
        """Compare the same message across different models"""
        
        results = {}
        
        for model in models:
            try:
                start_time = datetime.now()
                response = await self.quick_chat.chat(message, bot=bot, model=model)
                end_time = datetime.now()
                
                results[model] = {
                    "response": response,
                    "response_time": (end_time - start_time).total_seconds(),
                    "response_length": len(response),
                    "word_count": len(response.split()),
                    "success": True,
                    "error": None
                }
                
            except Exception as e:
                results[model] = {
                    "response": None,
                    "response_time": 0,
                    "response_length": 0,
                    "word_count": 0,
                    "success": False,
                    "error": str(e)
                }
        
        # Add comparison metrics
        successful_results = {k: v for k, v in results.items() if v["success"]}
        
        if successful_results:
            response_times = [v["response_time"] for v in successful_results.values()]
            response_lengths = [v["response_length"] for v in successful_results.values()]
            
            comparison = {
                "fastest_model": min(successful_results.keys(), key=lambda k: successful_results[k]["response_time"]),
                "longest_response": max(successful_results.keys(), key=lambda k: successful_results[k]["response_length"]),
                "avg_response_time": sum(response_times) / len(response_times),
                "avg_response_length": sum(response_lengths) / len(response_lengths)
            }
            
            results["_comparison"] = comparison
        
        return results

# Convenience classes for specific use cases
class SimpleAssistant:
    """Ultra-simple assistant interface"""
    
    def __init__(self, provider: str = "openai", api_key: str = None, model: str = None):
        config = QuickConfig(provider=provider, api_key=api_key, model=model)
        self.chat_manager = QuickChat(config)
        self.chat_manager.create_bot("assistant")
    
    def ask(self, question: str) -> str:
        """Ask a question and get an answer"""
        return self.chat_manager.chat_sync(question)
    
    async def ask_async(self, question: str) -> str:
        """Ask a question asynchronously"""
        return await self.chat_manager.chat(question)
    
    async def stream_ask(self, question: str) -> AsyncGenerator[str, None]:
        """Ask a question and stream the response"""
        async for chunk in self.chat_manager.stream_chat(question):
            yield chunk

class CreativeWriter:
    """Specialized creative writing assistant"""
    
    def __init__(self, provider: str = "openai", api_key: str = None):
        config = QuickConfig(provider=provider, api_key=api_key)
        self.chat_manager = QuickChat(config)
        self.chat_manager.create_bot("writer", personality="creative", temperature=0.9)
    
    def write_story(self, prompt: str) -> str:
        """Generate a creative story"""
        return self.chat_manager.chat_sync(f"Write a creative story: {prompt}", bot="writer")
    
    def brainstorm(self, topic: str) -> str:
        """Brainstorm ideas"""
        return self.chat_manager.chat_sync(f"Brainstorm creative ideas about: {topic}", bot="writer")
    
    def improve_text(self, text: str) -> str:
        """Improve existing text"""
        return self.chat_manager.chat_sync(f"Improve this text creatively: {text}", bot="writer")

class CodeHelper:
    """Programming assistance"""
    
    def __init__(self, provider: str = "openai", api_key: str = None):
        config = QuickConfig(provider=provider, api_key=api_key)
        self.chat_manager = QuickChat(config)
        self.chat_manager.create_bot("coder", personality="analytical", temperature=0.3)
    
    def debug_code(self, code: str, error: str = None) -> str:
        """Debug code issues"""
        prompt = f"Debug this code: {code}"
        if error:
            prompt += f"\nError: {error}"
        return self.chat_manager.chat_sync(prompt, bot="coder")
    
    def explain_code(self, code: str) -> str:
        """Explain how code works"""
        return self.chat_manager.chat_sync(f"Explain this code: {code}", bot="coder")
    
    def optimize_code(self, code: str) -> str:
        """Optimize code performance"""
        return self.chat_manager.chat_sync(f"Optimize this code: {code}", bot="coder")

# Context managers for resource management
@asynccontextmanager
async def quick_session(config: Union[QuickConfig, Dict[str, Any]] = None):
    """Context manager for quick chat sessions"""
    
    chat_manager = QuickChat(config)
    try:
        yield chat_manager
    finally:
        # Cleanup if needed
        if hasattr(chat_manager.manager, 'shutdown'):
            await chat_manager.manager.shutdown()

@asynccontextmanager
async def conversation_session(bot_name: str, config: Union[QuickConfig, Dict[str, Any]] = None):
    """Context manager for conversation sessions"""
    
    async with quick_session(config) as chat_manager:
        conv_manager = ConversationManager(chat_manager)
        session = conv_manager.create_session(bot_name)
        
        try:
            yield conv_manager, session.session_id
        finally:
            # Auto-save session
            conv_manager.save_session(session.session_id)

# Factory functions
def create_assistant(provider: str = "openai", **kwargs) -> SimpleAssistant:
    """Create a simple assistant"""
    return SimpleAssistant(provider=provider, **kwargs)

def create_writer(provider: str = "openai", **kwargs) -> CreativeWriter:
    """Create a creative writer"""
    return CreativeWriter(provider=provider, **kwargs)

def create_coder(provider: str = "openai", **kwargs) -> CodeHelper:
    """Create a code helper"""
    return CodeHelper(provider=provider, **kwargs)

async def quick_ask(question: str, provider: str = "openai", **kwargs) -> str:
    """One-line function to ask a question"""
    async with quick_session(QuickConfig(provider=provider, **kwargs)) as chat:
        chat.create_bot("temp_assistant")
        return await chat.chat(question, bot="temp_assistant")

def quick_ask_sync(question: str, provider: str = "openai", **kwargs) -> str:
    """Synchronous one-line function to ask a question"""
    return asyncio.run(quick_ask(question, provider, **kwargs))

# Utility functions
def setup_environment(providers: List[str] = None):
    """Setup environment with multiple providers"""
    
    providers = providers or ["openai", "venice", "huggingface"]
    config = {}
    
    for provider in providers:
        api_key_env = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(api_key_env)
        
        if api_key:
            config[f"{provider}_config"] = QuickConfig(provider=provider, api_key=api_key)
            print(f"✅ {provider.title()} configured")
        else:
            print(f"⚠️ {provider.title()} API key not found in {api_key_env}")
    
    return config

def validate_setup(provider: str = "openai") -> bool:
    """Validate that everything is set up correctly"""
    
    try:
        # Test basic functionality
        assistant = create_assistant(provider=provider)
        response = assistant.ask("Hello, this is a test message. Please respond with 'Test successful!'")
        
        return "test successful" in response.lower()
        
    except Exception as e:
        print(f"Setup validation failed: {e}")
        return False

# Example usage functions
def demo_basic_usage():
    """Demonstrate basic SDK usage"""
    
    print("=== AI Chat Manager SDK Demo ===\n")
    
    # Simple assistant
    print("1. Simple Assistant:")
    assistant = create_assistant()
    response = assistant.ask("What is artificial intelligence?")
    print(f"Q: What is artificial intelligence?")
    print(f"A: {response[:100]}...\n")
    
    # Creative writer
    print("2. Creative Writer:")
    writer = create_writer()
    story = writer.write_story("A robot discovers emotions")
    print(f"Story prompt: A robot discovers emotions")
    print(f"Story: {story[:100]}...\n")
    
    # Quick question
    print("3. Quick Question:")
    answer = quick_ask_sync("What's 2+2?")
    print(f"Q: What's 2+2?")
    print(f"A: {answer}\n")

async def demo_advanced_usage():
    """Demonstrate advanced SDK features"""
    
    print("=== Advanced SDK Demo ===\n")
    
    # Batch processing
    print("1. Batch Processing:")
    async with quick_session() as chat:
        chat.create_bot("assistant")
        
        batch_processor = BatchProcessor(chat)
        messages = [
            "What is Python?",
            "Explain machine learning",
            "How does the internet work?"
        ]
        
        results = await batch_processor.process_batch(messages)
        for result in results:
            print(f"Q: {result['input']}")
            print(f"A: {result['output'][:50]}...")
            print()
    
    # Model comparison
    print("2. Model Comparison:")
    async with quick_session() as chat:
        chat.create_bot("assistant")
        
        comparer = ModelComparer(chat)
        comparison = await comparer.compare_models(
            "Explain quantum computing briefly",
            ["gpt-3.5-turbo", "gpt-4"]
        )
        
        for model, result in comparison.items():
            if model != "_comparison":
                print(f"{model}: {result['response'][:50]}...")
        print()

if __name__ == "__main__":
    # Run demos if script is executed directly
    print("Running AI Chat Manager SDK demos...\n")
    
    try:
        demo_basic_usage()
        asyncio.run(demo_advanced_usage())
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure you have API keys configured!")
