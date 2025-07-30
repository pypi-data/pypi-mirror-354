"""
OpenAI Backend Implementation for AI Chat Manager

This module provides a comprehensive implementation of the OpenAI API backend
with support for chat completions, streaming, function calling, and advanced features.
"""

import json
import asyncio
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from datetime import datetime

from .base import BaseBackend, ResponseValidator
from ..core.types import (
    Message, ChatResponse, StreamingChunk, Usage, 
    FinishReason, FunctionCall, MessageRole, MessageType
)
from ..core.config import BackendConfig
from ..core.exceptions import (
    BackendError, AuthenticationError, ModelNotFoundError,
    QuotaExceededError, RateLimitError, ValidationError
)

logger = logging.getLogger(__name__)

class OpenAIBackend(BaseBackend):
    """
    OpenAI API backend implementation
    
    Supports:
    - Chat completions with GPT-3.5, GPT-4, and other models
    - Streaming responses
    - Function calling
    - Vision capabilities (GPT-4V)
    - Advanced parameters and customization
    """
    
    # Model pricing per 1K tokens (approximate, as of 2024)
    MODEL_PRICING = {
        "gpt-3.5-turbo": {"input": 0.0010, "output": 0.0020},
        "gpt-3.5-turbo-16k": {"input": 0.0030, "output": 0.0040},
        "gpt-4": {"input": 0.0300, "output": 0.0600},
        "gpt-4-32k": {"input": 0.0600, "output": 0.1200},
        "gpt-4-turbo": {"input": 0.0100, "output": 0.0300},
        "gpt-4-vision": {"input": 0.0100, "output": 0.0300},
        "gpt-4o": {"input": 0.0050, "output": 0.0150},
        "gpt-4o-mini": {"input": 0.0001, "output": 0.0004},
    }
    
    def __init__(self, config: BackendConfig):
        super().__init__(config)
        
        # Validate OpenAI-specific configuration
        api_key = config.get_api_key()
        if not api_key:
            raise AuthenticationError(
                "OpenAI API key is required",
                backend_name=self.name
            )
        
        self.api_key = api_key
        self.base_url = config.base_url or "https://api.openai.com/v1"
        self.organization = config.custom_params.get("organization")
        
        # Model validation
        self.model = config.model or "gpt-3.5-turbo"
        self._validate_model()
        
        # Feature flags
        self.supports_streaming_flag = config.supports_streaming
        self.supports_functions_flag = config.supports_functions
        self.supports_vision_flag = config.supports_vision and "vision" in self.model.lower()
        
        logger.info(f"OpenAI backend initialized: {self.model}")
    
    def _validate_model(self):
        """Validate that the model name is reasonable"""
        valid_prefixes = ["gpt-3.5", "gpt-4", "text-", "code-", "davinci", "curie", "babbage", "ada"]
        
        if not any(self.model.startswith(prefix) for prefix in valid_prefixes):
            logger.warning(f"Unknown OpenAI model: {self.model}")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get OpenAI authentication headers"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        
        return headers
    
    def _prepare_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert messages to OpenAI format"""
        openai_messages = []
        
        for message in messages:
            openai_message = {
                "role": message.role.value,
                "content": message.content
            }
            
            # Add name for function messages
            if message.name:
                openai_message["name"] = message.name
            
            # Handle function calls
            if message.function_call:
                openai_message["function_call"] = {
                    "name": message.function_call.name,
                    "arguments": json.dumps(message.function_call.arguments)
                }
            
            # Handle vision content (images)
            if message.attachments and self.supports_vision_flag:
                content_parts = [{"type": "text", "text": message.content}]
                
                for attachment in message.attachments:
                    if attachment.content_type.value.startswith("image/"):
                        if attachment.url:
                            content_parts.append({
                                "type": "image_url",
                                "image_url": {"url": attachment.url}
                            })
                        elif attachment.data:
                            # Convert binary data to base64 data URL
                            import base64
                            b64_data = base64.b64encode(attachment.data).decode()
                            data_url = f"data:{attachment.content_type.value};base64,{b64_data}"
                            content_parts.append({
                                "type": "image_url",
                                "image_url": {"url": data_url}
                            })
                
                openai_message["content"] = content_parts
            
            openai_messages.append(openai_message)
        
        return openai_messages
    
    def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
        """Build OpenAI API request data"""
        # Prepare messages
        openai_messages = self._prepare_messages(messages)
        
        # Build base request
        request_data = {
            "model": kwargs.get("model", self.model),
            "messages": openai_messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "frequency_penalty": kwargs.get("frequency_penalty", self.config.frequency_penalty),
            "presence_penalty": kwargs.get("presence_penalty", self.config.presence_penalty),
        }
        
        # Add streaming parameter
        if kwargs.get("stream", False):
            request_data["stream"] = True
        
        # Add function calling parameters
        if kwargs.get("functions"):
            request_data["functions"] = kwargs["functions"]
        
        if kwargs.get("function_call"):
            request_data["function_call"] = kwargs["function_call"]
        
        # Add tools (newer function calling format)
        if kwargs.get("tools"):
            request_data["tools"] = kwargs["tools"]
            
        if kwargs.get("tool_choice"):
            request_data["tool_choice"] = kwargs["tool_choice"]
        
        # Add other OpenAI-specific parameters
        openai_params = [
            "logit_bias", "user", "seed", "logprobs", "top_logprobs",
            "response_format", "stop"
        ]
        
        for param in openai_params:
            if param in kwargs:
                request_data[param] = kwargs[param]
        
        # Add custom parameters from config
        request_data.update(self.config.custom_params)
        
        return request_data
    
    async def chat_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate chat completion using OpenAI API"""
        try:
            # Build request
            request_data = self._build_request_data(messages, **kwargs)
            url = f"{self.base_url}/chat/completions"
            
            # Make request
            response_data = await self._make_request("POST", url, data=request_data)
            
            # Validate and convert response
            chat_response = self.validator.validate_chat_response(response_data, self.name)
            
            # Add model-specific cost estimation
            if chat_response.usage:
                chat_response.usage.cost_estimate = self._calculate_cost(
                    chat_response.usage, request_data["model"]
                )
            
            return chat_response
            
        except Exception as e:
            logger.error(f"OpenAI chat completion failed: {e}")
            raise self._convert_openai_error(e)
    
    async def stream_completion(self, messages: List[Message], **kwargs) -> AsyncGenerator[StreamingChunk, None]:
        """Generate streaming chat completion"""
        if not self.supports_streaming_flag:
            # Fall back to regular completion
            async for chunk in super().stream_completion(messages, **kwargs):
                yield chunk
            return
        
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
                        metadata={"full_content": full_content}
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
                            metadata={"raw_chunk": chunk_data}
                        )
                        
                        yield chunk
                        chunk_count += 1
                        
                        if finish_reason:
                            break
                
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming chunk: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"OpenAI streaming failed: {e}")
            raise self._convert_openai_error(e)
    
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
            pricing = {"input": 0.0010, "output": 0.0020}
        
        input_cost = (usage.prompt_tokens / 1000) * pricing["input"]
        output_cost = (usage.completion_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def _convert_openai_error(self, error: Exception) -> Exception:
        """Convert OpenAI-specific errors to our exception types"""
        if isinstance(error, (BackendError, AuthenticationError, RateLimitError)):
            return error
        
        error_str = str(error).lower()
        
        # Authentication errors
        if "unauthorized" in error_str or "invalid api key" in error_str:
            return AuthenticationError(
                "Invalid OpenAI API key",
                backend_name=self.name,
                auth_method="api_key"
            )
        
        # Rate limit errors
        if "rate limit" in error_str or "quota" in error_str:
            return RateLimitError(
                "OpenAI rate limit or quota exceeded",
                backend_name=self.name,
                limit_type="api_quota"
            )
        
        # Model errors
        if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
            return ModelNotFoundError(
                f"OpenAI model not found: {self.model}",
                backend_name=self.name,
                model_name=self.model
            )
        
        # Quota errors
        if "insufficient quota" in error_str or "billing" in error_str:
            return QuotaExceededError(
                "OpenAI quota exceeded or billing issue",
                backend_name=self.name,
                quota_type="api_quota"
            )
        
        # Validation errors
        if "invalid" in error_str or "bad request" in error_str:
            return ValidationError(
                f"Invalid request to OpenAI: {error}",
                backend_name=self.name
            )
        
        # Generic backend error
        return BackendError(
            f"OpenAI API error: {error}",
            backend_name=self.name,
            original_error=error
        )
    
    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        return self.supports_streaming_flag
    
    def supports_functions(self) -> bool:
        """Check if function calling is supported"""
        return self.supports_functions_flag and "gpt" in self.model.lower()
    
    def supports_vision(self) -> bool:
        """Check if vision is supported"""
        return self.supports_vision_flag
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get detailed model information"""
        info = super().get_model_info()
        
        # Add OpenAI-specific information
        info.update({
            "provider": "OpenAI",
            "model_family": self._get_model_family(),
            "context_length": self._get_context_length(),
            "pricing": self.MODEL_PRICING.get(self.model.lower()),
            "training_data_cutoff": self._get_training_cutoff(),
        })
        
        return info
    
    def _get_model_family(self) -> str:
        """Get model family name"""
        if "gpt-4" in self.model.lower():
            return "GPT-4"
        elif "gpt-3.5" in self.model.lower():
            return "GPT-3.5"
        elif "davinci" in self.model.lower():
            return "GPT-3"
        else:
            return "Unknown"
    
    def _get_context_length(self) -> int:
        """Get model context length"""
        context_lengths = {
            "gpt-4-32k": 32768,
            "gpt-4-turbo": 128000,
            "gpt-4o": 128000,
            "gpt-4": 8192,
            "gpt-3.5-turbo-16k": 16384,
            "gpt-3.5-turbo": 4096,
        }
        
        for model_name, length in context_lengths.items():
            if model_name in self.model.lower():
                return length
        
        return 4096  # Default
    
    def _get_training_cutoff(self) -> str:
        """Get training data cutoff date"""
        cutoffs = {
            "gpt-4-turbo": "2024-04",
            "gpt-4o": "2023-10",
            "gpt-4": "2021-09",
            "gpt-3.5": "2021-09",
        }
        
        for model_name, cutoff in cutoffs.items():
            if model_name in self.model.lower():
                return cutoff
        
        return "Unknown"
    
    def estimate_tokens(self, text: str) -> int:
        """Improved token estimation for OpenAI models"""
        # More accurate estimation based on OpenAI's tokenization
        # This is still an approximation - use tiktoken for exact counts
        
        # Basic character-based estimation
        char_count = len(text)
        
        # Adjust based on typical OpenAI tokenization patterns
        if char_count == 0:
            return 0
        
        # English text averages about 4 characters per token
        # But varies significantly with content type
        base_estimate = char_count / 4
        
        # Adjust for common patterns
        word_count = len(text.split())
        if word_count > 0:
            # Use word count as a secondary estimate
            word_estimate = word_count * 1.3  # Average 1.3 tokens per word
            
            # Take average of both estimates
            base_estimate = (base_estimate + word_estimate) / 2
        
        return max(1, int(base_estimate))
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from OpenAI API"""
        try:
            url = f"{self.base_url}/models"
            response_data = await self._make_request("GET", url)
            
            models = []
            for model_data in response_data.get("data", []):
                models.append({
                    "id": model_data.get("id"),
                    "object": model_data.get("object"),
                    "created": model_data.get("created"),
                    "owned_by": model_data.get("owned_by"),
                    "permission": model_data.get("permission", []),
                })
            
            return models
            
        except Exception as e:
            logger.error(f"Failed to get OpenAI models: {e}")
            return []
    
    async def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Create text embedding using OpenAI API"""
        try:
            url = f"{self.base_url}/embeddings"
            request_data = {
                "input": text,
                "model": model
            }
            
            response_data = await self._make_request("POST", url, data=request_data)
            
            if "data" in response_data and response_data["data"]:
                return response_data["data"][0]["embedding"]
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to create OpenAI embedding: {e}")
            raise self._convert_openai_error(e)
    
    def health_check(self) -> bool:
        """Enhanced health check for OpenAI backend"""
        try:
            # Check base health
            if not super().health_check():
                return False
            
            # Check API key format
            if not self.api_key or not self.api_key.startswith(("sk-", "sk-proj-")):
                logger.warning("Invalid OpenAI API key format")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False

# Utility functions for OpenAI backend

def create_openai_backend(
    api_key: str,
    model: str = "gpt-3.5-turbo",
    **kwargs
) -> OpenAIBackend:
    """Factory function to create OpenAI backend"""
    from ..core.config import BackendConfig, BackendType
    
    config = BackendConfig(
        name="openai",
        backend_type=BackendType.OPENAI,
        api_key=api_key,
        model=model,
        supports_streaming=True,
        supports_functions=True,
        supports_vision="vision" in model.lower(),
        **kwargs
    )
    
    return OpenAIBackend(config)

def get_openai_model_recommendations(use_case: str = "general") -> List[str]:
    """Get recommended OpenAI models for different use cases"""
    recommendations = {
        "general": ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"],
        "creative": ["gpt-4", "gpt-4-turbo", "gpt-4o"],
        "analytical": ["gpt-4", "gpt-4-turbo"],
        "coding": ["gpt-4", "gpt-4-turbo"],
        "vision": ["gpt-4-vision", "gpt-4o"],
        "cost_effective": ["gpt-4o-mini", "gpt-3.5-turbo"],
        "high_quality": ["gpt-4", "gpt-4-turbo", "gpt-4o"],
    }
    
    return recommendations.get(use_case, recommendations["general"])