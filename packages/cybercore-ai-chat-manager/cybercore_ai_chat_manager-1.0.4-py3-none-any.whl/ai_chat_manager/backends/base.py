"""
Base Backend Interface for AI Chat Manager

This module provides the abstract base class and common functionality for all AI backends.
It includes rate limiting, retry logic, response validation, and standardized error handling.
"""

import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator, Union, Callable
from datetime import datetime, timedelta
import json
import time
from dataclasses import dataclass
import hashlib

from asyncio_throttle import Throttler
import backoff

from ..core.types import (
    Message, ChatResponse, StreamingChunk, Usage, 
    FinishReason, FunctionCall, MessageRole
)
from ..core.config import BackendConfig, RetryConfig
from ..core.exceptions import (
    BackendError, AuthenticationError, RateLimitError, 
    NetworkError, TimeoutError, ModelNotFoundError,
    QuotaExceededError, create_error_from_response
)

logger = logging.getLogger(__name__)

@dataclass
class RequestMetrics:
    """Request performance metrics"""
    request_id: str
    backend_name: str
    model: str
    start_time: datetime
    end_time: Optional[datetime] = None
    response_time: Optional[float] = None
    tokens_used: Optional[int] = None
    success: bool = False
    error: Optional[str] = None
    retry_count: int = 0

class RateLimiter:
    """Advanced rate limiter with burst handling and backoff"""
    
    def __init__(self, rate_limit_config):
        self.requests_per_minute = rate_limit_config.requests_per_minute
        self.requests_per_hour = rate_limit_config.requests_per_hour
        self.requests_per_day = rate_limit_config.requests_per_day
        self.burst_limit = rate_limit_config.burst_limit
        self.cooldown_period = rate_limit_config.cooldown_period
        
        # Tracking
        self.minute_requests = []
        self.hour_requests = []
        self.day_requests = []
        self.burst_requests = []
        self.last_cooldown = None
        
        # Throttler for basic rate limiting
        self.throttler = Throttler(rate_limit=self.requests_per_minute, period=60)
    
    async def acquire(self):
        """Acquire permission to make a request"""
        now = datetime.now()
        
        # Clean old requests
        self._cleanup_old_requests(now)
        
        # Check cooldown
        if self.last_cooldown and (now - self.last_cooldown).seconds < self.cooldown_period:
            wait_time = self.cooldown_period - (now - self.last_cooldown).seconds
            await asyncio.sleep(wait_time)
        
        # Check daily limit
        if len(self.day_requests) >= self.requests_per_day:
            raise RateLimitError(
                "Daily request limit exceeded",
                limit_type="daily",
                current_usage=len(self.day_requests),
                limit_value=self.requests_per_day
            )
        
        # Check hourly limit
        if len(self.hour_requests) >= self.requests_per_hour:
            raise RateLimitError(
                "Hourly request limit exceeded",
                limit_type="hourly",
                current_usage=len(self.hour_requests),
                limit_value=self.requests_per_hour
            )
        
        # Check burst limit
        if len(self.burst_requests) >= self.burst_limit:
            # Wait for burst window to clear
            oldest_burst = min(self.burst_requests)
            wait_time = 60 - (now - oldest_burst).seconds
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Use throttler for minute-level limiting
        async with self.throttler:
            # Record request
            self.minute_requests.append(now)
            self.hour_requests.append(now)
            self.day_requests.append(now)
            self.burst_requests.append(now)
    
    def _cleanup_old_requests(self, now: datetime):
        """Remove old request records"""
        # Minute window
        cutoff = now - timedelta(minutes=1)
        self.minute_requests = [t for t in self.minute_requests if t > cutoff]
        self.burst_requests = [t for t in self.burst_requests if t > cutoff]
        
        # Hour window
        cutoff = now - timedelta(hours=1)
        self.hour_requests = [t for t in self.hour_requests if t > cutoff]
        
        # Day window
        cutoff = now - timedelta(days=1)
        self.day_requests = [t for t in self.day_requests if t > cutoff]
    
    def record_error(self):
        """Record an error for cooldown purposes"""
        self.last_cooldown = datetime.now()

class ResponseValidator:
    """Validates and sanitizes backend responses"""
    
    @staticmethod
    def validate_chat_response(response_data: Dict[str, Any], backend_name: str) -> ChatResponse:
        """Validate and convert response data to ChatResponse"""
        try:
            # Extract basic fields
            content = ResponseValidator._extract_content(response_data)
            model = response_data.get("model", "unknown")
            finish_reason = ResponseValidator._extract_finish_reason(response_data)
            
            # Extract usage information
            usage = ResponseValidator._extract_usage(response_data)
            
            # Extract function calls
            function_calls = ResponseValidator._extract_function_calls(response_data)
            
            # Calculate response time if available
            response_time = response_data.get("processing_time")
            
            return ChatResponse(
                content=content,
                model=model,
                backend=backend_name,
                finish_reason=finish_reason,
                usage=usage,
                function_calls=function_calls,
                response_time=response_time,
                raw_response=response_data
            )
            
        except Exception as e:
            logger.error(f"Failed to validate response from {backend_name}: {e}")
            raise BackendError(f"Invalid response format: {e}", backend_name=backend_name)
    
    @staticmethod
    def _extract_content(response_data: Dict[str, Any]) -> str:
        """Extract content from response"""
        # Try different common response formats
        if "choices" in response_data and response_data["choices"]:
            choice = response_data["choices"][0]
            if "message" in choice:
                return choice["message"].get("content", "")
            elif "text" in choice:
                return choice["text"]
        
        if "content" in response_data:
            return response_data["content"]
        
        if "text" in response_data:
            return response_data["text"]
        
        if "generated_text" in response_data:
            return response_data["generated_text"]
        
        # For list responses (some HuggingFace models)
        if isinstance(response_data, list) and response_data:
            first_item = response_data[0]
            if isinstance(first_item, dict):
                return first_item.get("generated_text", str(first_item))
            return str(first_item)
        
        logger.warning(f"Could not extract content from response: {response_data}")
        return ""
    
    @staticmethod
    def _extract_finish_reason(response_data: Dict[str, Any]) -> Optional[FinishReason]:
        """Extract finish reason"""
        if "choices" in response_data and response_data["choices"]:
            finish_reason = response_data["choices"][0].get("finish_reason")
            if finish_reason:
                try:
                    return FinishReason(finish_reason)
                except ValueError:
                    return FinishReason.STOP
        return FinishReason.STOP
    
    @staticmethod
    def _extract_usage(response_data: Dict[str, Any]) -> Optional[Usage]:
        """Extract token usage information"""
        usage_data = response_data.get("usage")
        if usage_data:
            return Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            )
        return None
    
    @staticmethod
    def _extract_function_calls(response_data: Dict[str, Any]) -> List[FunctionCall]:
        """Extract function calls from response"""
        function_calls = []
        
        if "choices" in response_data and response_data["choices"]:
            choice = response_data["choices"][0]
            message = choice.get("message", {})
            
            # OpenAI-style function calls
            if "function_call" in message:
                fc = message["function_call"]
                function_calls.append(FunctionCall(
                    name=fc.get("name", ""),
                    arguments=json.loads(fc.get("arguments", "{}"))
                ))
            
            # Tool calls format
            if "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    if tool_call.get("type") == "function":
                        function = tool_call.get("function", {})
                        function_calls.append(FunctionCall(
                            name=function.get("name", ""),
                            arguments=json.loads(function.get("arguments", "{}")),
                            call_id=tool_call.get("id")
                        ))
        
        return function_calls

class BaseBackend(ABC):
    """
    Abstract base class for AI backends
    
    This class provides common functionality including:
    - Rate limiting and throttling
    - Retry logic with exponential backoff
    - Request/response validation
    - Error handling and conversion
    - Performance monitoring
    - Session management
    """
    
    def __init__(self, config: BackendConfig):
        self.config = config
        self.name = config.name
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.session: Optional[aiohttp.ClientSession] = None
        self.metrics: List[RequestMetrics] = []
        
        # Validation
        self.validator = ResponseValidator()
        
        # Performance tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        
        logger.info(f"Initialized backend: {self.name} ({config.backend_type})")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_session(self):
        """Ensure HTTP session is created"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers=self._get_default_headers(),
                connector=aiohttp.TCPConnector(limit=100, limit_per_host=30)
            )
    
    async def close(self):
        """Close the backend and cleanup resources"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for requests"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"AI-Chat-Manager/{self.name}/1.0",
            "Accept": "application/json"
        }
        
        # Add authentication headers
        auth_headers = self._get_auth_headers()
        headers.update(auth_headers)
        
        return headers
    
    @abstractmethod
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers (implemented by subclasses)"""
        pass
    
    @abstractmethod
    def _prepare_messages(self, messages: List[Message]) -> Union[List[Dict[str, Any]], str]:
        """Convert internal message format to backend-specific format"""
        pass
    
    @abstractmethod
    def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
        """Build request data for the specific backend"""
        pass
    
    @abstractmethod
    async def chat_completion(self, messages: List[Message], **kwargs) -> ChatResponse:
        """Generate chat completion (main method)"""
        pass
    
    async def stream_completion(
        self, 
        messages: List[Message], 
        **kwargs
    ) -> AsyncGenerator[StreamingChunk, None]:
        """Generate streaming chat completion (optional)"""
        # Default implementation: convert regular response to single chunk
        response = await self.chat_completion(messages, **kwargs)
        yield StreamingChunk(
            content=response.content,
            finish_reason=response.finish_reason,
            is_final=True,
            metadata={"converted_from_regular": True}
        )
    
    @backoff.on_exception(
        backoff.expo,
        (NetworkError, TimeoutError, RateLimitError),
        max_tries=3,
        max_time=300
    )
    async def _make_request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], aiohttp.ClientResponse]:
        """
        Make HTTP request with comprehensive error handling and retry logic
        """
        request_id = self._generate_request_id()
        metrics = RequestMetrics(
            request_id=request_id,
            backend_name=self.name,
            model=data.get("model", "unknown") if data else "unknown",
            start_time=datetime.now()
        )
        
        try:
            # Rate limiting
            await self.rate_limiter.acquire()
            
            # Ensure session
            await self._ensure_session()
            
            # Prepare request
            request_kwargs = {
                "method": method,
                "url": url,
                "headers": kwargs.get("headers", {}),
                **kwargs
            }
            
            if data:
                request_kwargs["json"] = data
            
            # Log request
            if self.config.log_requests:
                logger.debug(f"Request {request_id}: {method} {url}")
                if data and self.config.log_requests:
                    # Log without sensitive data
                    safe_data = self._sanitize_log_data(data)
                    logger.debug(f"Request data: {safe_data}")
            
            # Make request
            async with self.session.request(**request_kwargs) as response:
                metrics.response_time = (datetime.now() - metrics.start_time).total_seconds()
                
                # Handle streaming responses
                if stream:
                    return response
                
                # Handle errors
                if response.status >= 400:
                    error_text = await response.text()
                    error_data = {"status_code": response.status, "error": error_text}
                    
                    try:
                        error_json = json.loads(error_text)
                        error_data.update(error_json)
                    except json.JSONDecodeError:
                        pass
                    
                    # Record error
                    metrics.error = error_text
                    self.rate_limiter.record_error()
                    
                    # Raise specific exception
                    raise create_error_from_response(error_data, self.name)
                
                # Parse response
                response_data = await response.json()
                
                # Log response
                if self.config.log_responses:
                    logger.debug(f"Response {request_id}: {response.status}")
                
                metrics.success = True
                return response_data
                
        except aiohttp.ClientTimeout:
            metrics.error = "Request timeout"
            raise TimeoutError(
                f"Request timeout after {self.config.timeout}s",
                timeout_duration=self.config.timeout,
                backend_name=self.name
            )
            
        except aiohttp.ClientError as e:
            metrics.error = str(e)
            raise NetworkError(
                f"Network error: {e}",
                backend_name=self.name
            )
            
        except Exception as e:
            metrics.error = str(e)
            logger.error(f"Unexpected error in request {request_id}: {e}")
            raise BackendError(
                f"Request failed: {e}",
                backend_name=self.name,
                details={"request_id": request_id}
            )
            
        finally:
            # Record metrics
            metrics.end_time = datetime.now()
            if metrics.response_time is None:
                metrics.response_time = (metrics.end_time - metrics.start_time).total_seconds()
            
            self.metrics.append(metrics)
            self._update_performance_stats(metrics)
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        timestamp = str(time.time())
        backend_hash = hashlib.md5(self.name.encode()).hexdigest()[:8]
        return f"{self.name}_{backend_hash}_{timestamp}"
    
    def _sanitize_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive data from logs"""
        sanitized = data.copy()
        
        # Remove or mask sensitive fields
        sensitive_fields = ["api_key", "authorization", "token", "key"]
        
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = "[REDACTED]"
        
        # Truncate long messages for readability
        if "messages" in sanitized:
            sanitized["messages"] = str(sanitized["messages"])[:200] + "..."
        
        return sanitized
    
    def _update_performance_stats(self, metrics: RequestMetrics):
        """Update backend performance statistics"""
        self.total_requests += 1
        
        if metrics.success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        if metrics.response_time:
            self.total_response_time += metrics.response_time
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get backend performance statistics"""
        return {
            "backend_name": self.name,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            "average_response_time": self.total_response_time / self.successful_requests if self.successful_requests > 0 else 0,
            "recent_errors": [
                {"error": m.error, "time": m.start_time.isoformat()}
                for m in self.metrics[-10:] if not m.success
            ]
        }
    
    def health_check(self) -> bool:
        """Basic health check"""
        try:
            # Check if we can create a session
            if not self.session or self.session.closed:
                return True  # Will be created when needed
            
            # Check recent success rate
            recent_metrics = self.metrics[-20:] if len(self.metrics) > 20 else self.metrics
            if recent_metrics:
                recent_success_rate = sum(1 for m in recent_metrics if m.success) / len(recent_metrics)
                return recent_success_rate > 0.5
            
            return True
            
        except Exception as e:
            logger.warning(f"Health check failed for {self.name}: {e}")
            return False
    
    def supports_streaming(self) -> bool:
        """Check if backend supports streaming"""
        return self.config.supports_streaming
    
    def supports_functions(self) -> bool:
        """Check if backend supports function calling"""
        return self.config.supports_functions
    
    def supports_vision(self) -> bool:
        """Check if backend supports vision/image inputs"""
        return self.config.supports_vision
    
    def supports_audio(self) -> bool:
        """Check if backend supports audio"""
        return self.config.supports_audio
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "name": self.config.model,
            "backend": self.name,
            "max_tokens": self.config.max_tokens,
            "supports_streaming": self.supports_streaming(),
            "supports_functions": self.supports_functions(),
            "supports_vision": self.supports_vision(),
            "supports_audio": self.supports_audio(),
        }
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token)"""
        return len(text) // 4
    
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost for request (override in subclasses with actual pricing)"""
        # Very rough estimate - actual costs vary significantly by model and provider
        prompt_cost = prompt_tokens * 0.00001  # $0.01 per 1K tokens
        completion_cost = completion_tokens * 0.00002  # $0.02 per 1K tokens
        return prompt_cost + completion_cost
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, model={self.config.model})"
    
    def __repr__(self) -> str:
        return self.__str__()

# Utility functions for backend management

def validate_backend_config(config: BackendConfig) -> List[str]:
    """Validate backend configuration and return list of issues"""
    issues = []
    
    # Check required fields
    if not config.name:
        issues.append("Backend name is required")
    
    if not config.backend_type:
        issues.append("Backend type is required")
    
    # Check API key
    api_key = config.get_api_key()
    if not api_key:
        issues.append("API key is required (either direct or via environment variable)")
    
    # Check URL format
    if config.base_url and not (config.base_url.startswith('http://') or config.base_url.startswith('https://')):
        issues.append("base_url must start with http:// or https://")
    
    # Check numeric ranges
    if config.max_tokens <= 0:
        issues.append("max_tokens must be positive")
    
    if not 0 <= config.temperature <= 2:
        issues.append("temperature must be between 0 and 2")
    
    if not 0 <= config.top_p <= 1:
        issues.append("top_p must be between 0 and 1")
    
    if config.timeout <= 0:
        issues.append("timeout must be positive")
    
    return issues

async def test_backend_connection(backend: BaseBackend) -> Dict[str, Any]:
    """Test backend connection and return results"""
    test_result = {
        "backend_name": backend.name,
        "success": False,
        "response_time": None,
        "error": None,
        "model_info": None
    }
    
    try:
        start_time = datetime.now()
        
        # Simple test message
        test_messages = [Message(
            role=MessageRole.USER,
            content="Hello, this is a connection test."
        )]
        
        # Test chat completion
        response = await backend.chat_completion(test_messages, max_tokens=10)
        
        end_time = datetime.now()
        test_result.update({
            "success": True,
            "response_time": (end_time - start_time).total_seconds(),
            "model_info": backend.get_model_info(),
            "response_content": response.content[:50] + "..." if len(response.content) > 50 else response.content
        })
        
    except Exception as e:
        test_result["error"] = str(e)
        logger.error(f"Backend connection test failed for {backend.name}: {e}")
    
    return test_result