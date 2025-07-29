"""
Enhanced Configuration Management for AI Chat Manager

This module provides secure, validated configuration management with encryption,
environment variable support, and comprehensive validation.
"""

import os
import yaml
import json
import logging
import secrets
from typing import Dict, Any, Optional, List, Union, Type, Callable
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel, Field, validator, SecretStr
from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)

class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class BackendType(str, Enum):
    """Supported backend types"""
    OPENAI = "openai"
    VENICE = "venice"
    HUGGINGFACE = "huggingface"
    ELEVENLABS = "elevenlabs"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    LOCAL = "local"
    CUSTOM = "custom"

@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_limit: int = 10
    cooldown_period: int = 60  # seconds

@dataclass
class RetryConfig:
    """Retry configuration for failed requests"""
    max_retries: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

class BackendConfig(BaseModel):
    """Configuration for AI backend with enhanced validation"""
    
    name: str = Field(..., description="Backend name")
    backend_type: BackendType = Field(..., description="Backend type")
    api_key: Optional[SecretStr] = Field(None, description="API key (encrypted)")
    api_key_env: Optional[str] = Field(None, description="Environment variable for API key")
    base_url: Optional[str] = Field(None, description="Custom base URL")
    model: Optional[str] = Field(None, description="Default model to use")
    max_tokens: int = Field(default=1000, ge=1, le=100000, description="Maximum tokens per request")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    top_p: float = Field(default=1.0, ge=0, le=1, description="Top-p sampling")
    frequency_penalty: float = Field(default=0.0, ge=-2, le=2, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, ge=-2, le=2, description="Presence penalty")
    enabled: bool = Field(default=True, description="Whether backend is enabled")
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    timeout: float = Field(default=30.0, ge=1, le=300, description="Request timeout in seconds")
    custom_params: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters")
    
    # Advanced settings
    supports_streaming: bool = Field(default=False, description="Supports streaming responses")
    supports_functions: bool = Field(default=False, description="Supports function calling")
    supports_vision: bool = Field(default=False, description="Supports vision/image inputs")
    supports_audio: bool = Field(default=False, description="Supports audio inputs/outputs")
    
    # Monitoring and logging
    log_requests: bool = Field(default=False, description="Log all requests")
    log_responses: bool = Field(default=False, description="Log all responses")
    collect_metrics: bool = Field(default=True, description="Collect performance metrics")
    
    @validator('api_key_env')
    def validate_api_key_source(cls, v, values):
        """Ensure either api_key or api_key_env is provided"""
        if not v and not values.get('api_key'):
            raise ValueError("Either api_key or api_key_env must be provided")
        return v
    
    @validator('base_url')
    def validate_base_url(cls, v):
        """Validate base URL format"""
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("base_url must start with http:// or https://")
        return v
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from direct value or environment variable"""
        if self.api_key:
            return self.api_key.get_secret_value()
        elif self.api_key_env:
            return os.getenv(self.api_key_env)
        return None

class BotPersonality(str, Enum):
    """Predefined bot personalities"""
    HELPFUL = "helpful"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    EMPATHETIC = "empathetic"
    CONCISE = "concise"
    DETAILED = "detailed"
    CUSTOM = "custom"

class BotConfig(BaseModel):
    """Configuration for a bot instance with enhanced features"""
    
    name: str = Field(..., description="Bot name")
    backend: str = Field(..., description="Backend to use")
    system_prompt: str = Field(default="", description="System prompt")
    personality: BotPersonality = Field(default=BotPersonality.HELPFUL, description="Bot personality")
    
    # Memory and context settings
    memory_enabled: bool = Field(default=True, description="Enable conversation memory")
    max_context_length: int = Field(default=4000, ge=100, le=100000, description="Maximum context length")
    context_compression: bool = Field(default=False, description="Enable context compression")
    memory_decay: bool = Field(default=False, description="Enable memory decay over time")
    memory_decay_days: int = Field(default=30, ge=1, description="Days before memory starts decaying")
    
    # Learning and adaptation
    learning_enabled: bool = Field(default=False, description="Enable learning from interactions")
    personalization_enabled: bool = Field(default=False, description="Enable user personalization")
    feedback_learning: bool = Field(default=False, description="Learn from user feedback")
    
    # Response settings
    max_response_length: int = Field(default=1000, ge=10, le=10000, description="Maximum response length")
    response_style: str = Field(default="balanced", description="Response style (concise/balanced/detailed)")
    language: str = Field(default="en", description="Primary language")
    
    # Safety and moderation
    content_filter_enabled: bool = Field(default=True, description="Enable content filtering")
    safety_level: str = Field(default="medium", description="Safety level (low/medium/high)")
    allowed_topics: List[str] = Field(default_factory=list, description="Allowed topics (empty = all)")
    blocked_topics: List[str] = Field(default_factory=list, description="Blocked topics")
    
    # Advanced features
    function_calling_enabled: bool = Field(default=False, description="Enable function calling")
    available_functions: List[str] = Field(default_factory=list, description="Available functions")
    web_search_enabled: bool = Field(default=False, description="Enable web search")
    file_access_enabled: bool = Field(default=False, description="Enable file access")
    
    # Metadata and tracking
    tags: List[str] = Field(default_factory=list, description="Bot tags for organization")
    description: str = Field(default="", description="Bot description")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Custom settings")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate bot name"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Bot name cannot be empty")
        if len(v) > 50:
            raise ValueError("Bot name must be 50 characters or less")
        return v.strip()

class GlobalConfig(BaseModel):
    """Global configuration settings"""
    
    # Logging configuration
    log_level: LogLevel = Field(default=LogLevel.INFO)
    log_file: Optional[str] = Field(None, description="Log file path")
    log_rotation: bool = Field(default=True, description="Enable log rotation")
    log_max_size: str = Field(default="100MB", description="Maximum log file size")
    log_backup_count: int = Field(default=5, description="Number of backup log files")
    
    # Performance settings
    max_concurrent_requests: int = Field(default=10, ge=1, le=100)
    default_timeout: float = Field(default=30.0, ge=1, le=300)
    request_pool_size: int = Field(default=20, ge=1, le=100)
    
    # Storage settings
    data_directory: str = Field(default="./data", description="Data storage directory")
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_interval_hours: int = Field(default=24, ge=1, description="Backup interval in hours")
    backup_retention_days: int = Field(default=30, ge=1, description="Backup retention in days")
    
    # Security settings
    encryption_enabled: bool = Field(default=True, description="Enable data encryption")
    api_key_encryption: bool = Field(default=True, description="Encrypt API keys")
    audit_logging: bool = Field(default=False, description="Enable audit logging")
    session_timeout_minutes: int = Field(default=60, ge=5, description="Session timeout")
    
    # Monitoring and metrics
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    metrics_endpoint: Optional[str] = Field(None, description="Metrics endpoint URL")
    health_check_enabled: bool = Field(default=True, description="Enable health checks")
    health_check_interval: int = Field(default=300, ge=30, description="Health check interval in seconds")
    
    # Development settings
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    development_mode: bool = Field(default=False, description="Enable development features")
    auto_reload: bool = Field(default=False, description="Auto-reload on config changes")

class ConfigEncryption:
    """Handles encryption and decryption of sensitive configuration data"""
    
    def __init__(self, password: Optional[str] = None):
        self.password = password or self._get_default_password()
        self.salt = self._get_or_create_salt()
        self.key = self._derive_key(self.password, self.salt)
        self.cipher = Fernet(self.key)
    
    def _get_default_password(self) -> str:
        """Get default encryption password from environment or generate one"""
        password = os.getenv('AI_CHAT_MANAGER_KEY')
        if not password:
            # Generate a random password and warn user
            password = secrets.token_urlsafe(32)
            logger.warning(
                "No AI_CHAT_MANAGER_KEY environment variable found. "
                f"Generated temporary key: {password[:8]}... "
                "Set AI_CHAT_MANAGER_KEY environment variable for persistent encryption."
            )
        return password
    
    def _get_or_create_salt(self) -> bytes:
        """Get or create a random salt for this installation"""
        salt_file = Path.home() / '.ai_chat_manager' / 'salt'
        
        if salt_file.exists():
            try:
                with open(salt_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Could not read salt file: {e}, generating new salt")
        
        # Generate new random salt
        salt = secrets.token_bytes(32)
        
        # Save salt securely
        try:
            salt_file.parent.mkdir(parents=True, exist_ok=True)
            with open(salt_file, 'wb') as f:
                f.write(salt)
            # Set secure permissions (Unix-like systems)
            if hasattr(os, 'chmod'):
                salt_file.chmod(0o600)
        except Exception as e:
            logger.error(f"Could not save salt file: {e}")
        
        return salt
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # Increased iterations for better security
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise ValueError("Failed to encrypt data")
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise ValueError("Failed to decrypt data - invalid key or corrupted data")

class Config:
    """Enhanced configuration manager with validation, encryption, and monitoring"""
    
    def __init__(self, config_path: str = "config.yaml", encryption_password: Optional[str] = None):
        self.config_path = Path(config_path)
        self.encryption = ConfigEncryption(encryption_password)
        self._config_data = {}
        self._watchers = []  # Config change watchers
        self._last_modified = None
        
        # Initialize logging
        self._setup_logging()
        
        # Load configuration
        self.load_config()
        
        # Setup file watching if enabled
        global_config = self.get_global_config()
        if global_config.auto_reload:
            self._setup_file_watcher()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _setup_file_watcher(self):
        """Setup file watcher for auto-reload"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class ConfigHandler(FileSystemEventHandler):
                def __init__(self, config_instance):
                    self.config = config_instance
                
                def on_modified(self, event):
                    if event.src_path == str(self.config.config_path):
                        self.config.reload_config()
            
            self.observer = Observer()
            handler = ConfigHandler(self)
            self.observer.schedule(handler, str(self.config_path.parent), recursive=False)
            self.observer.start()
            self.logger.info("File watcher enabled for config auto-reload")
            
        except ImportError:
            self.logger.warning("Watchdog not installed - auto-reload disabled")
    
    def add_change_watcher(self, callback: Callable[[Dict[str, Any]], None]):
        """Add a callback for configuration changes"""
        self._watchers.append(callback)
    
    def _notify_watchers(self):
        """Notify all watchers of configuration changes"""
        for watcher in self._watchers:
            try:
                watcher(self._config_data)
            except Exception as e:
                self.logger.error(f"Error in config watcher: {e}")
    
    def load_config(self):
        """Load configuration from file with validation"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = yaml.safe_load(f) or {}
                
                # Validate configuration structure
                self._validate_config_structure(data)
                self._config_data = data
                self._last_modified = self.config_path.stat().st_mtime
                
                self.logger.info(f"Configuration loaded from {self.config_path}")
                
            except yaml.YAMLError as e:
                self.logger.error(f"Invalid YAML in config file: {e}")
                raise ValueError(f"Invalid YAML in config file: {e}")
            except Exception as e:
                self.logger.error(f"Failed to load config: {e}")
                raise
        else:
            self.logger.info("Config file not found, creating default configuration")
            self._config_data = self._get_default_config()
            self.save_config()
    
    def reload_config(self):
        """Reload configuration if file has changed"""
        if not self.config_path.exists():
            return
        
        current_mtime = self.config_path.stat().st_mtime
        if self._last_modified is None or current_mtime > self._last_modified:
            old_data = self._config_data.copy()
            self.load_config()
            
            if old_data != self._config_data:
                self.logger.info("Configuration reloaded due to file changes")
                self._notify_watchers()
    
    def _validate_config_structure(self, data: Dict[str, Any]):
        """Validate configuration structure"""
        required_sections = ["backends", "bots", "global"]
        for section in required_sections:
            if section not in data:
                data[section] = {}
        
        # Validate each backend config
        for name, backend_data in data.get("backends", {}).items():
            try:
                BackendConfig(**backend_data)
            except Exception as e:
                self.logger.warning(f"Invalid backend config for {name}: {e}")
        
        # Validate each bot config
        for name, bot_data in data.get("bots", {}).items():
            try:
                BotConfig(**bot_data)
            except Exception as e:
                self.logger.warning(f"Invalid bot config for {name}: {e}")
        
        # Validate global config
        try:
            GlobalConfig(**data.get("global", {}))
        except Exception as e:
            self.logger.warning(f"Invalid global config: {e}")
    
    def save_config(self):
        """Save configuration to file with backup"""
        try:
            # Create backup if file exists
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.yaml.backup')
                import shutil
                shutil.copy2(self.config_path, backup_path)
            
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save configuration
            with open(self.config_path, 'w') as f:
                yaml.dump(self._config_data, f, default_flow_style=False, indent=2, sort_keys=True)
            
            # Update file permissions for security
            self.config_path.chmod(0o600)
            self._last_modified = self.config_path.stat().st_mtime
            
            self.logger.info(f"Configuration saved to {self.config_path}")
            self._notify_watchers()
            
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            raise
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration with all supported backends"""
        return {
            "backends": {
                "openai": {
                    "name": "openai",
                    "backend_type": "openai",
                    "api_key_env": "OPENAI_API_KEY",
                    "base_url": "https://api.openai.com/v1",
                    "model": "gpt-3.5-turbo",
                    "enabled": False,
                    "supports_streaming": True,
                    "supports_functions": True
                },
                "venice": {
                    "name": "venice",
                    "backend_type": "venice",
                    "api_key_env": "VENICE_API_KEY",
                    "base_url": "https://api.venice.ai/v1",
                    "model": "venice-base",
                    "enabled": False
                },
                "anthropic": {
                    "name": "anthropic",
                    "backend_type": "anthropic",
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "base_url": "https://api.anthropic.com",
                    "model": "claude-3-sonnet",
                    "enabled": False,
                    "supports_streaming": True
                },
                "huggingface": {
                    "name": "huggingface",
                    "backend_type": "huggingface",
                    "api_key_env": "HUGGINGFACE_API_KEY",
                    "base_url": "https://api-inference.huggingface.co",
                    "model": "microsoft/DialoGPT-large",
                    "enabled": False
                },
                "elevenlabs": {
                    "name": "elevenlabs",
                    "backend_type": "elevenlabs",
                    "api_key_env": "ELEVENLABS_API_KEY",
                    "base_url": "https://api.elevenlabs.io/v1",
                    "model": "eleven_monolingual_v1",
                    "enabled": False,
                    "supports_audio": True
                }
            },
            "bots": {},
            "global": {
                "log_level": "INFO",
                "max_concurrent_requests": 10,
                "default_timeout": 30,
                "data_directory": "./data",
                "encryption_enabled": True,
                "metrics_enabled": True,
                "backup_enabled": True
            }
        }
    
    # Backend management methods
    def get_backend_config(self, backend_name: str) -> Optional[BackendConfig]:
        """Get backend configuration with decryption"""
        backend_data = self._config_data.get("backends", {}).get(backend_name)
        if not backend_data:
            return None
        
        # Decrypt API key if encrypted
        if backend_data.get("api_key") and backend_data["api_key"].startswith("encrypted:"):
            try:
                decrypted_key = self.encryption.decrypt(backend_data["api_key"][10:])
                backend_data = backend_data.copy()
                backend_data["api_key"] = decrypted_key
            except Exception as e:
                self.logger.error(f"Failed to decrypt API key for {backend_name}: {e}")
                return None
        
        try:
            return BackendConfig(**backend_data)
        except Exception as e:
            self.logger.error(f"Invalid backend config for {backend_name}: {e}")
            return None
    
    def set_backend_config(self, backend_name: str, config: BackendConfig):
        """Set backend configuration with encryption"""
        config_dict = config.model_dump(exclude_unset=True)
        
        # Encrypt API key if provided
        if config_dict.get("api_key"):
            encrypted_key = self.encryption.encrypt(config_dict["api_key"])
            config_dict["api_key"] = f"encrypted:{encrypted_key}"
        
        if "backends" not in self._config_data:
            self._config_data["backends"] = {}
        
        self._config_data["backends"][backend_name] = config_dict
        self.save_config()
    
    # Bot management methods
    def get_bot_config(self, bot_name: str) -> Optional[BotConfig]:
        """Get bot configuration"""
        bot_data = self._config_data.get("bots", {}).get(bot_name)
        if not bot_data:
            return None
        
        try:
            return BotConfig(**bot_data)
        except Exception as e:
            self.logger.error(f"Invalid bot config for {bot_name}: {e}")
            return None
    
    def set_bot_config(self, bot_name: str, config: BotConfig):
        """Set bot configuration"""
        config_dict = config.model_dump(exclude_unset=True)
        config_dict["updated_at"] = datetime.now()
        
        if "bots" not in self._config_data:
            self._config_data["bots"] = {}
        
        self._config_data["bots"][bot_name] = config_dict
        self.save_config()
    
    # Global configuration methods
    def get_global_config(self) -> GlobalConfig:
        """Get global configuration"""
        global_data = self._config_data.get("global", {})
        return GlobalConfig(**global_data)
    
    def set_global_config(self, config: GlobalConfig):
        """Set global configuration"""
        self._config_data["global"] = config.model_dump()
        self.save_config()
    
    # Utility methods
    def list_backends(self) -> List[str]:
        """List all configured backends"""
        return list(self._config_data.get("backends", {}).keys())
    
    def list_bots(self) -> List[str]:
        """List all configured bots"""
        return list(self._config_data.get("bots", {}).keys())
    
    def delete_backend(self, backend_name: str):
        """Delete backend configuration"""
        if backend_name in self._config_data.get("backends", {}):
            del self._config_data["backends"][backend_name]
            self.save_config()
            self.logger.info(f"Deleted backend: {backend_name}")
    
    def delete_bot(self, bot_name: str):
        """Delete bot configuration"""
        if bot_name in self._config_data.get("bots", {}):
            del self._config_data["bots"][bot_name]
            self.save_config()
            self.logger.info(f"Deleted bot: {bot_name}")
    
    def export_config(self, export_path: str, include_secrets: bool = False):
        """Export configuration to a file"""
        export_data = self._config_data.copy()
        
        if not include_secrets:
            # Remove encrypted API keys
            for backend_name, backend_data in export_data.get("backends", {}).items():
                if backend_data.get("api_key", "").startswith("encrypted:"):
                    backend_data["api_key"] = "[REDACTED]"
        
        with open(export_path, 'w') as f:
            yaml.dump(export_data, f, default_flow_style=False, indent=2)
        
        self.logger.info(f"Configuration exported to {export_path}")
    
    def validate_all_configs(self) -> Dict[str, List[str]]:
        """Validate all configurations and return errors"""
        errors = {"backends": [], "bots": [], "global": []}
        
        # Validate backends
        for name in self.list_backends():
            try:
                config = self.get_backend_config(name)
                if config is None:
                    errors["backends"].append(f"{name}: Failed to load configuration")
            except Exception as e:
                errors["backends"].append(f"{name}: {str(e)}")
        
        # Validate bots
        for name in self.list_bots():
            try:
                config = self.get_bot_config(name)
                if config is None:
                    errors["bots"].append(f"{name}: Failed to load configuration")
            except Exception as e:
                errors["bots"].append(f"{name}: {str(e)}")
        
        # Validate global config
        try:
            self.get_global_config()
        except Exception as e:
            errors["global"].append(f"Global config error: {str(e)}")
        
        return errors
    
    def get_config_stats(self) -> Dict[str, Any]:
        """Get configuration statistics"""
        return {
            "config_file": str(self.config_path),
            "file_size": self.config_path.stat().st_size if self.config_path.exists() else 0,
            "last_modified": datetime.fromtimestamp(self._last_modified) if self._last_modified else None,
            "backend_count": len(self.list_backends()),
            "bot_count": len(self.list_bots()),
            "enabled_backends": len([
                name for name in self.list_backends()
                if self.get_backend_config(name) and self.get_backend_config(name).enabled
            ]),
            "watchers_count": len(self._watchers),
        }