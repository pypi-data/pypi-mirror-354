"""
Enhanced Exception Handling for AI Chat Manager

This module provides comprehensive exception classes with detailed error information,
recovery suggestions, and structured error data for better debugging and user experience.
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorSeverity(str, Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(str, Enum):
    """Error categories for classification"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    RATE_LIMIT = "rate_limit"
    MODEL = "model"
    VALIDATION = "validation"
    TIMEOUT = "timeout"
    QUOTA = "quota"
    SYSTEM = "system"
    USER_INPUT = "user_input"
    DATA = "data"
    PLUGIN = "plugin"

class AIChatManagerError(Exception):
    """
    Base exception for AI Chat Manager with enhanced error information
    
    This is the root exception class that provides structured error information,
    recovery suggestions, and detailed context for debugging.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        category: Optional[ErrorCategory] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None,
        original_error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.category = category or ErrorCategory.SYSTEM
        self.severity = severity
        self.details = details or {}
        self.suggestions = suggestions or []
        self.original_error = original_error
        self.context = context or {}
        self.timestamp = datetime.now()
        
        # Log the error
        self._log_error()
    
    def _log_error(self):
        """Log the error with appropriate level"""
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(self.severity, logging.ERROR)
        
        logger.log(
            log_level,
            f"{self.error_code}: {self.message}",
            extra={
                "error_code": self.error_code,
                "category": self.category.value,
                "severity": self.severity.value,
                "details": self.details,
                "context": self.context
            }
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "suggestions": self.suggestions,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "original_error": str(self.original_error) if self.original_error else None
        }
    
    def add_suggestion(self, suggestion: str):
        """Add a recovery suggestion"""
        self.suggestions.append(suggestion)
    
    def add_context(self, key: str, value: Any):
        """Add context information"""
        self.context[key] = value
    
    def is_recoverable(self) -> bool:
        """Check if this error is potentially recoverable"""
        return self.severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM]
    
    def should_retry(self) -> bool:
        """Check if operation should be retried"""
        return self.category in [
            ErrorCategory.NETWORK,
            ErrorCategory.TIMEOUT,
            ErrorCategory.RATE_LIMIT
        ]

class ConfigurationError(AIChatManagerError):
    """Configuration-related errors"""
    
    def __init__(
        self,
        message: str,
        config_path: Optional[str] = None,
        config_section: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.CONFIGURATION,
            **kwargs
        )
        
        if config_path:
            self.add_context("config_path", config_path)
        if config_section:
            self.add_context("config_section", config_section)
        
        # Add common suggestions
        self.add_suggestion("Check configuration file format and syntax")
        self.add_suggestion("Verify all required fields are present")
        self.add_suggestion("Run 'ai-chat-manager validate-config' to check configuration")

class BackendError(AIChatManagerError):
    """Backend-related errors"""
    
    def __init__(
        self,
        message: str,
        backend_name: Optional[str] = None,
        backend_type: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        
        if backend_name:
            self.add_context("backend_name", backend_name)
        if backend_type:
            self.add_context("backend_type", backend_type)

class AuthenticationError(BackendError):
    """Authentication failures with specific guidance"""
    
    def __init__(
        self,
        message: str,
        backend_name: Optional[str] = None,
        auth_method: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            backend_name=backend_name,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        
        if auth_method:
            self.add_context("auth_method", auth_method)
        
        # Add specific suggestions
        self.add_suggestion("Verify API key is correct and not expired")
        self.add_suggestion("Check if API key has required permissions")
        self.add_suggestion("Ensure environment variables are set correctly")
        if backend_name:
            self.add_suggestion(f"Check {backend_name} service status and documentation")

class AuthorizationError(BackendError):
    """Authorization/permission errors"""
    
    def __init__(
        self,
        message: str,
        required_permission: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        
        if required_permission:
            self.add_context("required_permission", required_permission)
        
        self.add_suggestion("Check API key permissions and scopes")
        self.add_suggestion("Verify account subscription and limits")

class RateLimitError(BackendError):
    """Rate limiting errors with retry information"""
    
    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        limit_type: Optional[str] = None,
        current_usage: Optional[int] = None,
        limit_value: Optional[int] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.RATE_LIMIT,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if retry_after:
            self.add_context("retry_after_seconds", retry_after)
        if limit_type:
            self.add_context("limit_type", limit_type)
        if current_usage is not None:
            self.add_context("current_usage", current_usage)
        if limit_value is not None:
            self.add_context("limit_value", limit_value)
        
        self.add_suggestion("Wait before retrying the request")
        self.add_suggestion("Consider reducing request frequency")
        self.add_suggestion("Implement exponential backoff in your code")
        if retry_after:
            self.add_suggestion(f"Retry after {retry_after} seconds")

class QuotaExceededError(BackendError):
    """Quota/billing limit exceeded"""
    
    def __init__(
        self,
        message: str,
        quota_type: Optional[str] = None,
        usage_amount: Optional[float] = None,
        quota_limit: Optional[float] = None,
        reset_date: Optional[datetime] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.QUOTA,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        
        if quota_type:
            self.add_context("quota_type", quota_type)
        if usage_amount is not None:
            self.add_context("usage_amount", usage_amount)
        if quota_limit is not None:
            self.add_context("quota_limit", quota_limit)
        if reset_date:
            self.add_context("reset_date", reset_date.isoformat())
        
        self.add_suggestion("Check your account usage and billing")
        self.add_suggestion("Consider upgrading your plan")
        if reset_date:
            self.add_suggestion(f"Quota resets on {reset_date.strftime('%Y-%m-%d')}")

class ModelNotFoundError(BackendError):
    """Model not found or not available"""
    
    def __init__(
        self,
        message: str,
        model_name: Optional[str] = None,
        available_models: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.MODEL,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        
        if model_name:
            self.add_context("requested_model", model_name)
        if available_models:
            self.add_context("available_models", available_models)
        
        self.add_suggestion("Check model name spelling and availability")
        self.add_suggestion("Verify your account has access to this model")
        if available_models:
            self.add_suggestion(f"Available models: {', '.join(available_models[:5])}")

class ModelCapabilityError(BackendError):
    """Model doesn't support requested capability"""
    
    def __init__(
        self,
        message: str,
        model_name: Optional[str] = None,
        requested_capability: Optional[str] = None,
        supported_capabilities: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.MODEL,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if model_name:
            self.add_context("model_name", model_name)
        if requested_capability:
            self.add_context("requested_capability", requested_capability)
        if supported_capabilities:
            self.add_context("supported_capabilities", supported_capabilities)
        
        self.add_suggestion("Use a different model that supports this capability")
        if supported_capabilities:
            self.add_suggestion(f"This model supports: {', '.join(supported_capabilities)}")

class NetworkError(BackendError):
    """Network connectivity errors"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if status_code:
            self.add_context("status_code", status_code)
        if endpoint:
            self.add_context("endpoint", endpoint)
        
        self.add_suggestion("Check internet connectivity")
        self.add_suggestion("Verify service endpoint URL")
        self.add_suggestion("Check if service is experiencing downtime")

class TimeoutError(BackendError):
    """Request timeout errors"""
    
    def __init__(
        self,
        message: str,
        timeout_duration: Optional[float] = None,
        operation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.TIMEOUT,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if timeout_duration:
            self.add_context("timeout_duration", timeout_duration)
        if operation:
            self.add_context("operation", operation)
        
        self.add_suggestion("Increase timeout duration")
        self.add_suggestion("Check network stability")
        self.add_suggestion("Try reducing request complexity")

class BotNotFoundError(AIChatManagerError):
    """Bot not found error"""
    
    def __init__(
        self,
        message: str,
        bot_name: Optional[str] = None,
        available_bots: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if bot_name:
            self.add_context("bot_name", bot_name)
        if available_bots:
            self.add_context("available_bots", available_bots)
        
        self.add_suggestion("Check bot name spelling")
        self.add_suggestion("Run 'ai-chat-manager bot list' to see available bots")
        if available_bots:
            self.add_suggestion(f"Available bots: {', '.join(available_bots)}")

class ValidationError(AIChatManagerError):
    """Data validation errors"""
    
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None,
        validation_rule: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if field_name:
            self.add_context("field_name", field_name)
        if field_value is not None:
            self.add_context("field_value", str(field_value))
        if validation_rule:
            self.add_context("validation_rule", validation_rule)
        
        self.add_suggestion("Check input data format and types")
        self.add_suggestion("Refer to documentation for valid values")

class ConversationError(AIChatManagerError):
    """Conversation management errors"""
    
    def __init__(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.DATA,
            **kwargs
        )
        
        if conversation_id:
            self.add_context("conversation_id", conversation_id)

class MemoryError(AIChatManagerError):
    """Memory/storage related errors"""
    
    def __init__(
        self,
        message: str,
        memory_type: Optional[str] = None,
        storage_path: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.SYSTEM,
            **kwargs
        )
        
        if memory_type:
            self.add_context("memory_type", memory_type)
        if storage_path:
            self.add_context("storage_path", storage_path)
        
        self.add_suggestion("Check available disk space")
        self.add_suggestion("Verify write permissions")
        self.add_suggestion("Consider clearing old conversation data")

class PluginError(AIChatManagerError):
    """Plugin-related errors"""
    
    def __init__(
        self,
        message: str,
        plugin_name: Optional[str] = None,
        plugin_version: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.PLUGIN,
            **kwargs
        )
        
        if plugin_name:
            self.add_context("plugin_name", plugin_name)
        if plugin_version:
            self.add_context("plugin_version", plugin_version)
        
        self.add_suggestion("Check plugin compatibility")
        self.add_suggestion("Verify plugin installation")
        self.add_suggestion("Check plugin documentation")

class ContentFilterError(AIChatManagerError):
    """Content filtering/safety errors"""
    
    def __init__(
        self,
        message: str,
        content_type: Optional[str] = None,
        filter_reason: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        
        if content_type:
            self.add_context("content_type", content_type)
        if filter_reason:
            self.add_context("filter_reason", filter_reason)
        
        self.add_suggestion("Review content for policy violations")
        self.add_suggestion("Consider rephrasing the input")
        self.add_suggestion("Check content filtering settings")

# Utility functions for error handling

def create_error_from_response(
    response_data: Dict[str, Any],
    backend_name: Optional[str] = None
) -> AIChatManagerError:
    """Create appropriate error from API response"""
    
    error_message = response_data.get("error", {}).get("message", "Unknown error")
    error_type = response_data.get("error", {}).get("type", "")
    status_code = response_data.get("status_code")
    
    # Map common error types to specific exceptions
    if status_code == 401 or "auth" in error_type.lower():
        return AuthenticationError(
            error_message,
            backend_name=backend_name,
            details=response_data
        )
    elif status_code == 403:
        return AuthorizationError(
            error_message,
            backend_name=backend_name,
            details=response_data
        )
    elif status_code == 429 or "rate" in error_type.lower():
        retry_after = response_data.get("retry_after")
        return RateLimitError(
            error_message,
            backend_name=backend_name,
            retry_after=retry_after,
            details=response_data
        )
    elif status_code == 404 or "not_found" in error_type.lower():
        return ModelNotFoundError(
            error_message,
            backend_name=backend_name,
            details=response_data
        )
    elif status_code and 500 <= status_code < 600:
        return NetworkError(
            error_message,
            backend_name=backend_name,
            status_code=status_code,
            details=response_data
        )
    else:
        return BackendError(
            error_message,
            backend_name=backend_name,
            details=response_data
        )

def handle_exception(
    func
):
    """Decorator to handle and convert exceptions to AI Chat Manager exceptions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AIChatManagerError:
            # Re-raise our own exceptions
            raise
        except Exception as e:
            # Convert other exceptions
            raise AIChatManagerError(
                f"Unexpected error in {func.__name__}: {str(e)}",
                original_error=e,
                severity=ErrorSeverity.HIGH
            )
    return wrapper

async def handle_async_exception(
    func
):
    """Async decorator to handle and convert exceptions"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AIChatManagerError:
            raise
        except Exception as e:
            raise AIChatManagerError(
                f"Unexpected error in {func.__name__}: {str(e)}",
                original_error=e,
                severity=ErrorSeverity.HIGH
            )
    return wrapper

# Exception registry for serialization/deserialization
EXCEPTION_REGISTRY = {
    "AIChatManagerError": AIChatManagerError,
    "ConfigurationError": ConfigurationError,
    "BackendError": BackendError,
    "AuthenticationError": AuthenticationError,
    "AuthorizationError": AuthorizationError,
    "RateLimitError": RateLimitError,
    "QuotaExceededError": QuotaExceededError,
    "ModelNotFoundError": ModelNotFoundError,
    "ModelCapabilityError": ModelCapabilityError,
    "NetworkError": NetworkError,
    "TimeoutError": TimeoutError,
    "BotNotFoundError": BotNotFoundError,
    "ValidationError": ValidationError,
    "ConversationError": ConversationError,
    "MemoryError": MemoryError,
    "PluginError": PluginError,
    "ContentFilterError": ContentFilterError,
}

def exception_from_dict(data: Dict[str, Any]) -> AIChatManagerError:
    """Recreate exception from dictionary"""
    error_class = EXCEPTION_REGISTRY.get(data.get("error_code", "AIChatManagerError"))
    if not error_class:
        error_class = AIChatManagerError
    
    return error_class(
        message=data.get("message", ""),
        error_code=data.get("error_code"),
        category=ErrorCategory(data.get("category", "system")),
        severity=ErrorSeverity(data.get("severity", "medium")),
        details=data.get("details", {}),
        suggestions=data.get("suggestions", []),
        context=data.get("context", {})
    )