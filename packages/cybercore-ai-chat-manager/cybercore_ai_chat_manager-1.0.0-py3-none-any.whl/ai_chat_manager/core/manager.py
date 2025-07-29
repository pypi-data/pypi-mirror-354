"""
Enhanced Chat Manager for AI Chat Manager

This module provides the main orchestration layer for managing multiple AI backends,
bots, users, and system-wide operations with advanced features like load balancing,
health monitoring, and plugin management.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Callable, Set
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
import weakref

from .config import Config, BotConfig, BackendConfig, GlobalConfig
from .bot import Bot, create_bot_from_template
from .types import Message, ChatResponse, ConversationHistory
from .exceptions import (
    BotNotFoundError, BackendError, ConfigurationError,
    AIChatManagerError, ValidationError, NetworkError
)

logger = logging.getLogger(__name__)

@dataclass
class BackendHealth:
    """Backend health information"""
    name: str
    is_healthy: bool = True
    last_check: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
    error_count: int = 0
    success_count: int = 0
    last_error: Optional[str] = None
    consecutive_failures: int = 0
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.error_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def is_degraded(self) -> bool:
        return self.success_rate < 0.8 or self.consecutive_failures > 3

@dataclass
class SystemMetrics:
    """System-wide metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    active_bots: int = 0
    active_users: int = 0
    uptime_start: datetime = field(default_factory=datetime.now)
    
    @property
    def success_rate(self) -> float:
        return self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0
    
    @property
    def uptime_hours(self) -> float:
        return (datetime.now() - self.uptime_start).total_seconds() / 3600

class LoadBalancer:
    """Load balancer for distributing requests across backends"""
    
    def __init__(self):
        self.backend_weights: Dict[str, float] = {}
        self.backend_health: Dict[str, BackendHealth] = {}
        self.request_counts: Dict[str, int] = {}
    
    def add_backend(self, name: str, weight: float = 1.0):
        """Add backend to load balancer"""
        self.backend_weights[name] = weight
        self.backend_health[name] = BackendHealth(name=name)
        self.request_counts[name] = 0
    
    def select_backend(self, available_backends: List[str]) -> Optional[str]:
        """Select best backend based on health and load"""
        if not available_backends:
            return None
        
        # Filter healthy backends
        healthy_backends = [
            name for name in available_backends
            if self.backend_health.get(name, BackendHealth(name)).is_healthy
        ]
        
        if not healthy_backends:
            # Fall back to degraded backends if no healthy ones
            degraded_backends = [
                name for name in available_backends
                if not self.backend_health.get(name, BackendHealth(name)).is_degraded
            ]
            healthy_backends = degraded_backends or available_backends
        
        # Select backend with lowest load and best health
        best_backend = None
        best_score = float('inf')
        
        for backend_name in healthy_backends:
            health = self.backend_health.get(backend_name, BackendHealth(backend_name))
            weight = self.backend_weights.get(backend_name, 1.0)
            load = self.request_counts.get(backend_name, 0)
            
            # Calculate score (lower is better)
            score = load / weight + (1 - health.success_rate) * 10
            
            if score < best_score:
                best_score = score
                best_backend = backend_name
        
        return best_backend
    
    def record_request(self, backend_name: str, success: bool, response_time: float):
        """Record request result for load balancing"""
        self.request_counts[backend_name] = self.request_counts.get(backend_name, 0) + 1
        
        health = self.backend_health.get(backend_name, BackendHealth(backend_name))
        health.last_check = datetime.now()
        health.response_time = response_time
        
        if success:
            health.success_count += 1
            health.consecutive_failures = 0
        else:
            health.error_count += 1
            health.consecutive_failures += 1
        
        # Update health status
        health.is_healthy = health.consecutive_failures < 5 and health.success_rate > 0.5
        self.backend_health[backend_name] = health

class PluginManager:
    """Plugin system for extending functionality"""
    
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(self, name: str, plugin_class: type):
        """Register a plugin"""
        try:
            plugin_instance = plugin_class()
            self.plugins[name] = plugin_instance
            
            # Register hooks
            if hasattr(plugin_instance, 'register_hooks'):
                plugin_instance.register_hooks(self)
                
            logger.info(f"Plugin '{name}' registered successfully")
        except Exception as e:
            logger.error(f"Failed to register plugin '{name}': {e}")
    
    def add_hook(self, event: str, callback: Callable):
        """Add hook for specific event"""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    async def call_hooks(self, event: str, *args, **kwargs):
        """Call all hooks for an event"""
        for callback in self.hooks.get(event, []):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Hook callback failed for event '{event}': {e}")

class ChatManager:
    """
    Enhanced main manager for AI chat bots and backends
    
    This class provides comprehensive management of:
    - Multiple AI backends with load balancing
    - Bot lifecycle management
    - User session management
    - Health monitoring and metrics
    - Plugin system
    - Advanced configuration management
    """
    
    def __init__(self, config_path: str = "config.yaml", auto_start: bool = True):
        self.config = Config(config_path)
        self.backends: Dict[str, Any] = {}
        self.bots: Dict[str, Bot] = {}
        self.user_sessions: Dict[str, Dict[str, Bot]] = {}  # user_id -> {bot_name: bot}
        
        # Advanced features
        self.load_balancer = LoadBalancer()
        self.plugin_manager = PluginManager()
        self.metrics = SystemMetrics()
        self.health_monitor_task: Optional[asyncio.Task] = None
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Weak references to track active bots
        self._active_bots: weakref.WeakSet = weakref.WeakSet()
        
        # Initialize system
        if auto_start:
            self.initialize()
    
    def initialize(self):
        """Initialize the chat manager system"""
        try:
            logger.info("Initializing AI Chat Manager...")
            
            # Initialize backends
            self._initialize_backends()
            
            # Initialize bots
            self._initialize_bots()
            
            # Start health monitoring
            self._start_health_monitoring()
            
            # Load plugins
            self._load_plugins()
            
            logger.info("AI Chat Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chat Manager: {e}")
            raise ConfigurationError(f"Initialization failed: {e}")
    
    def _initialize_backends(self):
        """Initialize all configured backends with enhanced error handling"""
        from ..backends import get_backend_class
        
        backend_names = self.config.list_backends()
        logger.info(f"Initializing {len(backend_names)} backends...")
        
        for backend_name in backend_names:
            try:
                backend_config = self.config.get_backend_config(backend_name)
                if not backend_config or not backend_config.enabled:
                    logger.debug(f"Skipping disabled backend: {backend_name}")
                    continue
                
                backend_class = get_backend_class(backend_config.backend_type.value)
                if not backend_class:
                    logger.warning(f"Backend class not found: {backend_config.backend_type}")
                    continue
                
                # Initialize backend
                backend_instance = backend_class(backend_config)
                self.backends[backend_name] = backend_instance
                
                # Add to load balancer
                self.load_balancer.add_backend(backend_name)
                
                logger.info(f"✓ Initialized backend: {backend_name} ({backend_config.backend_type})")
                
            except Exception as e:
                logger.error(f"✗ Failed to initialize backend {backend_name}: {e}")
                # Continue with other backends
                continue
        
        if not self.backends:
            raise ConfigurationError("No backends were successfully initialized")
    
    def _initialize_bots(self):
        """Initialize all configured bots"""
        bot_names = self.config.list_bots()
        logger.info(f"Initializing {len(bot_names)} bots...")
        
        for bot_name in bot_names:
            try:
                self.load_bot(bot_name)
                logger.info(f"✓ Initialized bot: {bot_name}")
            except Exception as e:
                logger.error(f"✗ Failed to initialize bot {bot_name}: {e}")
                continue
    
    def _start_health_monitoring(self):
        """Start background health monitoring"""
        global_config = self.config.get_global_config()
        if global_config.health_check_enabled:
            self.health_monitor_task = asyncio.create_task(self._health_monitor_loop())
            logger.info("Health monitoring started")
    
    async def _health_monitor_loop(self):
        """Background health monitoring loop"""
        global_config = self.config.get_global_config()
        interval = global_config.health_check_interval
        
        while True:
            try:
                await asyncio.sleep(interval)
                await self._check_backend_health()
                await self._cleanup_inactive_sessions()
                await self._update_metrics()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
    
    async def _check_backend_health(self):
        """Check health of all backends"""
        for backend_name, backend in self.backends.items():
            try:
                start_time = datetime.now()
                
                # Simple health check - could be enhanced
                is_healthy = backend.health_check() if hasattr(backend, 'health_check') else True
                
                response_time = (datetime.now() - start_time).total_seconds()
                
                self.load_balancer.record_request(backend_name, is_healthy, response_time)
                
            except Exception as e:
                logger.warning(f"Health check failed for {backend_name}: {e}")
                self.load_balancer.record_request(backend_name, False, 0.0)
    
    async def _cleanup_inactive_sessions(self):
        """Clean up inactive user sessions"""
        global_config = self.config.get_global_config()
        timeout = timedelta(minutes=global_config.session_timeout_minutes)
        cutoff_time = datetime.now() - timeout
        
        inactive_sessions = []
        
        for user_id, user_bots in self.user_sessions.items():
            for bot_name, bot in user_bots.items():
                if bot.conversation_history.last_activity < cutoff_time:
                    inactive_sessions.append((user_id, bot_name))
        
        for user_id, bot_name in inactive_sessions:
            await self._cleanup_user_session(user_id, bot_name)
    
    async def _cleanup_user_session(self, user_id: str, bot_name: str):
        """Clean up specific user session"""
        try:
            if user_id in self.user_sessions and bot_name in self.user_sessions[user_id]:
                bot = self.user_sessions[user_id][bot_name]
                
                # Save final state
                if hasattr(bot, '_save_conversation_history'):
                    bot._save_conversation_history()
                if hasattr(bot, '_save_user_profile'):
                    bot._save_user_profile()
                
                # Remove from active sessions
                del self.user_sessions[user_id][bot_name]
                
                if not self.user_sessions[user_id]:
                    del self.user_sessions[user_id]
                
                logger.debug(f"Cleaned up inactive session: {user_id}/{bot_name}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup session {user_id}/{bot_name}: {e}")
    
    async def _update_metrics(self):
        """Update system metrics"""
        self.metrics.active_bots = len(self._active_bots)
        self.metrics.active_users = len(self.user_sessions)
    
    def _load_plugins(self):
        """Load configured plugins"""
        # Plugin loading would be implemented here
        # For now, just log that plugin system is ready
        logger.info("Plugin system ready")
    
    # Backend management methods
    
    def create_backend(self, name: str, backend_type: str, **kwargs) -> None:
        """Create and configure a new backend"""
        from ..backends import get_backend_class
        from .config import BackendConfig, BackendType
        
        try:
            # Validate backend type
            if backend_type not in [bt.value for bt in BackendType]:
                raise ValidationError(f"Unknown backend type: {backend_type}")
            
            # Create configuration
            backend_config = BackendConfig(
                name=name,
                backend_type=BackendType(backend_type),
                **kwargs
            )
            
            # Save configuration
            self.config.set_backend_config(name, backend_config)
            
            # Initialize backend if enabled
            if backend_config.enabled:
                backend_class = get_backend_class(backend_type)
                if not backend_class:
                    raise ConfigurationError(f"Backend class not found for type: {backend_type}")
                
                backend_instance = backend_class(backend_config)
                self.backends[name] = backend_instance
                self.load_balancer.add_backend(name)
                
                logger.info(f"✓ Created and initialized backend: {name}")
            
        except Exception as e:
            logger.error(f"Failed to create backend {name}: {e}")
            raise
    
    def get_backend_health(self, backend_name: str) -> Optional[BackendHealth]:
        """Get backend health information"""
        return self.load_balancer.backend_health.get(backend_name)
    
    def get_all_backend_health(self) -> Dict[str, BackendHealth]:
        """Get health information for all backends"""
        return self.load_balancer.backend_health.copy()
    
    # Bot management methods
    
    def create_bot(self, name: str, backend: str, **kwargs) -> Bot:
        """Create a new bot with enhanced validation"""
        try:
            # Validate backend exists and is available
            if backend not in self.backends:
                available_backends = list(self.backends.keys())
                raise BackendError(
                    f"Backend '{backend}' not available",
                    backend_name=backend,
                    details={"available_backends": available_backends}
                )
            
            # Create bot configuration
            bot_config = BotConfig(
                name=name,
                backend=backend,
                **kwargs
            )
            
            # Save configuration
            self.config.set_bot_config(name, bot_config)
            
            # Create bot instance
            bot = Bot(name, self.config, self.backends[backend])
            self.bots[name] = bot
            self._active_bots.add(bot)
            
            # Emit event
            asyncio.create_task(self.plugin_manager.call_hooks('bot_created', bot))
            
            logger.info(f"✓ Created bot: {name} (backend: {backend})")
            return bot
            
        except Exception as e:
            logger.error(f"Failed to create bot {name}: {e}")
            raise
    
    def create_bot_from_template(self, name: str, template: str, backend: str, **overrides) -> Bot:
        """Create bot from predefined template"""
        if backend not in self.backends:
            raise BackendError(f"Backend '{backend}' not available")
        
        bot = create_bot_from_template(
            name, template, self.config, self.backends[backend], **overrides
        )
        
        self.bots[name] = bot
        self._active_bots.add(bot)
        
        logger.info(f"✓ Created bot from template: {name} (template: {template})")
        return bot
    
    def load_bot(self, name: str, user_id: Optional[str] = None) -> Bot:
        """Load an existing bot with user session support"""
        try:
            bot_config = self.config.get_bot_config(name)
            if not bot_config:
                available_bots = self.config.list_bots()
                raise BotNotFoundError(
                    f"Bot '{name}' not found",
                    bot_name=name,
                    available_bots=available_bots
                )
            
            # Check if backend is available
            if bot_config.backend not in self.backends:
                raise BackendError(
                    f"Backend '{bot_config.backend}' not available for bot '{name}'",
                    backend_name=bot_config.backend
                )
            
            # Create user-specific bot instance if user_id provided
            if user_id:
                # Check if user already has this bot
                if user_id in self.user_sessions and name in self.user_sessions[user_id]:
                    return self.user_sessions[user_id][name]
                
                # Create new user session
                bot = Bot(name, self.config, self.backends[bot_config.backend], user_id=user_id)
                
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = {}
                self.user_sessions[user_id][name] = bot
            else:
                # Shared bot instance
                if name in self.bots:
                    return self.bots[name]
                
                bot = Bot(name, self.config, self.backends[bot_config.backend])
                self.bots[name] = bot
            
            self._active_bots.add(bot)
            return bot
            
        except Exception as e:
            logger.error(f"Failed to load bot {name}: {e}")
            raise
    
    def get_bot(self, name: str, user_id: Optional[str] = None) -> Bot:
        """Get a bot instance (load if necessary)"""
        return self.load_bot(name, user_id)
    
    def delete_bot(self, name: str, delete_data: bool = False):
        """Delete a bot and optionally its data"""
        try:
            # Remove from memory
            if name in self.bots:
                del self.bots[name]
            
            # Remove from user sessions
            for user_sessions in self.user_sessions.values():
                if name in user_sessions:
                    del user_sessions[name]
            
            # Remove from config
            self.config.delete_bot(name)
            
            # Delete data if requested
            if delete_data:
                global_config = self.config.get_global_config()
                data_dir = Path(global_config.data_directory)
                bot_data_dir = data_dir / "bots" / name
                
                if bot_data_dir.exists():
                    import shutil
                    shutil.rmtree(bot_data_dir)
                    logger.info(f"Deleted bot data: {bot_data_dir}")
            
            logger.info(f"✓ Deleted bot: {name}")
            
        except Exception as e:
            logger.error(f"Failed to delete bot {name}: {e}")
            raise
    
    # Chat methods with load balancing
    
    async def chat_with_bot(
        self, 
        bot_name: str, 
        message: str, 
        user_id: Optional[str] = None,
        preferred_backend: Optional[str] = None,
        **kwargs
    ) -> str:
        """Send a message to a specific bot with backend selection"""
        try:
            start_time = datetime.now()
            
            # Get bot instance
            bot = self.get_bot(bot_name, user_id)
            
            # Select backend if load balancing is needed
            if preferred_backend and preferred_backend in self.backends:
                # Use preferred backend if available
                selected_backend = self.backends[preferred_backend]
                backend_name = preferred_backend
            else:
                # Use bot's configured backend
                selected_backend = bot.backend
                backend_name = bot.backend.name
            
            # Update bot's backend if different
            if bot.backend != selected_backend:
                bot.backend = selected_backend
            
            # Send message
            response = await bot.chat(message, **kwargs)
            
            # Record metrics
            response_time = (datetime.now() - start_time).total_seconds()
            self.load_balancer.record_request(backend_name, True, response_time)
            
            self.metrics.total_requests += 1
            self.metrics.successful_requests += 1
            
            if response.usage:
                self.metrics.total_tokens += response.usage.total_tokens
                self.metrics.total_cost += response.usage.cost_estimate or 0
            
            # Update average response time
            if self.metrics.total_requests == 1:
                self.metrics.average_response_time = response_time
            else:
                self.metrics.average_response_time = (
                    (self.metrics.average_response_time * (self.metrics.total_requests - 1) + response_time)
                    / self.metrics.total_requests
                )
            
            # Emit event
            await self.plugin_manager.call_hooks('message_processed', bot, message, response)
            
            return response.content
            
        except Exception as e:
            # Record failure
            self.metrics.total_requests += 1
            self.metrics.failed_requests += 1
            
            if hasattr(bot, 'backend') and hasattr(bot.backend, 'name'):
                self.load_balancer.record_request(bot.backend.name, False, 0.0)
            
            logger.error(f"Chat failed for bot {bot_name}: {e}")
            raise
    
    async def smart_chat(
        self,
        message: str,
        user_id: str,
        bot_preferences: Optional[List[str]] = None,
        backend_preferences: Optional[List[str]] = None,
        **kwargs
    ) -> ChatResponse:
        """Smart chat that automatically selects best bot and backend"""
        
        # Select best bot based on preferences and availability
        available_bots = bot_preferences or self.config.list_bots()
        
        if not available_bots:
            raise BotNotFoundError("No bots available")
        
        # For now, use first available bot
        # Could be enhanced with ML-based bot selection
        bot_name = available_bots[0]
        
        # Select best backend
        bot_config = self.config.get_bot_config(bot_name)
        if not bot_config:
            raise BotNotFoundError(f"Bot {bot_name} not found")
        
        available_backends = backend_preferences or [bot_config.backend]
        selected_backend = self.load_balancer.select_backend(available_backends)
        
        if not selected_backend:
            raise BackendError("No healthy backends available")
        
        # Get bot and chat
        bot = self.get_bot(bot_name, user_id)
        response = await bot.chat(message, **kwargs)
        
        return response
    
    # System management methods
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        backend_status = {}
        for name, backend in self.backends.items():
            health = self.get_backend_health(name)
            backend_status[name] = {
                "type": backend.__class__.__name__,
                "healthy": health.is_healthy if health else True,
                "response_time": health.response_time if health else 0.0,
                "success_rate": health.success_rate if health else 1.0,
            }
        
        bot_status = {}
        for name in self.config.list_bots():
            bot_config = self.config.get_bot_config(name)
            bot_status[name] = {
                "backend": bot_config.backend if bot_config else "unknown",
                "active_sessions": sum(
                    1 for user_bots in self.user_sessions.values() 
                    if name in user_bots
                ),
                "memory_enabled": bot_config.memory_enabled if bot_config else False,
                "learning_enabled": bot_config.learning_enabled if bot_config else False,
            }
        
        return {
            "system": {
                "uptime_hours": self.metrics.uptime_hours,
                "total_requests": self.metrics.total_requests,
                "success_rate": self.metrics.success_rate,
                "average_response_time": self.metrics.average_response_time,
                "total_tokens": self.metrics.total_tokens,
                "total_cost": self.metrics.total_cost,
                "active_bots": self.metrics.active_bots,
                "active_users": self.metrics.active_users,
            },
            "backends": backend_status,
            "bots": bot_status,
            "config_path": str(self.config.config_path),
        }
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed system metrics"""
        return {
            "system_metrics": self.metrics.__dict__,
            "backend_health": {
                name: health.__dict__ 
                for name, health in self.load_balancer.backend_health.items()
            },
            "load_balancer": {
                "backend_weights": self.load_balancer.backend_weights,
                "request_counts": self.load_balancer.request_counts,
            },
            "sessions": {
                "total_users": len(self.user_sessions),
                "total_sessions": sum(len(user_bots) for user_bots in self.user_sessions.values()),
                "users_per_bot": {
                    bot_name: sum(
                        1 for user_bots in self.user_sessions.values()
                        if bot_name in user_bots
                    )
                    for bot_name in self.config.list_bots()
                }
            }
        }
    
    # Event system
    
    def add_event_handler(self, event: str, handler: Callable):
        """Add event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    async def emit_event(self, event: str, *args, **kwargs):
        """Emit event to all handlers"""
        for handler in self.event_handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args, **kwargs)
                else:
                    handler(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Event handler failed for '{event}': {e}")
    
    # Lifecycle methods
    
    async def shutdown(self):
        """Graceful shutdown of the chat manager"""
        logger.info("Shutting down Chat Manager...")
        
        try:
            # Cancel health monitoring
            if self.health_monitor_task:
                self.health_monitor_task.cancel()
                try:
                    await self.health_monitor_task
                except asyncio.CancelledError:
                    pass
            
            # Save all bot states
            for bot in self._active_bots:
                try:
                    if hasattr(bot, '_save_conversation_history'):
                        bot._save_conversation_history()
                    if hasattr(bot, '_save_user_profile'):
                        bot._save_user_profile()
                except Exception as e:
                    logger.warning(f"Failed to save bot state: {e}")
            
            # Close backend connections
            for backend in self.backends.values():
                try:
                    if hasattr(backend, 'close'):
                        await backend.close()
                    elif hasattr(backend, '__aexit__'):
                        await backend.__aexit__(None, None, None)
                except Exception as e:
                    logger.warning(f"Failed to close backend: {e}")
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            logger.info("Chat Manager shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.shutdown()
    
    # Utility methods
    
    def list_backends(self) -> List[str]:
        """List all available backends"""
        return list(self.backends.keys())
    
    def list_bots(self) -> List[str]:
        """List all configured bots"""
        return self.config.list_bots()
    
    def list_active_users(self) -> List[str]:
        """List all active users"""
        return list(self.user_sessions.keys())
    
    def get_user_bots(self, user_id: str) -> List[str]:
        """Get list of bots for a specific user"""
        return list(self.user_sessions.get(user_id, {}).keys())
    
    def validate_configuration(self) -> Dict[str, List[str]]:
        """Validate all configurations"""
        return self.config.validate_all_configs()
    
    def export_system_data(self, export_path: str):
        """Export system data for backup"""
        export_data = {
            "config": self.config._config_data,
            "metrics": self.metrics.__dict__,
            "backend_health": {
                name: health.__dict__ 
                for name, health in self.load_balancer.backend_health.items()
            },
            "export_timestamp": datetime.now().isoformat(),
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"System data exported to {export_path}")

# Factory functions

def create_chat_manager(
    config_path: str = "config.yaml",
    backends: Optional[Dict[str, Dict[str, Any]]] = None,
    bots: Optional[Dict[str, Dict[str, Any]]] = None
) -> ChatManager:
    """Factory function to create and configure a chat manager"""
    
    manager = ChatManager(config_path, auto_start=False)
    
    # Add backends if provided
    if backends:
        for name, config in backends.items():
            backend_type = config.pop('type', 'openai')
            manager.create_backend(name, backend_type, **config)
    
    # Add bots if provided
    if bots:
        for name, config in bots.items():
            backend = config.pop('backend')
            if 'template' in config:
                template = config.pop('template')
                manager.create_bot_from_template(name, template, backend, **config)
            else:
                manager.create_bot(name, backend, **config)
    
    # Initialize the manager
    manager.initialize()
    
    return manager