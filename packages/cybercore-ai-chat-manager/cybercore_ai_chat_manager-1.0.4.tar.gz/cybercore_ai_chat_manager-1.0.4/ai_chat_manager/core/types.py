"""
Enhanced Type Definitions for AI Chat Manager

This module provides comprehensive type definitions, data models, and validation
for all components of the AI Chat Manager system.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Union, Literal, Callable, AsyncGenerator
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field, validator, root_validator
import asyncio

class MessageRole(str, Enum):
    """Message roles in a conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"

class MessageType(str, Enum):
    """Types of messages"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    FILE = "file"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESULT = "function_result"
    SYSTEM_EVENT = "system_event"

class ContentType(str, Enum):
    """Content types for message content"""
    TEXT_PLAIN = "text/plain"
    TEXT_MARKDOWN = "text/markdown"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    AUDIO_MP3 = "audio/mp3"
    AUDIO_WAV = "audio/wav"
    APPLICATION_JSON = "application/json"
    APPLICATION_PDF = "application/pdf"

class FinishReason(str, Enum):
    """Reasons why a completion finished"""
    STOP = "stop"
    LENGTH = "length"
    FUNCTION_CALL = "function_call"
    CONTENT_FILTER = "content_filter"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

class ModelCapability(str, Enum):
    """AI model capabilities"""
    TEXT_GENERATION = "text_generation"
    TEXT_COMPLETION = "text_completion"
    CHAT_COMPLETION = "chat_completion"
    CODE_GENERATION = "code_generation"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    AUDIO_GENERATION = "audio_generation"
    AUDIO_TRANSCRIPTION = "audio_transcription"
    EMBEDDING = "embedding"
    FINE_TUNING = "fine_tuning"

@dataclass
class Usage:
    """Token usage information"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    _cost_estimate: Optional[float] = None
    
    @property
    def cost_estimate(self) -> float:
        """Get cost estimate in USD"""
        if self._cost_estimate is not None:
            return self._cost_estimate
        # Default rough estimate - actual costs vary significantly
        return (self.prompt_tokens * 0.00001) + (self.completion_tokens * 0.00002)
    
    @cost_estimate.setter
    def cost_estimate(self, value: float):
        """Set cost estimate in USD"""
        self._cost_estimate = value

@dataclass
class FileAttachment:
    """File attachment for messages"""
    filename: str
    content_type: ContentType
    size: int
    data: Optional[bytes] = None
    url: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "content_type": self.content_type.value,
            "size": self.size,
            "url": self.url,
            "description": self.description,
            # Don't include data in dict to avoid serialization issues
        }

@dataclass
class FunctionCall:
    """Function call information"""
    name: str
    arguments: Dict[str, Any]
    call_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "call_id": self.call_id
        }

@dataclass
class FunctionResult:
    """Function execution result"""
    call_id: str
    result: Any
    success: bool = True
    error: Optional[str] = None
    execution_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "call_id": self.call_id,
            "result": self.result,
            "success": self.success,
            "error": self.error,
            "execution_time": self.execution_time
        }

class Message(BaseModel):
    """Enhanced chat message with multimedia support"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole
    content: str
    message_type: MessageType = MessageType.TEXT
    content_type: ContentType = ContentType.TEXT_PLAIN
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Optional fields
    name: Optional[str] = None  # For function messages or named users
    function_call: Optional[FunctionCall] = None
    function_result: Optional[FunctionResult] = None
    attachments: List[FileAttachment] = Field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tokens: Optional[int] = None
    model: Optional[str] = None
    backend: Optional[str] = None
    
    # Conversation context
    parent_id: Optional[str] = None  # For threading
    thread_id: Optional[str] = None
    conversation_id: Optional[str] = None
    
    # Processing information
    processed: bool = False
    processing_time: Optional[float] = None
    retry_count: int = 0
    
    @validator('content')
    def validate_content(cls, v):
        if not isinstance(v, str):
            return str(v)
        return v
    
    def get_text_content(self) -> str:
        """Get text content, handling different content types"""
        if self.content_type == ContentType.TEXT_MARKDOWN:
            # Could add markdown-to-text conversion here
            return self.content
        return self.content
    
    def get_display_content(self, max_length: int = 100) -> str:
        """Get content for display purposes"""
        content = self.get_text_content()
        if len(content) > max_length:
            return content[:max_length-3] + "..."
        return content
    
    def add_attachment(self, attachment: FileAttachment):
        """Add file attachment to message"""
        self.attachments.append(attachment)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = self.model_dump()
        # Convert enum values to strings
        data['role'] = self.role.value
        data['message_type'] = self.message_type.value
        data['content_type'] = self.content_type.value
        data['timestamp'] = self.timestamp.isoformat()
        
        # Handle attachments
        if self.attachments:
            data['attachments'] = [att.to_dict() for att in self.attachments]
        
        # Handle function calls/results
        if self.function_call:
            data['function_call'] = self.function_call.to_dict()
        if self.function_result:
            data['function_result'] = self.function_result.to_dict()
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        # Convert string enums back to enum objects
        if 'role' in data:
            data['role'] = MessageRole(data['role'])
        if 'message_type' in data:
            data['message_type'] = MessageType(data['message_type'])
        if 'content_type' in data:
            data['content_type'] = ContentType(data['content_type'])
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        # Handle function calls
        if 'function_call' in data and data['function_call']:
            data['function_call'] = FunctionCall(**data['function_call'])
        if 'function_result' in data and data['function_result']:
            data['function_result'] = FunctionResult(**data['function_result'])
        
        return cls(**data)

class StreamingChunk(BaseModel):
    """Chunk of streaming response"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    finish_reason: Optional[FinishReason] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    chunk_index: int = 0
    is_final: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    """Enhanced response from AI backend"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    model: str
    backend: str
    finish_reason: Optional[FinishReason] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Token usage
    usage: Optional[Usage] = None
    
    # Function calling
    function_calls: List[FunctionCall] = Field(default_factory=list)
    
    # Streaming support
    is_streaming: bool = False
    chunks: List[StreamingChunk] = Field(default_factory=list)
    
    # Performance metrics
    response_time: Optional[float] = None
    queue_time: Optional[float] = None
    processing_time: Optional[float] = None
    
    # Quality metrics
    confidence_score: Optional[float] = None
    safety_score: Optional[float] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None
    
    # Error information
    error: Optional[str] = None
    warning: Optional[str] = None
    
    def add_chunk(self, chunk: StreamingChunk):
        """Add streaming chunk"""
        self.chunks.append(chunk)
        if not self.is_streaming:
            self.is_streaming = True
    
    def get_total_content(self) -> str:
        """Get complete content from all chunks"""
        if self.chunks:
            return "".join(chunk.content for chunk in self.chunks)
        return self.content
    
    def is_successful(self) -> bool:
        """Check if response was successful"""
        return self.error is None and self.finish_reason != FinishReason.ERROR
    
    def get_cost_estimate(self) -> Optional[float]:
        """Get estimated cost"""
        if self.usage:
            return self.usage.cost_estimate
        return None

class ConversationSummary(BaseModel):
    """Summary of conversation content"""
    
    message_count: int
    total_tokens: int
    unique_participants: List[str]
    start_time: datetime
    end_time: datetime
    duration: timedelta
    topics: List[str] = Field(default_factory=list)
    sentiment: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    
    @property
    def duration_minutes(self) -> float:
        return self.duration.total_seconds() / 60

class ConversationHistory(BaseModel):
    """Enhanced conversation history with analytics"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = Field(default_factory=list)
    bot_name: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    
    # Conversation metadata
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    language: str = "en"
    
    # Analytics
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    
    # Settings
    max_context_length: int = 4000
    context_strategy: str = "sliding_window"  # sliding_window, summarize, truncate
    
    def add_message(self, message: Message):
        """Add message to history with automatic updates"""
        self.messages.append(message)
        self.updated_at = datetime.now()
        self.last_activity = datetime.now()
        
        # Update analytics
        if message.tokens:
            self.total_tokens += message.tokens
        
        # Auto-generate title if this is the first user message
        if not self.title and message.role == MessageRole.USER and len(self.messages) <= 2:
            self.title = self._generate_title(message.content)
    
    def _generate_title(self, content: str) -> str:
        """Generate conversation title from first message"""
        words = content.split()[:6]
        title = " ".join(words)
        if len(content) > len(title):
            title += "..."
        return title
    
    def get_context(self, max_tokens: int = None) -> List[Message]:
        """Get conversation context with smart truncation"""
        max_tokens = max_tokens or self.max_context_length
        
        if self.context_strategy == "sliding_window":
            return self._get_sliding_window_context(max_tokens)
        elif self.context_strategy == "summarize":
            return self._get_summarized_context(max_tokens)
        else:  # truncate
            return self._get_truncated_context(max_tokens)
    
    def _get_sliding_window_context(self, max_tokens: int) -> List[Message]:
        """Get context using sliding window approach"""
        # Simple token estimation: ~4 characters per token
        char_limit = max_tokens * 4
        total_chars = 0
        context = []
        
        # Always include system messages
        system_messages = [msg for msg in self.messages if msg.role == MessageRole.SYSTEM]
        for msg in system_messages:
            context.append(msg)
            total_chars += len(msg.content)
        
        # Add recent messages within limit
        recent_messages = [msg for msg in self.messages if msg.role != MessageRole.SYSTEM]
        for message in reversed(recent_messages):
            message_chars = len(message.content)
            if total_chars + message_chars > char_limit and len(context) > len(system_messages):
                break
            context.insert(-len(system_messages) if system_messages else 0, message)
            total_chars += message_chars
        
        return context
    
    def _get_truncated_context(self, max_tokens: int) -> List[Message]:
        """Get context by truncating older messages"""
        char_limit = max_tokens * 4
        total_chars = 0
        context = []
        
        for message in reversed(self.messages):
            message_chars = len(message.content)
            if total_chars + message_chars > char_limit and context:
                break
            context.insert(0, message)
            total_chars += message_chars
        
        return context
    
    def _get_summarized_context(self, max_tokens: int) -> List[Message]:
        """Get context with summarization (placeholder for AI summarization)"""
        # This would require an AI model to summarize older parts of the conversation
        # For now, fall back to sliding window
        return self._get_sliding_window_context(max_tokens)
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Get message by ID"""
        for message in self.messages:
            if message.id == message_id:
                return message
        return None
    
    def get_messages_by_role(self, role: MessageRole) -> List[Message]:
        """Get all messages by role"""
        return [msg for msg in self.messages if msg.role == role]
    
    def get_recent_messages(self, count: int = 10) -> List[Message]:
        """Get recent messages"""
        return self.messages[-count:] if count < len(self.messages) else self.messages
    
    def clear_messages(self, keep_system: bool = True):
        """Clear conversation history"""
        if keep_system:
            self.messages = [msg for msg in self.messages if msg.role == MessageRole.SYSTEM]
        else:
            self.messages = []
        
        self.updated_at = datetime.now()
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def get_summary(self) -> ConversationSummary:
        """Get conversation summary"""
        if not self.messages:
            return ConversationSummary(
                message_count=0,
                total_tokens=0,
                unique_participants=[],
                start_time=self.created_at,
                end_time=self.updated_at,
                duration=timedelta(0)
            )
        
        participants = set()
        for msg in self.messages:
            if msg.role == MessageRole.USER:
                participants.add(msg.name or "User")
            elif msg.role == MessageRole.ASSISTANT:
                participants.add(self.bot_name)
        
        return ConversationSummary(
            message_count=len(self.messages),
            total_tokens=self.total_tokens,
            unique_participants=list(participants),
            start_time=self.created_at,
            end_time=self.updated_at,
            duration=self.updated_at - self.created_at
        )
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export conversation to dictionary"""
        return {
            "id": self.id,
            "bot_name": self.bot_name,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "language": self.language,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "messages": [msg.to_dict() for msg in self.messages]
        }
    
    def save_to_file(self, file_path: Union[str, Path]):
        """Save conversation to file"""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.export_to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'ConversationHistory':
        """Load conversation from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert timestamps
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Convert messages
        messages = []
        for msg_data in data.get('messages', []):
            messages.append(Message.from_dict(msg_data))
        data['messages'] = messages
        
        return cls(**data)

# Type aliases for common patterns
MessageHandler = Callable[[Message], Any]
ResponseHandler = Callable[[ChatResponse], Any]
StreamHandler = Callable[[StreamingChunk], Any]
ConversationFilter = Callable[[ConversationHistory], bool]

# Async type aliases
AsyncMessageHandler = Callable[[Message], AsyncGenerator[Any, None]]
AsyncResponseHandler = Callable[[ChatResponse], AsyncGenerator[Any, None]]