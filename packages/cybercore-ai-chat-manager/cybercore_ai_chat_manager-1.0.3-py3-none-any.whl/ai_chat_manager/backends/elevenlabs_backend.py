"""
ElevenLabs Backend Implementation for AI Chat Manager

This module provides integration with ElevenLabs' Text-to-Speech API,
supporting voice synthesis, voice cloning, and audio generation capabilities.
"""

import json
import asyncio
import logging
import base64
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from datetime import datetime
from pathlib import Path
import io

from .base import BaseBackend, ResponseValidator
from ..core.types import (
    Message, ChatResponse, StreamingChunk, Usage, 
    FinishReason, MessageRole, ContentType, FileAttachment
)
from ..core.config import BackendConfig
from ..core.exceptions import (
    BackendError, AuthenticationError, ModelNotFoundError,
    QuotaExceededError, RateLimitError, ValidationError
)

logger = logging.getLogger(__name__)

class ElevenLabsBackend(BaseBackend):
    """
    ElevenLabs Text-to-Speech backend implementation
    
    Supports:
    - Text-to-speech conversion
    - Multiple voice models
    - Voice cloning
    - Audio streaming
    - Voice settings customization
    - Multiple audio formats
    """
    
    # Available voice models and their characteristics
    VOICE_MODELS = {
        "eleven_monolingual_v1": {
            "name": "Eleven Monolingual v1",
            "description": "High quality English model",
            "languages": ["en"],
            "use_case": "English content, high quality"
        },
        "eleven_multilingual_v1": {
            "name": "Eleven Multilingual v1", 
            "description": "Supports multiple languages",
            "languages": ["en", "es", "fr", "de", "it", "pt", "pl", "hi"],
            "use_case": "Multi-language content"
        },
        "eleven_multilingual_v2": {
            "name": "Eleven Multilingual v2",
            "description": "Improved multilingual model",
            "languages": ["en", "es", "fr", "de", "it", "pt", "pl", "hi", "ar", "zh"],
            "use_case": "Latest multilingual model"
        },
        "eleven_turbo_v2": {
            "name": "Eleven Turbo v2",
            "description": "Fast generation with good quality",
            "languages": ["en"],
            "use_case": "Fast English generation"
        }
    }
    
    # Audio output formats
    AUDIO_FORMATS = {
        "mp3_44100_128": {"format": "mp3", "sample_rate": 44100, "bitrate": 128},
        "mp3_22050_32": {"format": "mp3", "sample_rate": 22050, "bitrate": 32},
        "pcm_16000": {"format": "pcm", "sample_rate": 16000, "bitrate": None},
        "pcm_22050": {"format": "pcm", "sample_rate": 22050, "bitrate": None},
        "pcm_44100": {"format": "pcm", "sample_rate": 44100, "bitrate": None},
    }
    
    # Pricing per character (approximate)
    CHARACTER_PRICING = {
        "starter": 0.00003,    # $0.30 per 1K characters
        "creator": 0.000022,   # $0.22 per 1K characters
        "pro": 0.000018,       # $0.18 per 1K characters
        "scale": 0.000012,     # $0.12 per 1K characters
    }
    
    def __init__(self, config: BackendConfig):
        super().__init__(config)
        
        # Validate ElevenLabs configuration
        api_key = config.get_api_key()
        if not api_key:
            raise AuthenticationError(
                "ElevenLabs API key is required",
                backend_name=self.name
            )
        
        self.api_key = api_key
        self.base_url = config.base_url or "https://api.elevenlabs.io/v1"
        
        # Voice and model configuration
        self.default_voice_id = config.custom_params.get("voice_id", "21m00Tcm4TlvDq8ikWAM")  # Rachel
        self.voice_model = config.model or "eleven_monolingual_v1"
        self.output_format = config.custom_params.get("output_format", "mp3_44100_128")
        
        # Voice settings
        self.voice_settings = {
            "stability": config.custom_params.get("stability", 0.5),
            "similarity_boost": config.custom_params.get("similarity_boost", 0.5),
            "style": config.custom_params.get("style", 0.0),
            "use_speaker_boost": config.custom_params.get("use_speaker_boost", True)
        }
        
        # Audio handling
        self.save_audio = config.custom_params.get("save_audio", False)
        self.audio_output_dir = config.custom_params.get("audio_output_dir", "./audio_output")
        
        # Validate configuration
        self._validate_configuration()
        
        logger.info(f"ElevenLabs backend initialized: {self.voice_model} (voice: {self.default_voice_id})")
    
    def _validate_configuration(self):
        """Validate ElevenLabs-specific configuration"""
        if self.voice_model not in self.VOICE_MODELS:
            logger.warning(f"Unknown voice model: {self.voice_model}")
        
        if self.output_format not in self.AUDIO_FORMATS:
            logger.warning(f"Unknown output format: {self.output_format}, using mp3_44100_128")
            self.output_format = "mp3_44100_128"
        
        # Validate voice settings ranges
        self.voice_settings["stability"] = max(0.0, min(1.0, self.voice_settings["stability"]))
        self.voice_settings["similarity_boost"] = max(0.0, min(1.0, self.voice_settings["similarity_boost"]))
        self.voice_settings["style"] = max(0.0, min(1.0, self.voice_settings["style"]))
        
        # Create audio output directory if needed
        if self.save_audio:
            Path(self.audio_output_dir).mkdir(parents=True, exist_ok=True)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get ElevenLabs authentication headers"""
        return {
            "xi-api-key": self.api_key,
        }
    
    def _prepare_messages(self, messages: List[Message]) -> str:
        """Convert messages to text for TTS"""
        # Extract text content from messages
        text_parts = []
        
        for message in messages:
            if message.role == MessageRole.ASSISTANT:
                # Only convert assistant messages to speech
                text_parts.append(message.content)
            elif message.role == MessageRole.USER and len(messages) == 1:
                # If only one user message, convert it
                text_parts.append(message.content)
        
        # If no assistant messages, use the last message
        if not text_parts and messages:
            text_parts.append(messages[-1].content)
        
        return " ".join(text_parts)
    
    def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
        """Build ElevenLabs API request data"""
        # Extract text to synthesize
        text = self._prepare_messages(messages)
        
        # Get voice ID
        voice_id = kwargs.get("voice_id", self.default_voice_id)
        
        # Build voice settings
        voice_settings = self.voice_settings.copy()
        voice_settings.update({
            "stability": kwargs.get("stability", voice_settings["stability"]),
            "similarity_boost": kwargs.get("similarity_boost", voice_settings["similarity_boost"]),
            "style": kwargs.get("style", voice_settings.get("style", 0.0)),
            "use_speaker_boost": kwargs.get("use_speaker_boost", voice_settings.get("use_speaker_boost", True))
        })
        
        return {
            "text": text,
            "model_id": kwargs.get("model", self.voice_model),
            "voice_settings": voice_settings,
            "voice_id": voice_id,
            "output_format": kwargs.get("output_format", self.output_format)
        }
    
    async def chat_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate speech from text using ElevenLabs API"""
        try:
            # Build request data
            request_data = self._build_request_data(messages, **kwargs)
            
            # Generate speech
            audio_data, audio_info = await self._generate_speech(request_data)
            
            # Calculate usage
            text_length = len(request_data["text"])
            usage = Usage(
                prompt_tokens=text_length // 4,  # Rough character to token conversion
                completion_tokens=0,  # No text output
                total_tokens=text_length // 4
            )
            usage.cost_estimate = self._calculate_cost(text_length)
            
            # Create file attachment for audio
            audio_attachment = FileAttachment(
                filename=f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{audio_info['format']}",
                content_type=ContentType.AUDIO_MP3 if audio_info['format'] == 'mp3' else ContentType.AUDIO_WAV,
                size=len(audio_data),
                data=audio_data,
                description=f"Speech synthesis of: {request_data['text'][:50]}..."
            )
            
            # Save audio file if configured
            audio_file_path = None
            if self.save_audio:
                audio_file_path = await self._save_audio_file(audio_data, audio_attachment.filename)
                audio_attachment.url = f"file://{audio_file_path}"
            
            # Create response
            response_content = f"🔊 Generated speech for: \"{request_data['text'][:100]}{'...' if len(request_data['text']) > 100 else ''}\""
            
            chat_response = ChatResponse(
                content=response_content,
                model=self.voice_model,
                backend=self.name,
                finish_reason=FinishReason.STOP,
                usage=usage,
                metadata={
                    "voice_id": request_data["voice_id"],
                    "voice_settings": request_data["voice_settings"],
                    "output_format": request_data["output_format"],
                    "audio_file_path": str(audio_file_path) if audio_file_path else None,
                    "character_count": text_length,
                    "provider": "ElevenLabs"
                }
            )
            
            # Add audio attachment to message
            if hasattr(chat_response, 'attachments'):
                chat_response.attachments = [audio_attachment]
            else:
                # Store in metadata if attachments not supported
                chat_response.metadata["audio_data"] = base64.b64encode(audio_data).decode()
                chat_response.metadata["audio_format"] = audio_info['format']
            
            return chat_response
            
        except Exception as e:
            logger.error(f"ElevenLabs speech generation failed: {e}")
            raise self._convert_elevenlabs_error(e)
    
    async def _generate_speech(self, request_data: Dict[str, Any]) -> tuple[bytes, Dict[str, Any]]:
        """Generate speech using ElevenLabs API"""
        voice_id = request_data.pop("voice_id")
        output_format = request_data.pop("output_format", self.output_format)
        
        # Build URL
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        # Set appropriate headers for audio response
        headers = self._get_default_headers()
        headers.update({
            "Accept": "audio/mpeg" if "mp3" in output_format else "audio/wav",
            "Content-Type": "application/json"
        })
        
        # Add output format to URL parameters
        url += f"?output_format={output_format}"
        
        # Make request
        response = await self._make_request_raw(
            "POST", 
            url, 
            data=request_data,
            headers=headers,
            expect_json=False
        )
        
        # Get audio data
        audio_data = await response.read()
        
        # Get format info
        format_info = self.AUDIO_FORMATS.get(output_format, {"format": "mp3", "sample_rate": 44100})
        
        return audio_data, format_info
    
    async def _make_request_raw(
        self, 
        method: str, 
        url: str, 
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expect_json: bool = True
    ):
        """Make raw HTTP request for binary data"""
        await self._ensure_session()
        
        # Prepare request
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers or self._get_default_headers()
        }
        
        if data:
            request_kwargs["json"] = data
        
        # Apply rate limiting
        await self.rate_limiter.acquire()
        
        # Make request
        async with self.session.request(**request_kwargs) as response:
            if response.status >= 400:
                error_text = await response.text()
                error_data = {"status_code": response.status, "error": error_text}
                
                try:
                    error_json = json.loads(error_text)
                    error_data.update(error_json)
                except json.JSONDecodeError:
                    pass
                
                raise self._convert_elevenlabs_error(
                    BackendError(f"ElevenLabs API error: {error_text}", backend_name=self.name)
                )
            
            return response
    
    async def _save_audio_file(self, audio_data: bytes, filename: str) -> Path:
        """Save audio data to file"""
        output_path = Path(self.audio_output_dir) / filename
        
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        
        logger.info(f"Audio saved to: {output_path}")
        return output_path
    
    def _calculate_cost(self, character_count: int, plan: str = "creator") -> float:
        """Calculate cost based on character count"""
        rate = self.CHARACTER_PRICING.get(plan, self.CHARACTER_PRICING["creator"])
        return character_count * rate
    
    async def stream_completion(self, messages: List[Message], **kwargs) -> AsyncGenerator[StreamingChunk, None]:
        """ElevenLabs doesn't support streaming - return single chunk"""
        response = await self.chat_completion(messages, **kwargs)
        
        yield StreamingChunk(
            content=response.content,
            finish_reason=response.finish_reason,
            is_final=True,
            metadata=response.metadata
        )
    
    def _convert_elevenlabs_error(self, error: Exception) -> Exception:
        """Convert ElevenLabs-specific errors"""
        if isinstance(error, (BackendError, AuthenticationError, RateLimitError)):
            return error
        
        error_str = str(error).lower()
        
        # Authentication errors
        if "unauthorized" in error_str or "invalid api key" in error_str:
            return AuthenticationError(
                "Invalid ElevenLabs API key",
                backend_name=self.name,
                auth_method="api_key"
            )
        
        # Rate limit errors
        if "rate limit" in error_str or "too many requests" in error_str:
            return RateLimitError(
                "ElevenLabs rate limit exceeded",
                backend_name=self.name,
                limit_type="character_quota"
            )
        
        # Voice/model errors
        if "voice" in error_str and ("not found" in error_str or "invalid" in error_str):
            return ModelNotFoundError(
                f"ElevenLabs voice not found: {self.default_voice_id}",
                backend_name=self.name,
                model_name=self.default_voice_id
            )
        
        # Quota errors
        if "quota" in error_str or "character limit" in error_str:
            return QuotaExceededError(
                "ElevenLabs character quota exceeded",
                backend_name=self.name,
                quota_type="character_quota"
            )
        
        # Text validation errors
        if "text" in error_str and ("too long" in error_str or "invalid" in error_str):
            return ValidationError(
                f"Text validation error: {error}",
                backend_name=self.name
            )
        
        # Generic backend error
        return BackendError(
            f"ElevenLabs error: {error}",
            backend_name=self.name,
            original_error=error
        )
    
    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        return False  # ElevenLabs doesn't support real-time streaming yet
    
    def supports_functions(self) -> bool:
        """Check if function calling is supported"""
        return False  # TTS doesn't support function calling
    
    def supports_vision(self) -> bool:
        """Check if vision is supported"""
        return False  # TTS doesn't support vision
    
    def supports_audio(self) -> bool:
        """Check if audio is supported"""
        return True  # This is an audio backend
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get detailed model information"""
        info = super().get_model_info()
        
        model_info = self.VOICE_MODELS.get(self.voice_model, {})
        format_info = self.AUDIO_FORMATS.get(self.output_format, {})
        
        info.update({
            "provider": "ElevenLabs",
            "capability": "text_to_speech",
            "voice_id": self.default_voice_id,
            "voice_model": self.voice_model,
            "model_description": model_info.get("description", "Unknown model"),
            "supported_languages": model_info.get("languages", ["en"]),
            "output_format": self.output_format,
            "sample_rate": format_info.get("sample_rate"),
            "audio_format": format_info.get("format"),
            "voice_settings": self.voice_settings,
        })
        
        return info
    
    async def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices from ElevenLabs"""
        try:
            url = f"{self.base_url}/voices"
            response_data = await self._make_request("GET", url)
            
            voices = []
            for voice_data in response_data.get("voices", []):
                voices.append({
                    "voice_id": voice_data.get("voice_id"),
                    "name": voice_data.get("name"),
                    "category": voice_data.get("category"),
                    "description": voice_data.get("description"),
                    "preview_url": voice_data.get("preview_url"),
                    "available_for_tiers": voice_data.get("available_for_tiers", []),
                    "settings": voice_data.get("settings"),
                })
            
            return voices
            
        except Exception as e:
            logger.error(f"Failed to get ElevenLabs voices: {e}")
            return []
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available TTS models"""
        try:
            url = f"{self.base_url}/models"
            response_data = await self._make_request("GET", url)
            
            models = []
            for model_data in response_data:
                models.append({
                    "model_id": model_data.get("model_id"),
                    "name": model_data.get("name"),
                    "description": model_data.get("description"),
                    "languages": model_data.get("languages", []),
                    "can_be_finetuned": model_data.get("can_be_finetuned", False),
                    "max_characters_request_free_user": model_data.get("max_characters_request_free_user"),
                    "max_characters_request_subscribed_user": model_data.get("max_characters_request_subscribed_user"),
                })
            
            return models
            
        except Exception as e:
            logger.error(f"Failed to get ElevenLabs models: {e}")
            # Return known models as fallback
            return [
                {
                    "model_id": model_id,
                    "name": info["name"],
                    "description": info["description"],
                    "languages": info["languages"]
                }
                for model_id, info in self.VOICE_MODELS.items()
            ]
    
    async def clone_voice(self, name: str, description: str, audio_files: List[bytes]) -> Dict[str, Any]:
        """Clone a voice using audio samples"""
        try:
            url = f"{self.base_url}/voices/add"
            
            # Prepare multipart form data
            form_data = aiohttp.FormData()
            form_data.add_field('name', name)
            form_data.add_field('description', description)
            
            # Add audio files
            for i, audio_data in enumerate(audio_files):
                form_data.add_field(
                    'files',
                    io.BytesIO(audio_data),
                    filename=f'sample_{i}.mp3',
                    content_type='audio/mpeg'
                )
            
            # Make request without JSON content type
            headers = self._get_auth_headers()
            
            await self._ensure_session()
            async with self.session.post(url, data=form_data, headers=headers) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise BackendError(f"Voice cloning failed: {error_text}")
                
                result = await response.json()
                return result
                
        except Exception as e:
            logger.error(f"Voice cloning failed: {e}")
            raise self._convert_elevenlabs_error(e)
    
    async def get_voice_settings(self, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """Get voice settings for a specific voice"""
        try:
            voice_id = voice_id or self.default_voice_id
            url = f"{self.base_url}/voices/{voice_id}/settings"
            
            response_data = await self._make_request("GET", url)
            return response_data
            
        except Exception as e:
            logger.error(f"Failed to get voice settings: {e}")
            return self.voice_settings
    
    def health_check(self) -> bool:
        """Enhanced health check for ElevenLabs backend"""
        try:
            # Check base health
            if not super().health_check():
                return False
            
            # Check API key
            if not self.api_key:
                logger.warning("No ElevenLabs API key provided")
                return False
            
            # Check voice settings are valid
            for setting, value in self.voice_settings.items():
                if setting in ["stability", "similarity_boost", "style"]:
                    if not (0.0 <= value <= 1.0):
                        logger.warning(f"Invalid voice setting {setting}: {value}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"ElevenLabs health check failed: {e}")
            return False

# Utility functions for ElevenLabs backend

def create_elevenlabs_backend(
    api_key: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_monolingual_v1",
    **kwargs
) -> ElevenLabsBackend:
    """Factory function to create ElevenLabs backend"""
    from ..core.config import BackendConfig, BackendType
    
    config = BackendConfig(
        name="elevenlabs",
        backend_type=BackendType.ELEVENLABS,
        api_key=api_key,
        model=model,
        supports_audio=True,
        custom_params={
            "voice_id": voice_id,
            **kwargs
        }
    )
    
    return ElevenLabsBackend(config)

def get_voice_recommendations(use_case: str = "general") -> List[str]:
    """Get recommended voices for different use cases"""
    # These are popular ElevenLabs voice IDs
    recommendations = {
        "general": ["21m00Tcm4TlvDq8ikWAM", "AZnzlk1XvdvUeBnXmlld"],  # Rachel, Domi
        "professional": ["21m00Tcm4TlvDq8ikWAM", "EXAVITQu4vr4xnSDxMaL"],  # Rachel, Bella
        "storytelling": ["ThT5KcBeYPX3keUQqHPh", "XrExE9yKIg1WjnnlVkGX"],  # Dorothy, Matilda
        "educational": ["21m00Tcm4TlvDq8ikWAM", "pNInz6obpgDQGcFmaJgB"],  # Rachel, Adam
        "conversational": ["AZnzlk1XvdvUeBnXmlld", "EXAVITQu4vr4xnSDxMaL"],  # Domi, Bella
        "calm": ["pNInz6obpgDQGcFmaJgB", "21m00Tcm4TlvDq8ikWAM"],  # Adam, Rachel
        "energetic": ["AZnzlk1XvdvUeBnXmlld", "ThT5KcBeYPX3keUQqHPh"],  # Domi, Dorothy
    }
    
    return recommendations.get(use_case, recommendations["general"])

def optimize_voice_settings(content_type: str = "general") -> Dict[str, float]:
    """Get optimized voice settings for different content types"""
    settings = {
        "general": {"stability": 0.5, "similarity_boost": 0.5, "style": 0.0},
        "audiobook": {"stability": 0.7, "similarity_boost": 0.8, "style": 0.1},
        "news": {"stability": 0.6, "similarity_boost": 0.7, "style": 0.0},
        "conversation": {"stability": 0.4, "similarity_boost": 0.6, "style": 0.2},
        "dramatic": {"stability": 0.3, "similarity_boost": 0.4, "style": 0.5},
        "calm": {"stability": 0.8, "similarity_boost": 0.9, "style": 0.0},
        "expressive": {"stability": 0.2, "similarity_boost": 0.3, "style": 0.7},
    }
    
    return settings.get(content_type, settings["general"])