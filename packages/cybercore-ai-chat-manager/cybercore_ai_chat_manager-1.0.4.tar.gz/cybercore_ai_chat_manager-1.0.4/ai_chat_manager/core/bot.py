"""
Enhanced Bot Implementation for AI Chat Manager

This module provides sophisticated bot functionality including conversation memory,
learning capabilities, personalization, and advanced conversation management.
"""

import json
import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable, Union, AsyncGenerator, Set
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
import uuid
import hashlib

from .types import (
    Message, MessageRole, ChatResponse, ConversationHistory,
    FinishReason, Usage, FunctionCall, StreamingChunk
)
from .config import Config, BotConfig
from .exceptions import (
    BotNotFoundError, BackendError, ValidationError, 
    ConversationError, MemoryError, ContentFilterError
)

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """User profile for personalization"""
    user_id: str
    name: Optional[str] = None
    preferred_style: str = "balanced"
    language: str = "en"
    interests: List[str] = field(default_factory=list)
    conversation_count: int = 0
    total_messages: int = 0
    first_interaction: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    feedback_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def update_interaction(self):
        """Update interaction statistics"""
        now = datetime.now()
        if self.first_interaction is None:
            self.first_interaction = now
        self.last_interaction = now
        self.total_messages += 1

@dataclass
class LearningData:
    """Data structure for bot learning"""
    interaction_id: str
    timestamp: datetime
    user_input: str
    bot_response: str
    user_feedback: Optional[str] = None
    feedback_score: Optional[float] = None
    context_length: int = 0
    response_time: float = 0.0
    topics: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BotMetrics:
    """Bot performance metrics"""
    total_conversations: int = 0
    total_messages: int = 0
    average_response_time: float = 0.0
    total_tokens_used: int = 0
    total_cost: float = 0.0
    user_satisfaction: float = 0.0
    common_topics: List[str] = field(default_factory=list)
    error_count: int = 0
    uptime_hours: float = 0.0
    
    def update_response_time(self, response_time: float):
        """Update average response time"""
        if self.total_messages == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * self.total_messages + response_time) 
                / (self.total_messages + 1)
            )

class ContentFilter:
    """Content filtering and safety system"""
    
    def __init__(self, bot_config: BotConfig):
        self.enabled = bot_config.content_filter_enabled
        self.safety_level = bot_config.safety_level
        self.allowed_topics = set(bot_config.allowed_topics)
        self.blocked_topics = set(bot_config.blocked_topics)
        
        # Load safety keywords
        self.unsafe_patterns = self._load_safety_patterns()
    
    def _load_safety_patterns(self) -> Set[str]:
        """Load safety patterns based on safety level"""
        # This would typically load from a configuration file
        # For now, using basic patterns
        patterns = set()
        
        if self.safety_level in ["medium", "high"]:
            patterns.update([
                "violence", "harmful", "illegal", "dangerous"
            ])
        
        if self.safety_level == "high":
            patterns.update([
                "controversial", "political", "sensitive"
            ])
        
        return patterns
    
    def filter_input(self, content: str) -> bool:
        """Check if input content is safe"""
        if not self.enabled:
            return True
        
        content_lower = content.lower()
        
        # Check blocked topics
        if self.blocked_topics:
            for topic in self.blocked_topics:
                if topic.lower() in content_lower:
                    return False
        
        # Check allowed topics (if specified, content must contain at least one)
        if self.allowed_topics:
            found_allowed = any(
                topic.lower() in content_lower 
                for topic in self.allowed_topics
            )
            if not found_allowed:
                return False
        
        # Check unsafe patterns
        for pattern in self.unsafe_patterns:
            if pattern in content_lower:
                return False
        
        return True
    
    def filter_output(self, content: str) -> bool:
        """Check if output content is safe"""
        return self.filter_input(content)  # Same rules for now

class FunctionManager:
    """Manages function calling capabilities"""
    
    def __init__(self, bot_config: BotConfig):
        self.enabled = bot_config.function_calling_enabled
        self.available_functions = {}
        self._load_functions(bot_config.available_functions)
    
    def _load_functions(self, function_names: List[str]):
        """Load available functions"""
        # This would load actual function implementations
        # For now, just register the names
        for name in function_names:
            self.available_functions[name] = self._create_placeholder_function(name)
    
    def _create_placeholder_function(self, name: str) -> Callable:
        """Create placeholder function"""
        async def placeholder(*args, **kwargs):
            return f"Function {name} called with args: {args}, kwargs: {kwargs}"
        return placeholder
    
    async def execute_function(self, function_call: FunctionCall) -> Any:
        """Execute a function call"""
        if not self.enabled:
            raise ValidationError("Function calling is disabled for this bot")
        
        if function_call.name not in self.available_functions:
            raise ValidationError(f"Function {function_call.name} not available")
        
        func = self.available_functions[function_call.name]
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(**function_call.arguments)
            else:
                result = func(**function_call.arguments)
            return result
        except Exception as e:
            logger.error(f"Function execution failed: {e}")
            raise ValidationError(f"Function execution failed: {str(e)}")

class Bot:
    """
    Enhanced AI Bot with advanced features
    
    This class provides a sophisticated bot implementation with:
    - Conversation memory and context management
    - Learning from user interactions
    - User personalization
    - Content filtering and safety
    - Function calling capabilities
    - Performance monitoring
    """
    
    def __init__(self, name: str, config: Config, backend, user_id: Optional[str] = None):
        self.name = name
        self.config = config
        self.backend = backend
        self.user_id = user_id or "default_user"
        
        # Load bot configuration
        self.bot_config = config.get_bot_config(name)
        if not self.bot_config:
            raise BotNotFoundError(f"Bot '{name}' not found in configuration")
        
        # Initialize components
        self.conversation_history = ConversationHistory(bot_name=name)
        self.content_filter = ContentFilter(self.bot_config)
        self.function_manager = FunctionManager(self.bot_config)
        
        # Initialize data directories
        self._setup_data_directories()
        
        # Load user profile and data
        self.user_profile = self._load_user_profile()
        self.learning_data: List[LearningData] = []
        self.metrics = BotMetrics()
        
        # Load conversation history and learning data
        if self.bot_config.memory_enabled:
            self._load_conversation_history()
        
        if self.bot_config.learning_enabled:
            self._load_learning_data()
        
        # Initialize session
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        
        # Event handlers
        self.message_handlers: List[Callable] = []
        self.response_handlers: List[Callable] = []
        
        logger.info(f"Bot '{name}' initialized for user '{self.user_id}'")
    
    def _setup_data_directories(self):
        """Setup data directories for the bot"""
        global_config = self.config.get_global_config()
        self.data_dir = Path(global_config.data_directory)
        self.bot_data_dir = self.data_dir / "bots" / self.name
        self.user_data_dir = self.bot_data_dir / "users" / self.user_id
        
        # Create directories
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        (self.user_data_dir / "conversations").mkdir(exist_ok=True)
        (self.user_data_dir / "learning").mkdir(exist_ok=True)
    
    def _load_user_profile(self) -> UserProfile:
        """Load or create user profile"""
        profile_file = self.user_data_dir / "profile.json"
        
        if profile_file.exists():
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                    # Convert datetime strings back to datetime objects
                    if data.get('first_interaction'):
                        data['first_interaction'] = datetime.fromisoformat(data['first_interaction'])
                    if data.get('last_interaction'):
                        data['last_interaction'] = datetime.fromisoformat(data['last_interaction'])
                    return UserProfile(**data)
            except Exception as e:
                logger.warning(f"Failed to load user profile: {e}")
        
        # Create new profile
        return UserProfile(user_id=self.user_id)
    
    def _save_user_profile(self):
        """Save user profile to disk"""
        if not self.bot_config.personalization_enabled:
            return
        
        profile_file = self.user_data_dir / "profile.json"
        
        try:
            # Convert to dict and handle datetime serialization
            data = self.user_profile.__dict__.copy()
            if data.get('first_interaction'):
                data['first_interaction'] = data['first_interaction'].isoformat()
            if data.get('last_interaction'):
                data['last_interaction'] = data['last_interaction'].isoformat()
            
            with open(profile_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save user profile: {e}")
    
    def _load_conversation_history(self):
        """Load conversation history from disk"""
        history_file = self.user_data_dir / "conversations" / "current.json"
        
        if history_file.exists():
            try:
                self.conversation_history = ConversationHistory.load_from_file(history_file)
                logger.info(f"Loaded conversation history with {len(self.conversation_history.messages)} messages")
            except Exception as e:
                logger.warning(f"Failed to load conversation history: {e}")
                # Create new history if loading fails
                self.conversation_history = ConversationHistory(bot_name=self.name)
    
    def _save_conversation_history(self):
        """Save conversation history to disk"""
        if not self.bot_config.memory_enabled:
            return
        
        history_file = self.user_data_dir / "conversations" / "current.json"
        
        try:
            self.conversation_history.save_to_file(history_file)
        except Exception as e:
            logger.error(f"Failed to save conversation history: {e}")
    
    def _load_learning_data(self):
        """Load learning data from disk"""
        learning_file = self.user_data_dir / "learning" / "interactions.jsonl"
        
        if learning_file.exists():
            try:
                with open(learning_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            # Convert timestamp string back to datetime
                            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                            self.learning_data.append(LearningData(**data))
                            
                logger.info(f"Loaded {len(self.learning_data)} learning interactions")
            except Exception as e:
                logger.warning(f"Failed to load learning data: {e}")
    
    def _save_learning_interaction(self, learning_data: LearningData):
        """Save learning interaction to disk"""
        if not self.bot_config.learning_enabled:
            return
        
        learning_file = self.user_data_dir / "learning" / "interactions.jsonl"
        
        try:
            # Convert to dict and handle datetime serialization
            data = learning_data.__dict__.copy()
            data['timestamp'] = data['timestamp'].isoformat()
            
            with open(learning_file, 'a') as f:
                f.write(json.dumps(data, default=str) + '\n')
                
        except Exception as e:
            logger.error(f"Failed to save learning interaction: {e}")
    
    async def chat(
        self, 
        user_message: str, 
        stream: bool = False,
        **kwargs
    ) -> Union[ChatResponse, AsyncGenerator[StreamingChunk, None]]:
        """
        Send a message to the bot and get a response
        
        Args:
            user_message: The user's message
            stream: Whether to stream the response
            **kwargs: Additional parameters for the backend
            
        Returns:
            ChatResponse or async generator for streaming
        """
        start_time = datetime.now()
        
        try:
            # Content filtering for input
            if not self.content_filter.filter_input(user_message):
                raise ContentFilterError(
                    "Input content violates safety guidelines",
                    content_type="user_input"
                )
            
            # Create user message
            user_msg = Message(
                role=MessageRole.USER,
                content=user_message,
                conversation_id=self.conversation_history.id,
                session_id=self.session_id
            )
            
            # Update user profile
            self.user_profile.update_interaction()
            
            # Add to conversation history
            self.conversation_history.add_message(user_msg)
            
            # Prepare context with personalization
            context_messages = self._prepare_context()
            
            # Call message handlers
            for handler in self.message_handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(user_msg)
                    else:
                        handler(user_msg)
                except Exception as e:
                    logger.warning(f"Message handler failed: {e}")
            
            # Get response from backend
            if stream:
                return self._handle_streaming_response(context_messages, start_time, **kwargs)
            else:
                return await self._handle_regular_response(context_messages, start_time, **kwargs)
                
        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Chat error: {e}")
            raise
    
    def _prepare_context(self) -> List[Message]:
        """Prepare context messages with personalization"""
        context_messages = []
        
        # Add system prompt with personalization
        system_prompt = self._build_system_prompt()
        if system_prompt:
            system_msg = Message(
                role=MessageRole.SYSTEM,
                content=system_prompt
            )
            context_messages.append(system_msg)
        
        # Add conversation context
        conversation_context = self.conversation_history.get_context(
            max_tokens=self.bot_config.max_context_length
        )
        context_messages.extend(conversation_context)
        
        return context_messages
    
    def _build_system_prompt(self) -> str:
        """Build personalized system prompt"""
        base_prompt = self.bot_config.system_prompt
        
        if not self.bot_config.personalization_enabled:
            return base_prompt
        
        # Add personalization based on user profile
        personalization = []
        
        if self.user_profile.name:
            personalization.append(f"The user's name is {self.user_profile.name}.")
        
        if self.user_profile.preferred_style:
            personalization.append(f"Respond in a {self.user_profile.preferred_style} style.")
        
        if self.user_profile.language != "en":
            personalization.append(f"Respond primarily in {self.user_profile.language}.")
        
        if self.user_profile.interests:
            interests = ", ".join(self.user_profile.interests[:3])
            personalization.append(f"The user is interested in: {interests}.")
        
        if personalization:
            return f"{base_prompt}\n\nPersonalization notes:\n" + "\n".join(personalization)
        
        return base_prompt
    
    async def _handle_regular_response(
        self, 
        context_messages: List[Message], 
        start_time: datetime,
        **kwargs
    ) -> ChatResponse:
        """Handle regular (non-streaming) response"""
        
        # Get response from backend
        response = await self.backend.chat_completion(
            messages=context_messages,
            **kwargs
        )
        
        # Content filtering for output
        if not self.content_filter.filter_output(response.content):
            raise ContentFilterError(
                "Generated content violates safety guidelines",
                content_type="bot_response"
            )
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        response.response_time = response_time
        
        # Create assistant message
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=response.content,
            model=response.model,
            backend=response.backend,
            tokens=response.usage.total_tokens if response.usage else None,
            processing_time=response_time,
            conversation_id=self.conversation_history.id,
            session_id=self.session_id
        )
        
        # Add to conversation history
        self.conversation_history.add_message(assistant_msg)
        
        # Handle function calls if present
        if response.function_calls:
            await self._handle_function_calls(response.function_calls)
        
        # Update metrics
        self._update_metrics(response, response_time)
        
        # Save data
        self._save_conversation_history()
        self._save_user_profile()
        
        # Learning
        if self.bot_config.learning_enabled:
            await self._learn_from_interaction(
                context_messages[-1].content,  # Last user message
                response.content,
                response_time
            )
        
        # Call response handlers
        for handler in self.response_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(response)
                else:
                    handler(response)
            except Exception as e:
                logger.warning(f"Response handler failed: {e}")
        
        return response
    
    async def _handle_streaming_response(
        self, 
        context_messages: List[Message], 
        start_time: datetime,
        **kwargs
    ) -> AsyncGenerator[StreamingChunk, None]:
        """Handle streaming response"""
        
        full_content = ""
        chunk_count = 0
        
        try:
            async for chunk in self.backend.stream_completion(context_messages, **kwargs):
                chunk_count += 1
                chunk.chunk_index = chunk_count
                full_content += chunk.content
                
                yield chunk
                
                if chunk.is_final:
                    break
            
            # Create final response for processing
            response = ChatResponse(
                content=full_content,
                model=kwargs.get("model", self.backend.config.model),
                backend=self.backend.name,
                is_streaming=True,
                response_time=(datetime.now() - start_time).total_seconds()
            )
            
            # Process like regular response
            await self._finalize_response(response, context_messages, start_time)
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            raise
    
    async def _handle_function_calls(self, function_calls: List[FunctionCall]):
        """Handle function calls from the model"""
        for function_call in function_calls:
            try:
                result = await self.function_manager.execute_function(function_call)
                
                # Add function result to conversation
                function_msg = Message(
                    role=MessageRole.FUNCTION,
                    content=json.dumps(result),
                    name=function_call.name,
                    conversation_id=self.conversation_history.id
                )
                self.conversation_history.add_message(function_msg)
                
            except Exception as e:
                logger.error(f"Function call failed: {e}")
                # Add error message
                error_msg = Message(
                    role=MessageRole.FUNCTION,
                    content=json.dumps({"error": str(e)}),
                    name=function_call.name,
                    conversation_id=self.conversation_history.id
                )
                self.conversation_history.add_message(error_msg)
    
    def _update_metrics(self, response: ChatResponse, response_time: float):
        """Update bot performance metrics"""
        self.metrics.total_messages += 1
        self.metrics.update_response_time(response_time)
        
        if response.usage:
            self.metrics.total_tokens_used += response.usage.total_tokens
            if hasattr(response.usage, 'cost_estimate'):
                self.metrics.total_cost += response.usage.cost_estimate
    
    async def _learn_from_interaction(
        self, 
        user_input: str, 
        bot_response: str, 
        response_time: float
    ):
        """Learn from user interactions"""
        learning_data = LearningData(
            interaction_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_input=user_input,
            bot_response=bot_response,
            context_length=len(self.conversation_history.messages),
            response_time=response_time,
            metadata={
                "user_id": self.user_id,
                "bot_name": self.name,
                "session_id": self.session_id
            }
        )
        
        # Extract topics (simple keyword extraction)
        learning_data.topics = self._extract_topics(user_input + " " + bot_response)
        
        # Store learning data
        self.learning_data.append(learning_data)
        self._save_learning_interaction(learning_data)
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simple implementation)"""
        # This is a simplified topic extraction
        # In a real implementation, you might use NLP libraries
        common_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "is", "are", "was", "were", "be",
            "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "can", "i", "you", "he",
            "she", "it", "we", "they", "this", "that", "these", "those"
        }
        
        words = text.lower().split()
        topics = [
            word for word in words 
            if len(word) > 3 and word not in common_words
        ]
        
        # Return unique topics, limited to top 5
        return list(set(topics))[:5]
    
    # Public API methods
    
    def add_message_handler(self, handler: Callable):
        """Add a message handler"""
        self.message_handlers.append(handler)
    
    def add_response_handler(self, handler: Callable):
        """Add a response handler"""
        self.response_handlers.append(handler)
    
    def set_user_preference(self, key: str, value: Any):
        """Set user preference"""
        self.user_profile.preferences[key] = value
        self._save_user_profile()
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        return self.user_profile.preferences.get(key, default)
    
    def add_user_feedback(self, message_id: str, feedback: str, score: Optional[float] = None):
        """Add user feedback for learning"""
        feedback_data = {
            "message_id": message_id,
            "feedback": feedback,
            "score": score,
            "timestamp": datetime.now().isoformat()
        }
        
        self.user_profile.feedback_history.append(feedback_data)
        self._save_user_profile()
        
        # Update satisfaction score
        if score is not None:
            scores = [
                f.get("score") for f in self.user_profile.feedback_history 
                if f.get("score") is not None
            ]
            if scores:
                self.metrics.user_satisfaction = sum(scores) / len(scores)
    
    def clear_history(self, keep_system: bool = True):
        """Clear conversation history"""
        self.conversation_history.clear_messages(keep_system)
        self._save_conversation_history()
        logger.info(f"Conversation history cleared for bot '{self.name}'")
    
    def export_conversation(self, file_path: str):
        """Export conversation to file"""
        self.conversation_history.save_to_file(file_path)
        logger.info(f"Conversation exported to {file_path}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive bot statistics"""
        conversation_summary = self.conversation_history.get_summary()
        
        return {
            "bot_name": self.name,
            "user_id": self.user_id,
            "backend": self.backend.name,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            
            # Configuration
            "memory_enabled": self.bot_config.memory_enabled,
            "learning_enabled": self.bot_config.learning_enabled,
            "personalization_enabled": self.bot_config.personalization_enabled,
            "function_calling_enabled": self.bot_config.function_calling_enabled,
            
            # Conversation stats
            "message_count": len(self.conversation_history.messages),
            "conversation_duration_minutes": conversation_summary.duration_minutes,
            "last_activity": self.conversation_history.last_activity.isoformat(),
            
            # User profile
            "user_conversation_count": self.user_profile.conversation_count,
            "user_total_messages": self.user_profile.total_messages,
            "user_interests": self.user_profile.interests,
            
            # Performance metrics
            "total_tokens_used": self.metrics.total_tokens_used,
            "average_response_time": self.metrics.average_response_time,
            "total_cost": self.metrics.total_cost,
            "user_satisfaction": self.metrics.user_satisfaction,
            "error_count": self.metrics.error_count,
            
            # Learning data
            "learning_interactions": len(self.learning_data),
            "common_topics": self.metrics.common_topics,
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        # Final save of all data
        self._save_conversation_history()
        self._save_user_profile()
        logger.info(f"Bot '{self.name}' session ended")

# Utility functions for bot management

def create_bot_from_template(
    name: str,
    template: str,
    config: Config,
    backend,
    **overrides
) -> Bot:
    """Create bot from predefined template"""
    
    templates = {
        "assistant": {
            "system_prompt": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses.",
            "personality": "helpful",
            "memory_enabled": True,
            "learning_enabled": False,
        },
        "creative": {
            "system_prompt": "You are a creative AI assistant specializing in writing, art, and creative projects.",
            "personality": "creative",
            "memory_enabled": True,
            "learning_enabled": True,
            "temperature": 0.9,
        },
        "researcher": {
            "system_prompt": "You are a research assistant focused on providing accurate, well-sourced information.",
            "personality": "analytical",
            "memory_enabled": True,
            "learning_enabled": True,
            "temperature": 0.3,
        },
        "teacher": {
            "system_prompt": "You are an educational assistant. Explain concepts clearly and adapt to the student's level.",
            "personality": "empathetic",
            "memory_enabled": True,
            "learning_enabled": True,
            "personalization_enabled": True,
        }
    }
    
    if template not in templates:
        raise ValidationError(f"Unknown template: {template}")
    
    # Merge template with overrides
    bot_settings = {**templates[template], **overrides}
    
    # Create bot configuration
    from .config import BotConfig
    bot_config = BotConfig(name=name, backend=backend.name, **bot_settings)
    
    # Save configuration
    config.set_bot_config(name, bot_config)
    
    # Create and return bot
    return Bot(name, config, backend)