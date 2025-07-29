"""
HuggingFace Backend Implementation for AI Chat Manager

This module provides integration with HuggingFace's Inference API and local models,
supporting both hosted models via the Inference API and local model execution
with transformers library.
"""

import json
import asyncio
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from datetime import datetime
import re

from .base import BaseBackend, ResponseValidator
from ..core.types import (
    Message, ChatResponse, StreamingChunk, Usage, 
    FinishReason, MessageRole
)
from ..core.config import BackendConfig
from ..core.exceptions import (
    BackendError, AuthenticationError, ModelNotFoundError,
    QuotaExceededError, RateLimitError, ValidationError,
    ModelCapabilityError
)

logger = logging.getLogger(__name__)

class HuggingFaceBackend(BaseBackend):
    """
    HuggingFace backend implementation
    
    Supports:
    - HuggingFace Inference API (hosted models)
    - Local model execution with transformers
    - Text generation models
    - Conversational models
    - Custom fine-tuned models
    - Various model architectures (GPT, LLaMA, Flan-T5, etc.)
    """
    
    # Common model categories and their optimal settings
    MODEL_CATEGORIES = {
        "conversational": {
            "examples": ["microsoft/DialoGPT-large", "facebook/blenderbot-400M-distill"],
            "format": "conversational",
            "supports_chat": True
        },
        "text_generation": {
            "examples": ["gpt2", "EleutherAI/gpt-neo-2.7B", "microsoft/DialoGPT-medium"],
            "format": "completion",
            "supports_chat": False
        },
        "instruction_following": {
            "examples": ["google/flan-t5-large", "microsoft/DialoGPT-large"],
            "format": "instruction",
            "supports_chat": True
        },
        "code_generation": {
            "examples": ["Salesforce/codegen-350M-mono", "microsoft/CodeGPT-small-py"],
            "format": "code",
            "supports_chat": False
        },
        "llama": {
            "examples": ["meta-llama/Llama-2-7b-chat-hf", "meta-llama/Llama-2-13b-chat-hf"],
            "format": "llama_chat",
            "supports_chat": True
        }
    }
    
    # Approximate pricing for HuggingFace Inference API (per 1K tokens)
    INFERENCE_PRICING = {
        "small": {"input": 0.0001, "output": 0.0002},  # < 1B parameters
        "medium": {"input": 0.0005, "output": 0.0010}, # 1B - 10B parameters
        "large": {"input": 0.0020, "output": 0.0040},  # > 10B parameters
    }
    
    def __init__(self, config: BackendConfig):
        super().__init__(config)
        
        # Configuration
        self.api_key = config.get_api_key()
        self.base_url = config.base_url or "https://api-inference.huggingface.co"
        self.model = config.model or "microsoft/DialoGPT-large"
        self.use_local = config.custom_params.get("use_local", False)
        
        # Model configuration
        self.model_category = self._detect_model_category()
        self.conversation_format = self._get_conversation_format()
        
        # Local model setup
        self.local_model = None
        self.local_tokenizer = None
        
        if self.use_local:
            self._setup_local_model()
        elif not self.api_key:
            logger.warning("No HuggingFace API key provided - some models may not work")
        
        logger.info(f"HuggingFace backend initialized: {self.model} ({'local' if self.use_local else 'API'})")
    
    def _detect_model_category(self) -> str:
        """Detect model category based on model name"""
        model_lower = self.model.lower()
        
        for category, info in self.MODEL_CATEGORIES.items():
            for example in info["examples"]:
                if example.lower() in model_lower or any(part in model_lower for part in example.lower().split("/")):
                    return category
        
        # Default categorization based on common patterns
        if "dialog" in model_lower or "chat" in model_lower:
            return "conversational"
        elif "llama" in model_lower:
            return "llama"
        elif "flan" in model_lower or "t5" in model_lower:
            return "instruction_following"
        elif "code" in model_lower:
            return "code_generation"
        else:
            return "text_generation"
    
    def _get_conversation_format(self) -> str:
        """Get the conversation format for this model"""
        return self.MODEL_CATEGORIES.get(self.model_category, {}).get("format", "completion")
    
    def _setup_local_model(self):
        """Setup local model using transformers"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            import torch
            
            logger.info(f"Loading local model: {self.model}")
            
            # Load tokenizer
            self.local_tokenizer = AutoTokenizer.from_pretrained(self.model)
            
            # Set pad token if not present
            if self.local_tokenizer.pad_token is None:
                self.local_tokenizer.pad_token = self.local_tokenizer.eos_token
            
            # Load model
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.local_model = AutoModelForCausalLM.from_pretrained(
                self.model,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.local_model,
                tokenizer=self.local_tokenizer,
                device=0 if device == "cuda" else -1,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            
            logger.info(f"Local model loaded successfully on {device}")
            
        except ImportError:
            raise ModelCapabilityError(
                "Transformers library not available for local models",
                model_name=self.model,
                requested_capability="local_execution"
            )
        except Exception as e:
            logger.error(f"Failed to load local model: {e}")
            raise ModelNotFoundError(
                f"Failed to load local model {self.model}: {e}",
                model_name=self.model
            )
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get HuggingFace authentication headers"""
        headers = {}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def _prepare_messages(self, messages: List[Message]) -> Union[str, List[Dict[str, Any]]]:
        """Convert messages to HuggingFace format based on model type"""
        
        if self.conversation_format == "conversational":
            return self._prepare_conversational_format(messages)
        elif self.conversation_format == "llama_chat":
            return self._prepare_llama_format(messages)
        elif self.conversation_format == "instruction":
            return self._prepare_instruction_format(messages)
        else:
            return self._prepare_completion_format(messages)
    
    def _prepare_conversational_format(self, messages: List[Message]) -> Dict[str, Any]:
        """Prepare messages for conversational models (like DialoGPT)"""
        past_user_inputs = []
        generated_responses = []
        current_input = ""
        
        for message in messages:
            if message.role == MessageRole.USER:
                if current_input:  # If we have a previous input, it becomes past
                    past_user_inputs.append(current_input)
                current_input = message.content
            elif message.role == MessageRole.ASSISTANT:
                generated_responses.append(message.content)
            # Skip system messages for now as DialoGPT doesn't handle them well
        
        return {
            "inputs": {
                "past_user_inputs": past_user_inputs,
                "generated_responses": generated_responses,
                "text": current_input
            }
        }
    
    def _prepare_llama_format(self, messages: List[Message]) -> str:
        """Prepare messages for LLaMA chat format"""
        formatted_messages = []
        
        for message in messages:
            if message.role == MessageRole.SYSTEM:
                formatted_messages.append(f"<<SYS>>\n{message.content}\n<</SYS>>")
            elif message.role == MessageRole.USER:
                formatted_messages.append(f"[INST] {message.content} [/INST]")
            elif message.role == MessageRole.ASSISTANT:
                formatted_messages.append(message.content)
        
        return " ".join(formatted_messages)
    
    def _prepare_instruction_format(self, messages: List[Message]) -> str:
        """Prepare messages for instruction-following models"""
        instruction_parts = []
        
        # Find system message for context
        system_context = ""
        for message in messages:
            if message.role == MessageRole.SYSTEM:
                system_context = message.content
                break
        
        # Build conversation history
        conversation = []
        for message in messages:
            if message.role == MessageRole.USER:
                conversation.append(f"Human: {message.content}")
            elif message.role == MessageRole.ASSISTANT:
                conversation.append(f"Assistant: {message.content}")
        
        # Format as instruction
        if system_context:
            instruction_parts.append(f"Context: {system_context}")
        
        if conversation:
            instruction_parts.append("Conversation:\n" + "\n".join(conversation))
            instruction_parts.append("Assistant:")
        
        return "\n\n".join(instruction_parts)
    
    def _prepare_completion_format(self, messages: List[Message]) -> str:
        """Prepare messages for text completion models"""
        text_parts = []
        
        for message in messages:
            if message.role == MessageRole.SYSTEM:
                text_parts.append(f"System: {message.content}")
            elif message.role == MessageRole.USER:
                text_parts.append(f"User: {message.content}")
            elif message.role == MessageRole.ASSISTANT:
                text_parts.append(f"Assistant: {message.content}")
        
        # Add prompt for assistant response
        text_parts.append("Assistant:")
        
        return "\n".join(text_parts)
    
    def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
        """Build HuggingFace API request data"""
        # Prepare input based on model type
        inputs = self._prepare_messages(messages)
        
        # Build parameters
        parameters = {
            "max_new_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "repetition_penalty": kwargs.get("repetition_penalty", 1.1),
            "return_full_text": kwargs.get("return_full_text", False),
            "do_sample": kwargs.get("temperature", self.config.temperature) > 0,
        }
        
        # Handle different input formats
        if isinstance(inputs, dict):
            # Conversational format
            request_data = {
                "inputs": inputs,
                "parameters": parameters
            }
        else:
            # Text format
            request_data = {
                "inputs": inputs,
                "parameters": parameters
            }
        
        # Add streaming if supported
        if kwargs.get("stream", False):
            request_data["stream"] = True
        
        # Add custom parameters
        if self.config.custom_params:
            parameters.update(self.config.custom_params)
        
        return request_data
    
    async def chat_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate chat completion using HuggingFace API or local model"""
        try:
            if self.use_local:
                return await self._local_completion(messages, **kwargs)
            else:
                return await self._api_completion(messages, **kwargs)
                
        except Exception as e:
            logger.error(f"HuggingFace chat completion failed: {e}")
            raise self._convert_huggingface_error(e)
    
    async def _api_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate completion using HuggingFace Inference API"""
        # Build request
        request_data = self._build_request_data(messages, **kwargs)
        url = f"{self.base_url}/models/{self.model}"
        
        # Make request
        response_data = await self._make_request("POST", url, data=request_data)
        
        # Parse response based on model type
        content = self._extract_content_from_response(response_data, messages)
        
        # Create usage estimation
        input_text = str(request_data.get("inputs", ""))
        estimated_input_tokens = self.estimate_tokens(input_text)
        estimated_output_tokens = self.estimate_tokens(content)
        
        usage = Usage(
            prompt_tokens=estimated_input_tokens,
            completion_tokens=estimated_output_tokens,
            total_tokens=estimated_input_tokens + estimated_output_tokens
        )
        
        # Create response
        chat_response = ChatResponse(
            content=content,
            model=self.model,
            backend=self.name,
            finish_reason=FinishReason.STOP,
            usage=usage,
            metadata={
                "model_category": self.model_category,
                "conversation_format": self.conversation_format,
                "raw_response": response_data
            }
        )
        
        # Add cost estimation
        usage.cost_estimate = self._calculate_cost(usage)
        
        return chat_response
    
    async def _local_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate completion using local model"""
        if not self.pipeline:
            raise ModelCapabilityError(
                "Local model not available",
                model_name=self.model
            )
        
        # Prepare input
        input_text = self._prepare_messages(messages)
        if isinstance(input_text, dict):
            # Handle conversational format
            input_text = input_text["inputs"]["text"]
        
        # Generate response
        loop = asyncio.get_event_loop()
        
        def generate():
            return self.pipeline(
                input_text,
                max_new_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                top_p=kwargs.get("top_p", self.config.top_p),
                do_sample=kwargs.get("temperature", self.config.temperature) > 0,
                pad_token_id=self.local_tokenizer.eos_token_id,
                return_full_text=False
            )
        
        # Run generation in thread pool to avoid blocking
        result = await loop.run_in_executor(None, generate)
        
        # Extract content
        if isinstance(result, list) and result:
            content = result[0].get("generated_text", "")
        else:
            content = str(result)
        
        # Clean up content
        content = self._clean_generated_content(content, input_text)
        
        # Create usage estimation
        estimated_input_tokens = self.estimate_tokens(input_text)
        estimated_output_tokens = self.estimate_tokens(content)
        
        usage = Usage(
            prompt_tokens=estimated_input_tokens,
            completion_tokens=estimated_output_tokens,
            total_tokens=estimated_input_tokens + estimated_output_tokens
        )
        
        return ChatResponse(
            content=content,
            model=self.model,
            backend=self.name,
            finish_reason=FinishReason.STOP,
            usage=usage,
            metadata={
                "execution_type": "local",
                "model_category": self.model_category
            }
        )
    
    def _extract_content_from_response(self, response_data: Any, original_messages: List[Message]) -> str:
        """Extract content from HuggingFace API response"""
        if isinstance(response_data, list) and response_data:
            # Text generation response
            item = response_data[0]
            if isinstance(item, dict):
                content = item.get("generated_text", "")
            else:
                content = str(item)
        elif isinstance(response_data, dict):
            # Conversational response
            if "conversation" in response_data:
                content = response_data["conversation"].get("generated_responses", [""])[-1]
            elif "generated_text" in response_data:
                content = response_data["generated_text"]
            else:
                content = str(response_data)
        else:
            content = str(response_data)
        
        # Clean up content
        original_input = self._prepare_messages(original_messages)
        if isinstance(original_input, str):
            content = self._clean_generated_content(content, original_input)
        
        return content
    
    def _clean_generated_content(self, content: str, original_input: str) -> str:
        """Clean generated content from artifacts"""
        # Remove original input if it was included
        if isinstance(original_input, str) and content.startswith(original_input):
            content = content[len(original_input):].strip()
        
        # Remove common artifacts
        content = content.strip()
        
        # Remove "Assistant:" prefix if present
        if content.startswith("Assistant:"):
            content = content[10:].strip()
        
        # Remove repetitive patterns
        content = re.sub(r'(.+?)\1{2,}', r'\1', content)
        
        # Truncate at natural stopping points
        stop_patterns = ["\nUser:", "\nHuman:", "\n\nUser:", "\n\nHuman:", "<|endoftext|>"]
        for pattern in stop_patterns:
            if pattern in content:
                content = content.split(pattern)[0]
        
        return content.strip()
    
    def _calculate_cost(self, usage: Usage) -> float:
        """Calculate cost estimation for HuggingFace usage"""
        # Estimate model size category
        model_lower = self.model.lower()
        
        if any(size in model_lower for size in ["small", "mini", "350m", "125m"]):
            pricing = self.INFERENCE_PRICING["small"]
        elif any(size in model_lower for size in ["large", "7b", "13b", "6b"]):
            pricing = self.INFERENCE_PRICING["large"]
        else:
            pricing = self.INFERENCE_PRICING["medium"]
        
        input_cost = (usage.prompt_tokens / 1000) * pricing["input"]
        output_cost = (usage.completion_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def _convert_huggingface_error(self, error: Exception) -> Exception:
        """Convert HuggingFace-specific errors"""
        if isinstance(error, (BackendError, AuthenticationError, RateLimitError)):
            return error
        
        error_str = str(error).lower()
        
        # Authentication errors
        if "unauthorized" in error_str or "invalid token" in error_str:
            return AuthenticationError(
                "Invalid HuggingFace API token",
                backend_name=self.name,
                auth_method="api_token"
            )
        
        # Rate limit errors
        if "rate limit" in error_str or "too many requests" in error_str:
            return RateLimitError(
                "HuggingFace rate limit exceeded",
                backend_name=self.name,
                limit_type="inference_api"
            )
        
        # Model errors
        if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
            return ModelNotFoundError(
                f"HuggingFace model not found: {self.model}",
                backend_name=self.name,
                model_name=self.model
            )
        
        # Model loading errors
        if "loading" in error_str or "starting" in error_str:
            return ModelCapabilityError(
                f"Model is loading, please try again: {self.model}",
                model_name=self.model,
                requested_capability="immediate_inference"
            )
        
        # Quota errors
        if "quota" in error_str or "limit exceeded" in error_str:
            return QuotaExceededError(
                "HuggingFace quota exceeded",
                backend_name=self.name,
                quota_type="inference_quota"
            )
        
        # Generic backend error
        return BackendError(
            f"HuggingFace error: {error}",
            backend_name=self.name,
            original_error=error
        )
    
    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        # HuggingFace Inference API has limited streaming support
        return False
    
    def supports_functions(self) -> bool:
        """Check if function calling is supported"""
        # Most HuggingFace models don't support function calling
        return False
    
    def supports_vision(self) -> bool:
        """Check if vision is supported"""
        # Vision models would need special handling
        return "vision" in self.model.lower() or "vit" in self.model.lower()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get detailed model information"""
        info = super().get_model_info()
        
        # Add HuggingFace-specific information
        info.update({
            "provider": "HuggingFace",
            "execution_type": "local" if self.use_local else "api",
            "model_category": self.model_category,
            "conversation_format": self.conversation_format,
            "supports_chat": self.MODEL_CATEGORIES.get(self.model_category, {}).get("supports_chat", False),
            "model_url": f"https://huggingface.co/{self.model}",
        })
        
        if self.use_local and self.local_model:
            info.update({
                "local_device": str(self.local_model.device),
                "model_dtype": str(self.local_model.dtype),
                "parameters": self._estimate_parameters(),
            })
        
        return info
    
    def _estimate_parameters(self) -> str:
        """Estimate model parameters based on name"""
        model_lower = self.model.lower()
        
        # Extract parameter count from model name
        param_patterns = [
            (r'(\d+)b', lambda x: f"{x}B parameters"),
            (r'(\d+)m', lambda x: f"{x}M parameters"),
            (r'350m', lambda x: "350M parameters"),
            (r'125m', lambda x: "125M parameters"),
            (r'large', lambda x: "~1B parameters"),
            (r'medium', lambda x: "~300M parameters"),
            (r'small', lambda x: "~100M parameters"),
        ]
        
        for pattern, formatter in param_patterns:
            match = re.search(pattern, model_lower)
            if match:
                if match.groups():
                    return formatter(match.group(1))
                else:
                    return formatter(None)
        
        return "Unknown"
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models (popular ones)"""
        # This would ideally call HuggingFace's model API
        # For now, return a curated list of popular models
        popular_models = [
            {
                "id": "microsoft/DialoGPT-large",
                "category": "conversational",
                "description": "Large conversational model",
                "parameters": "774M"
            },
            {
                "id": "microsoft/DialoGPT-medium", 
                "category": "conversational",
                "description": "Medium conversational model",
                "parameters": "355M"
            },
            {
                "id": "google/flan-t5-large",
                "category": "instruction_following",
                "description": "Instruction-following model",
                "parameters": "780M"
            },
            {
                "id": "EleutherAI/gpt-neo-2.7B",
                "category": "text_generation", 
                "description": "Large text generation model",
                "parameters": "2.7B"
            },
            {
                "id": "meta-llama/Llama-2-7b-chat-hf",
                "category": "llama",
                "description": "LLaMA 2 chat model",
                "parameters": "7B"
            }
        ]
        
        return popular_models
    
    def health_check(self) -> bool:
        """Enhanced health check for HuggingFace backend"""
        try:
            # Check base health
            if not super().health_check():
                return False
            
            if self.use_local:
                # Check local model availability
                return self.local_model is not None and self.local_tokenizer is not None
            else:
                # Check API access
                return True  # Will be validated on first request
                
        except Exception as e:
            logger.error(f"HuggingFace health check failed: {e}")
            return False

# Utility functions for HuggingFace backend

def create_huggingface_backend(
    model: str,
    api_key: Optional[str] = None,
    use_local: bool = False,
    **kwargs
) -> HuggingFaceBackend:
    """Factory function to create HuggingFace backend"""
    from ..core.config import BackendConfig, BackendType
    
    config = BackendConfig(
        name="huggingface",
        backend_type=BackendType.HUGGINGFACE,
        api_key=api_key,
        model=model,
        custom_params={
            "use_local": use_local,
            **kwargs
        }
    )
    
    return HuggingFaceBackend(config)

def get_huggingface_model_recommendations(task: str = "chat") -> List[str]:
    """Get recommended HuggingFace models for different tasks"""
    recommendations = {
        "chat": [
            "microsoft/DialoGPT-large",
            "meta-llama/Llama-2-7b-chat-hf",
            "google/flan-t5-large"
        ],
        "text_generation": [
            "EleutherAI/gpt-neo-2.7B",
            "EleutherAI/gpt-j-6B",
            "gpt2-large"
        ],
        "instruction": [
            "google/flan-t5-large",
            "google/flan-t5-xl",
            "microsoft/DialoGPT-large"
        ],
        "code": [
            "Salesforce/codegen-350M-mono",
            "microsoft/CodeGPT-small-py",
            "EleutherAI/gpt-neo-2.7B"
        ],
        "small_fast": [
            "microsoft/DialoGPT-medium",
            "google/flan-t5-base",
            "gpt2"
        ]
    }
    
    return recommendations.get(task, recommendations["chat"])

def check_local_model_requirements() -> Dict[str, bool]:
    """Check if requirements for local models are available"""
    requirements = {
        "transformers": False,
        "torch": False,
        "accelerate": False,
        "cuda": False
    }
    
    try:
        import transformers
        requirements["transformers"] = True
    except ImportError:
        pass
    
    try:
        import torch
        requirements["torch"] = True
        requirements["cuda"] = torch.cuda.is_available()
    except ImportError:
        pass
    
    try:
        import accelerate
        requirements["accelerate"] = True
    except ImportError:
        pass
    
    return requirements