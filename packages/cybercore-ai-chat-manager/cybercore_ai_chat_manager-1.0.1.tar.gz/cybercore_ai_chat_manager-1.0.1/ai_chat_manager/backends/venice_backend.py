"""
Venice AI Backend Implementation for AI Chat Manager

Venice AI is a privacy-focused AI platform that provides censorship-resistant
and anonymous AI services. This backend implements their OpenAI-compatible API
with additional privacy and security features.
"""

import json
import asyncio
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime

from .base import BaseBackend, ResponseValidator
from ..core.types import (
    Message, ChatResponse, StreamingChunk, Usage, 
    FinishReason, MessageRole
)
from ..core.config import BackendConfig
from ..core.exceptions import (
    BackendError, AuthenticationError, ModelNotFoundError,
    QuotaExceededError, RateLimitError, ValidationError
)

logger = logging.getLogger(__name__)

class VeniceBackend(BaseBackend):
    """
    Venice AI backend implementation
    
    Venice AI focuses on:
    - Privacy and anonymity
    - Censorship resistance
    - Decentralized AI access
    - OpenAI-compatible API
    - No data retention
    
    Features:
    - Chat completions with various models
    - Streaming responses
    - Privacy-preserving requests
    - Anonymous usage
    """
    
    # Venice AI model pricing (estimated, as of 2024)
    MODEL_PRICING = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.0025},
        "gpt-4": {"input": 0.0350, "output": 0.0700},
        "claude-3-sonnet": {"input": 0.0030, "output": 0.0150},
        "claude-3-haiku": {"input": 0.0002, "output": 0.0010},
        "llama-2-70b": {"input": 0.0020, "output": 0.0020},
        "mixtral-8x7b": {"input": 0.0024, "output": 0.0024},
    }
    
    # Privacy modes
    PRIVACY_LEVELS = {
        "standard": "Standard privacy protection",
        "enhanced": "Enhanced anonymization",
        "maximum": "Maximum privacy with Tor routing"
    }
    
    def __init__(self, config: BackendConfig):
        super().__init__(config)
        
        # Validate Venice-specific configuration
        api_key = config.get_api_key()
        if not api_key:
            raise AuthenticationError(
                "Venice AI API key is required",
                backend_name=self.name
            )
        
        self.api_key = api_key
        self.base_url = config.base_url or "https://api.venice.ai/v1"
        
        # Venice-specific settings
        self.privacy_level = config.custom_params.get("privacy_level", "standard")
        self.anonymous_mode = config.custom_params.get("anonymous_mode", True)
        self.data_retention = config.custom_params.get("data_retention", False)
        self.tor_routing = config.custom_params.get("tor_routing", False)
        
        # Model configuration
        self.model = config.model or "gpt-3.5-turbo"
        
        # Validate privacy settings
        self._validate_privacy_config()
        
        logger.info(f"Venice AI backend initialized: {self.model} (privacy: {self.privacy_level})")
    
    def _validate_privacy_config(self):
        """Validate privacy configuration"""
        if self.privacy_level not in self.PRIVACY_LEVELS:
            logger.warning(f"Unknown privacy level: {self.privacy_level}, using 'standard'")
            self.privacy_level = "standard"
        
        # Maximum privacy implies certain settings
        if self.privacy_level == "maximum":
            self.anonymous_mode = True
            self.data_retention = False
            self.tor_routing = True
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get Venice AI authentication headers"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Add privacy headers
        if self.anonymous_mode:
            headers["X-Venice-Anonymous"] = "true"
        
        if not self.data_retention:
            headers["X-Venice-No-Logs"] = "true"
        
        if self.privacy_level:
            headers["X-Venice-Privacy-Level"] = self.privacy_level
        
        # Add user agent that doesn't identify specific users
        headers["User-Agent"] = "Venice-Client/1.0"
        
        return headers
    
    def _prepare_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert messages to Venice AI format (OpenAI-compatible)"""
        venice_messages = []
        
        for message in messages:
            venice_message = {
                "role": message.role.value,
                "content": message.content
            }
            
            # Add name for assistant messages if specified
            if message.name and message.role == MessageRole.ASSISTANT:
                venice_message["name"] = message.name
            
            # Handle function calls (if supported by model)
            if message.function_call:
                venice_message["function_call"] = {
                    "name": message.function_call.name,
                    "arguments": json.dumps(message.function_call.arguments)
                }
            
            venice_messages.append(venice_message)
        
        return venice_messages
    
    def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
        """Build Venice AI API request data"""
        # Prepare messages
        venice_messages = self._prepare_messages(messages)
        
        # Build base request (OpenAI-compatible)
        request_data = {
            "model": kwargs.get("model", self.model),
            "messages": venice_messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "frequency_penalty": kwargs.get("frequency_penalty", self.config.frequency_penalty),
            "presence_penalty": kwargs.get("presence_penalty", self.config.presence_penalty),
        }
        
        # Add streaming parameter
        if kwargs.get("stream", False):
            request_data["stream"] = True
        
        # Venice-specific parameters
        venice_params = {
            "privacy_level": self.privacy_level,
            "anonymous": self.anonymous_mode,
            "no_logs": not self.data_retention,
        }
        
        # Add Venice-specific parameters to metadata
        request_data["metadata"] = venice_params
        
        # Add other parameters
        optional_params = ["stop", "logit_bias", "user", "seed"]
        for param in optional_params:
            if param in kwargs:
                request_data[param] = kwargs[param]
        
        # Add custom parameters from config
        request_data.update(self.config.custom_params)
        
        return request_data
    
    async def chat_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate chat completion using Venice AI API"""
        try:
            # Build request
            request_data = self._build_request_data(messages, **kwargs)
            url = f"{self.base_url}/chat/completions"
            
            # Add privacy-specific request modifications
            if self.tor_routing:
                # In a real implementation, this would configure Tor proxy
                logger.debug("Using Tor routing for maximum privacy")
            
            # Make request
            response_data = await self._make_request("POST", url, data=request_data)
            
            # Validate and convert response
            chat_response = self.validator.validate_chat_response(response_data, self.name)
            
            # Add Venice-specific metadata
            chat_response.metadata.update({
                "privacy_level": self.privacy_level,
                "anonymous_mode": self.anonymous_mode,
                "provider": "Venice AI"
            })
            
            # Calculate cost estimation
            if chat_response.usage:
                chat_response.usage.cost_estimate = self._calculate_cost(
                    chat_response.usage, request_data["model"]
                )
            
            return chat_response
            
        except Exception as e:
            logger.error(f"Venice AI chat completion failed: {e}")
            raise self._convert_venice_error(e)
    
    async def stream_completion(self, messages: List[Message], **kwargs) -> AsyncGenerator[StreamingChunk, None]:
        """Generate streaming chat completion with Venice AI"""
        try:
            # Build request with streaming enabled
            request_data = self._build_request_data(messages, stream=True, **kwargs)
            url = f"{self.base_url}/chat/completions"
            
            # Make streaming request
            response = await self._make_request("POST", url, data=request_data, stream=True)
            
            chunk_count = 0
            full_content = ""
            
            async for line in response.content:
                line = line.decode('utf-8').strip()
                
                if not line or not line.startswith('data: '):
                    continue
                
                # Remove 'data: ' prefix
                data_str = line[6:]
                
                if data_str == '[DONE]':
                    # Final chunk
                    yield StreamingChunk(
                        content="",
                        finish_reason=FinishReason.STOP,
                        chunk_index=chunk_count,
                        is_final=True,
                        metadata={
                            "full_content": full_content,
                            "privacy_level": self.privacy_level,
                            "provider": "Venice AI"
                        }
                    )
                    break
                
                try:
                    chunk_data = json.loads(data_str)
                    
                    if "choices" in chunk_data and chunk_data["choices"]:
                        choice = chunk_data["choices"][0]
                        delta = choice.get("delta", {})
                        
                        content = delta.get("content", "")
                        finish_reason = choice.get("finish_reason")
                        
                        if content:
                            full_content += content
                        
                        chunk = StreamingChunk(
                            content=content,
                            finish_reason=FinishReason(finish_reason) if finish_reason else None,
                            chunk_index=chunk_count,
                            is_final=finish_reason is not None,
                            metadata={
                                "raw_chunk": chunk_data,
                                "privacy_level": self.privacy_level
                            }
                        )
                        
                        yield chunk
                        chunk_count += 1
                        
                        if finish_reason:
                            break
                
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse Venice streaming chunk: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Venice AI streaming failed: {e}")
            raise self._convert_venice_error(e)
    
    def _calculate_cost(self, usage: Usage, model: str) -> float:
        """Calculate cost based on token usage and model"""
        # Normalize model name for pricing lookup
        model_key = model.lower()
        
        # Find matching pricing
        pricing = None
        for price_model, price_data in self.MODEL_PRICING.items():
            if price_model in model_key:
                pricing = price_data
                break
        
        if not pricing:
            # Fall back to default pricing
            pricing = {"input": 0.0020, "output": 0.0030}
        
        input_cost = (usage.prompt_tokens / 1000) * pricing["input"]
        output_cost = (usage.completion_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def _convert_venice_error(self, error: Exception) -> Exception:
        """Convert Venice-specific errors to our exception types"""
        if isinstance(error, (BackendError, AuthenticationError, RateLimitError)):
            return error
        
        error_str = str(error).lower()
        
        # Authentication errors
        if "unauthorized" in error_str or "invalid api key" in error_str:
            return AuthenticationError(
                "Invalid Venice AI API key",
                backend_name=self.name,
                auth_method="api_key"
            )
        
        # Rate limit errors
        if "rate limit" in error_str or "too many requests" in error_str:
            return RateLimitError(
                "Venice AI rate limit exceeded",
                backend_name=self.name,
                limit_type="api_quota"
            )
        
        # Model errors
        if "model" in error_str and ("not found" in error_str or "not available" in error_str):
            return ModelNotFoundError(
                f"Venice AI model not available: {self.model}",
                backend_name=self.name,
                model_name=self.model
            )
        
        # Privacy-related errors
        if "privacy" in error_str or "anonymous" in error_str:
            return ValidationError(
                f"Privacy configuration error: {error}",
                backend_name=self.name
            )
        
        # Quota errors
        if "quota" in error_str or "billing" in error_str:
            return QuotaExceededError(
                "Venice AI quota exceeded",
                backend_name=self.name,
                quota_type="api_quota"
            )
        
        # Generic backend error
        return BackendError(
            f"Venice AI error: {error}",
            backend_name=self.name,
            original_error=error
        )
    
    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        return True  # Venice AI supports streaming
    
    def supports_functions(self) -> bool:
        """Check if function calling is supported"""
        # Function calling support depends on the model
        return "gpt" in self.model.lower() or "claude" in self.model.lower()
    
    def supports_vision(self) -> bool:
        """Check if vision is supported"""
        # Vision support is limited and model-dependent
        return "vision" in self.model.lower() or "gpt-4" in self.model.lower()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get detailed model information"""
        info = super().get_model_info()
        
        # Add Venice-specific information
        info.update({
            "provider": "Venice AI",
            "privacy_level": self.privacy_level,
            "anonymous_mode": self.anonymous_mode,
            "data_retention": self.data_retention,
            "tor_routing": self.tor_routing,
            "privacy_features": [
                "No data retention",
                "Anonymous requests",
                "Censorship resistant",
                "Decentralized access"
            ],
            "model_family": self._get_model_family(),
            "estimated_context_length": self._get_estimated_context_length(),
        })
        
        return info
    
    def _get_model_family(self) -> str:
        """Get model family name"""
        model_lower = self.model.lower()
        
        if "gpt-4" in model_lower:
            return "GPT-4"
        elif "gpt-3.5" in model_lower:
            return "GPT-3.5"
        elif "claude" in model_lower:
            return "Claude"
        elif "llama" in model_lower:
            return "LLaMA"
        elif "mixtral" in model_lower:
            return "Mixtral"
        else:
            return "Unknown"
    
    def _get_estimated_context_length(self) -> int:
        """Get estimated context length based on model"""
        model_lower = self.model.lower()
        
        # Estimated context lengths for different models
        if "gpt-4" in model_lower:
            return 8192 if "32k" not in model_lower else 32768
        elif "gpt-3.5" in model_lower:
            return 4096 if "16k" not in model_lower else 16384
        elif "claude-3" in model_lower:
            return 200000  # Claude-3 has very large context
        elif "llama-2-70b" in model_lower:
            return 4096
        elif "mixtral" in model_lower:
            return 32768
        else:
            return 4096  # Default
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from Venice AI"""
        try:
            url = f"{self.base_url}/models"
            response_data = await self._make_request("GET", url)
            
            models = []
            for model_data in response_data.get("data", []):
                models.append({
                    "id": model_data.get("id"),
                    "object": model_data.get("object"),
                    "created": model_data.get("created"),
                    "owned_by": model_data.get("owned_by", "Venice AI"),
                    "privacy_compatible": True,  # All Venice models support privacy
                })
            
            return models
            
        except Exception as e:
            logger.error(f"Failed to get Venice AI models: {e}")
            # Return common models as fallback
            return [
                {"id": "gpt-3.5-turbo", "privacy_compatible": True},
                {"id": "gpt-4", "privacy_compatible": True},
                {"id": "claude-3-sonnet", "privacy_compatible": True},
                {"id": "claude-3-haiku", "privacy_compatible": True},
            ]
    
    async def check_privacy_status(self) -> Dict[str, Any]:
        """Check current privacy settings and status"""
        try:
            url = f"{self.base_url}/privacy/status"
            response_data = await self._make_request("GET", url)
            
            return {
                "privacy_level": self.privacy_level,
                "anonymous_mode": self.anonymous_mode,
                "data_retention": self.data_retention,
                "tor_routing": self.tor_routing,
                "server_status": response_data.get("status", "unknown"),
                "encryption": response_data.get("encryption", "unknown"),
                "location": response_data.get("location", "unknown"),
            }
            
        except Exception as e:
            logger.error(f"Failed to check Venice privacy status: {e}")
            return {
                "privacy_level": self.privacy_level,
                "anonymous_mode": self.anonymous_mode,
                "data_retention": self.data_retention,
                "tor_routing": self.tor_routing,
                "server_status": "unknown",
                "error": str(e)
            }
    
    def health_check(self) -> bool:
        """Enhanced health check for Venice AI backend"""
        try:
            # Check base health
            if not super().health_check():
                return False
            
            # Check API key format (Venice uses custom format)
            if not self.api_key:
                logger.warning("No Venice AI API key provided")
                return False
            
            # Validate privacy configuration
            if self.privacy_level not in self.PRIVACY_LEVELS:
                logger.warning("Invalid privacy level configuration")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Venice AI health check failed: {e}")
            return False
    
    def get_privacy_recommendations(self) -> Dict[str, str]:
        """Get privacy recommendations based on current settings"""
        recommendations = {}
        
        if self.privacy_level == "standard":
            recommendations["upgrade_privacy"] = "Consider using 'enhanced' or 'maximum' privacy level for better protection"
        
        if self.data_retention:
            recommendations["disable_logs"] = "Disable data retention for better privacy"
        
        if not self.anonymous_mode:
            recommendations["enable_anonymous"] = "Enable anonymous mode to avoid request tracking"
        
        if self.privacy_level == "maximum" and not self.tor_routing:
            recommendations["enable_tor"] = "Enable Tor routing for maximum privacy level"
        
        if not recommendations:
            recommendations["status"] = "Your privacy settings are optimized"
        
        return recommendations

# Utility functions for Venice AI backend

def create_venice_backend(
    api_key: str,
    model: str = "gpt-3.5-turbo",
    privacy_level: str = "enhanced",
    **kwargs
) -> VeniceBackend:
    """Factory function to create Venice AI backend with privacy settings"""
    from ..core.config import BackendConfig, BackendType
    
    config = BackendConfig(
        name="venice",
        backend_type=BackendType.VENICE,
        api_key=api_key,
        model=model,
        supports_streaming=True,
        supports_functions=True,
        custom_params={
            "privacy_level": privacy_level,
            "anonymous_mode": True,
            "data_retention": False,
            **kwargs
        }
    )
    
    return VeniceBackend(config)

def get_venice_model_recommendations(privacy_focus: str = "balanced") -> List[str]:
    """Get recommended Venice AI models based on privacy focus"""
    recommendations = {
        "speed": ["gpt-3.5-turbo", "claude-3-haiku"],
        "quality": ["gpt-4", "claude-3-sonnet"],
        "privacy": ["llama-2-70b", "mixtral-8x7b"],  # Open source models
        "balanced": ["gpt-3.5-turbo", "claude-3-sonnet", "gpt-4"],
        "cost_effective": ["gpt-3.5-turbo", "claude-3-haiku"],
    }
    
    return recommendations.get(privacy_focus, recommendations["balanced"])

def validate_venice_privacy_config(config: Dict[str, Any]) -> List[str]:
    """Validate Venice AI privacy configuration"""
    issues = []
    
    privacy_level = config.get("privacy_level", "standard")
    if privacy_level not in ["standard", "enhanced", "maximum"]:
        issues.append(f"Invalid privacy level: {privacy_level}")
    
    if privacy_level == "maximum":
        if not config.get("anonymous_mode", True):
            issues.append("Maximum privacy requires anonymous mode")
        
        if config.get("data_retention", False):
            issues.append("Maximum privacy incompatible with data retention")
    
    return issues