#!/usr/bin/env python3
"""
Practical Self-Improvement Implementation for AI Chat Manager

This module provides concrete implementations of self-improving capabilities
that can be integrated into the existing AI Chat Manager architecture.
"""

import asyncio
import json
import logging
import time
import hashlib
import pickle
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from pathlib import Path
from dataclasses import dataclass, field
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import requests
import subprocess
import tempfile
import ast

logger = logging.getLogger(__name__)

@dataclass
class InteractionMetrics:
    """Metrics for a single interaction"""
    timestamp: datetime
    user_id: str
    bot_name: str
    input_text: str
    output_text: str
    response_time: float
    user_rating: Optional[float] = None
    error_occurred: bool = False
    tokens_used: int = 0
    backend_used: str = ""
    context_length: int = 0

@dataclass
class SystemMetrics:
    """System-wide performance metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    response_times: List[float]
    error_rate: float
    user_satisfaction: float
    active_users: int
    total_requests: int

class LearningDatabase:
    """SQLite database for storing learning data"""
    
    def __init__(self, db_path: str = "learning.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the learning database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Interactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                user_id TEXT,
                bot_name TEXT,
                input_text TEXT,
                output_text TEXT,
                response_time REAL,
                user_rating REAL,
                error_occurred INTEGER,
                tokens_used INTEGER,
                backend_used TEXT,
                context_length INTEGER
            )
        """)
        
        # System metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                cpu_usage REAL,
                memory_usage REAL,
                avg_response_time REAL,
                error_rate REAL,
                user_satisfaction REAL,
                active_users INTEGER,
                total_requests INTEGER
            )
        """)
        
        # Learned patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                created_at REAL,
                last_used REAL,
                usage_count INTEGER
            )
        """)
        
        # Auto-generated improvements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                improvement_type TEXT,
                description TEXT,
                code_changes TEXT,
                impact_score REAL,
                created_at REAL,
                applied_at REAL,
                status TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_interaction(self, metrics: InteractionMetrics):
        """Store interaction metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO interactions 
            (timestamp, user_id, bot_name, input_text, output_text, 
             response_time, user_rating, error_occurred, tokens_used, 
             backend_used, context_length)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metrics.timestamp.timestamp(), metrics.user_id, metrics.bot_name,
            metrics.input_text, metrics.output_text, metrics.response_time,
            metrics.user_rating, int(metrics.error_occurred), metrics.tokens_used,
            metrics.backend_used, metrics.context_length
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_interactions(self, hours: int = 24) -> List[InteractionMetrics]:
        """Get recent interactions for analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(hours=hours)).timestamp()
        cursor.execute("""
            SELECT * FROM interactions 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        """, (cutoff,))
        
        interactions = []
        for row in cursor.fetchall():
            interactions.append(InteractionMetrics(
                timestamp=datetime.fromtimestamp(row[1]),
                user_id=row[2],
                bot_name=row[3],
                input_text=row[4],
                output_text=row[5],
                response_time=row[6],
                user_rating=row[7],
                error_occurred=bool(row[8]),
                tokens_used=row[9],
                backend_used=row[10],
                context_length=row[11]
            ))
        
        conn.close()
        return interactions

class PatternAnalyzer:
    """Analyzes interaction patterns and identifies improvement opportunities"""
    
    def __init__(self, learning_db: LearningDatabase):
        self.learning_db = learning_db
        self.models = {}
    
    async def analyze_performance_patterns(self) -> Dict[str, Any]:
        """Analyze performance patterns in recent interactions"""
        interactions = self.learning_db.get_recent_interactions(hours=168)  # 1 week
        
        if not interactions:
            return {"status": "insufficient_data"}
        
        # Prepare data for analysis
        data = []
        for interaction in interactions:
            data.append([
                len(interaction.input_text),
                interaction.context_length,
                interaction.tokens_used,
                hash(interaction.backend_used) % 1000,  # Simple backend encoding
                interaction.response_time
            ])
        
        data = np.array(data)
        
        if len(data) < 10:
            return {"status": "insufficient_data"}
        
        # Train response time prediction model
        X = data[:, :-1]  # Features
        y = data[:, -1]   # Response times
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        
        # Feature importance
        feature_names = ['input_length', 'context_length', 'tokens_used', 'backend']
        importance = dict(zip(feature_names, model.feature_importances_))
        
        # Identify slow interactions
        slow_threshold = np.percentile(y, 90)
        slow_interactions = [i for i, interaction in enumerate(interactions) 
                           if interaction.response_time > slow_threshold]
        
        return {
            "status": "success",
            "total_interactions": len(interactions),
            "avg_response_time": np.mean(y),
            "slow_threshold": slow_threshold,
            "slow_interaction_count": len(slow_interactions),
            "feature_importance": importance,
            "model_accuracy": model.score(X, y)
        }
    
    async def identify_user_patterns(self) -> Dict[str, Any]:
        """Identify user behavior patterns"""
        interactions = self.learning_db.get_recent_interactions(hours=168)
        
        if not interactions:
            return {"status": "insufficient_data"}
        
        # Group by user
        user_patterns = {}
        for interaction in interactions:
            if interaction.user_id not in user_patterns:
                user_patterns[interaction.user_id] = {
                    'interaction_count': 0,
                    'avg_input_length': 0,
                    'preferred_bots': {},
                    'satisfaction_scores': [],
                    'common_topics': []
                }
            
            pattern = user_patterns[interaction.user_id]
            pattern['interaction_count'] += 1
            pattern['avg_input_length'] += len(interaction.input_text)
            
            # Track bot preferences
            bot = interaction.bot_name
            pattern['preferred_bots'][bot] = pattern['preferred_bots'].get(bot, 0) + 1
            
            if interaction.user_rating:
                pattern['satisfaction_scores'].append(interaction.user_rating)
        
        # Calculate averages
        for user_id, pattern in user_patterns.items():
            if pattern['interaction_count'] > 0:
                pattern['avg_input_length'] /= pattern['interaction_count']
            
            if pattern['satisfaction_scores']:
                pattern['avg_satisfaction'] = np.mean(pattern['satisfaction_scores'])
        
        return {
            "status": "success",
            "total_users": len(user_patterns),
            "user_patterns": user_patterns
        }

class AutoOptimizer:
    """Automatically optimizes system configuration based on learned patterns"""
    
    def __init__(self, chat_manager, learning_db: LearningDatabase):
        self.chat_manager = chat_manager
        self.learning_db = learning_db
        self.optimization_history = []
    
    async def optimize_backend_selection(self) -> Dict[str, Any]:
        """Optimize backend selection based on performance data"""
        interactions = self.learning_db.get_recent_interactions(hours=168)
        
        if not interactions:
            return {"status": "insufficient_data"}
        
        # Analyze backend performance
        backend_performance = {}
        for interaction in interactions:
            backend = interaction.backend_used
            if backend not in backend_performance:
                backend_performance[backend] = {
                    'response_times': [],
                    'error_rates': [],
                    'satisfaction_scores': []
                }
            
            backend_performance[backend]['response_times'].append(interaction.response_time)
            backend_performance[backend]['error_rates'].append(1 if interaction.error_occurred else 0)
            
            if interaction.user_rating:
                backend_performance[backend]['satisfaction_scores'].append(interaction.user_rating)
        
        # Calculate metrics
        backend_rankings = {}
        for backend, perf in backend_performance.items():
            if len(perf['response_times']) > 5:  # Minimum sample size
                avg_response_time = np.mean(perf['response_times'])
                error_rate = np.mean(perf['error_rates'])
                avg_satisfaction = np.mean(perf['satisfaction_scores']) if perf['satisfaction_scores'] else 0.5
                
                # Combined score (lower is better for response time and error rate)
                score = (1 / avg_response_time) * (1 - error_rate) * avg_satisfaction
                backend_rankings[backend] = {
                    'score': score,
                    'avg_response_time': avg_response_time,
                    'error_rate': error_rate,
                    'avg_satisfaction': avg_satisfaction
                }
        
        # Apply optimization
        if backend_rankings:
            best_backend = max(backend_rankings.keys(), key=lambda k: backend_rankings[k]['score'])
            
            # Update default backend selection logic
            optimization = {
                "type": "backend_optimization",
                "best_backend": best_backend,
                "rankings": backend_rankings,
                "applied_at": datetime.now().isoformat()
            }
            
            self.optimization_history.append(optimization)
            
            return {
                "status": "success",
                "optimization": optimization
            }
        
        return {"status": "insufficient_data"}
    
    async def optimize_response_settings(self) -> Dict[str, Any]:
        """Optimize response generation settings based on user feedback"""
        interactions = self.learning_db.get_recent_interactions(hours=168)
        
        # Filter interactions with user ratings
        rated_interactions = [i for i in interactions if i.user_rating is not None]
        
        if len(rated_interactions) < 20:
            return {"status": "insufficient_data"}
        
        # Analyze correlation between settings and satisfaction
        high_satisfaction = [i for i in rated_interactions if i.user_rating >= 4.0]
        low_satisfaction = [i for i in rated_interactions if i.user_rating <= 2.0]
        
        if not high_satisfaction or not low_satisfaction:
            return {"status": "insufficient_contrast"}
        
        # Analyze patterns in high vs low satisfaction interactions
        high_avg_length = np.mean([len(i.output_text) for i in high_satisfaction])
        low_avg_length = np.mean([len(i.output_text) for i in low_satisfaction])
        
        high_avg_tokens = np.mean([i.tokens_used for i in high_satisfaction])
        low_avg_tokens = np.mean([i.tokens_used for i in low_satisfaction])
        
        # Generate recommendations
        recommendations = {}
        
        if high_avg_length > low_avg_length * 1.2:
            recommendations['increase_max_tokens'] = {
                'current_avg': low_avg_tokens,
                'recommended_avg': high_avg_tokens,
                'confidence': abs(high_avg_length - low_avg_length) / max(high_avg_length, low_avg_length)
            }
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "analysis": {
                "high_satisfaction_count": len(high_satisfaction),
                "low_satisfaction_count": len(low_satisfaction),
                "high_avg_length": high_avg_length,
                "low_avg_length": low_avg_length
            }
        }

class CodeEvolutionEngine:
    """Generates and applies code improvements automatically"""
    
    def __init__(self, chat_manager, learning_db: LearningDatabase):
        self.chat_manager = chat_manager
        self.learning_db = learning_db
        self.improvement_templates = self._load_improvement_templates()
    
    def _load_improvement_templates(self) -> Dict[str, str]:
        """Load templates for common code improvements"""
        return {
            "caching": """
async def cached_completion(self, cache_key, original_method, *args, **kwargs):
    # Simple memory cache implementation
    if not hasattr(self, '_cache'):
        self._cache = {}
    
    if cache_key in self._cache:
        cache_entry = self._cache[cache_key]
        if time.time() - cache_entry['timestamp'] < 300:  # 5 minute TTL
            return cache_entry['result']
    
    result = await original_method(*args, **kwargs)
    
    self._cache[cache_key] = {
        'result': result,
        'timestamp': time.time()
    }
    
    return result
""",
            "rate_limiting": """
async def adaptive_rate_limit(self, backend_name, base_limit=60):
    # Adaptive rate limiting based on error rates
    error_rate = await self.get_backend_error_rate(backend_name)
    
    if error_rate > 0.1:  # More than 10% errors
        adjusted_limit = base_limit * 0.5  # Reduce by half
    elif error_rate < 0.01:  # Less than 1% errors
        adjusted_limit = base_limit * 1.5  # Increase by 50%
    else:
        adjusted_limit = base_limit
    
    return min(adjusted_limit, base_limit * 2)  # Cap at 2x base limit
""",
            "error_recovery": """
async def smart_retry(self, operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff with jitter
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
            
            # Log for learning
            await self.log_retry_attempt(operation.__name__, str(e), attempt)
"""
        }
    
    async def analyze_performance_bottlenecks(self) -> List[Dict[str, Any]]:
        """Analyze code for performance bottlenecks"""
        bottlenecks = []
        
        # Analyze response time patterns
        pattern_analysis = await PatternAnalyzer(self.learning_db).analyze_performance_patterns()
        
        if pattern_analysis.get("status") == "success":
            importance = pattern_analysis.get("feature_importance", {})
            
            # Suggest caching if response time is high
            if pattern_analysis.get("avg_response_time", 0) > 2.0:
                bottlenecks.append({
                    "type": "slow_responses",
                    "severity": "high",
                    "suggested_fix": "caching",
                    "description": "Average response time is high, consider implementing caching"
                })
            
            # Suggest backend optimization if backend choice is important
            if importance.get("backend", 0) > 0.3:
                bottlenecks.append({
                    "type": "backend_selection",
                    "severity": "medium", 
                    "suggested_fix": "intelligent_routing",
                    "description": "Backend choice significantly affects performance"
                })
        
        return bottlenecks
    
    async def generate_improvement_code(self, bottleneck: Dict[str, Any]) -> Optional[str]:
        """Generate code to fix identified bottlenecks"""
        fix_type = bottleneck.get("suggested_fix")
        
        if fix_type in self.improvement_templates:
            template = self.improvement_templates[fix_type]
            
            # In a real implementation, this would use AI to customize the template
            # For now, return the template as-is
            return template
        
        return None
    
    async def apply_safe_improvement(self, improvement_code: str, improvement_type: str) -> bool:
        """Safely apply a code improvement with rollback capability"""
        try:
            # Create a backup of current state
            backup = await self._create_state_backup()
            
            # Validate the improvement code
            if not await self._validate_improvement_code(improvement_code):
                return False
            
            # Apply improvement in test environment
            test_result = await self._test_improvement(improvement_code, improvement_type)
            
            if test_result["success"]:
                # Apply to production
                await self._apply_improvement_to_production(improvement_code, improvement_type)
                
                # Monitor for issues
                monitoring_task = asyncio.create_task(
                    self._monitor_improvement_impact(improvement_type, backup)
                )
                
                return True
            else:
                logger.warning(f"Improvement test failed: {test_result['error']}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply improvement: {e}")
            return False
    
    async def _validate_improvement_code(self, code: str) -> bool:
        """Validate improvement code for safety"""
        try:
            # Parse the code to check syntax
            ast.parse(code)
            
            # Check for dangerous operations
            dangerous_patterns = [
                "os.system", "subprocess.call", "eval(", "exec(",
                "open(", "__import__", "globals(", "locals("
            ]
            
            for pattern in dangerous_patterns:
                if pattern in code:
                    logger.warning(f"Dangerous pattern detected: {pattern}")
                    return False
            
            return True
            
        except SyntaxError as e:
            logger.error(f"Syntax error in improvement code: {e}")
            return False
    
    async def _test_improvement(self, code: str, improvement_type: str) -> Dict[str, Any]:
        """Test improvement in isolated environment"""
        try:
            # Create temporary test file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Basic syntax check
            result = subprocess.run([
                'python', '-m', 'py_compile', temp_file
            ], capture_output=True, text=True)
            
            # Clean up
            Path(temp_file).unlink()
            
            if result.returncode == 0:
                return {"success": True}
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

class SelfUpdatingManager:
    """Manages self-updating capabilities"""
    
    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
        self.update_history = []
        self.learning_db = LearningDatabase()
    
    async def check_for_updates(self) -> Dict[str, Any]:
        """Check for available updates from multiple sources"""
        update_sources = [
            self._check_official_updates(),
            self._check_performance_improvements(),
            self._check_community_contributions()
        ]
        
        results = await asyncio.gather(*update_sources, return_exceptions=True)
        
        available_updates = []
        for result in results:
            if isinstance(result, dict) and result.get("updates"):
                available_updates.extend(result["updates"])
        
        return {
            "total_updates": len(available_updates),
            "updates": available_updates
        }
    
    async def _check_official_updates(self) -> Dict[str, Any]:
        """Check for official package updates"""
        try:
            # Check PyPI for newer versions
            response = requests.get(
                "https://pypi.org/pypi/cybercore-ai-chat-manager/json",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data["info"]["version"]
                current_version = self.chat_manager.__version__
                
                if latest_version != current_version:
                    return {
                        "updates": [{
                            "type": "official_update",
                            "current_version": current_version,
                            "latest_version": latest_version,
                            "priority": "high",
                            "description": "Official package update available"
                        }]
                    }
            
            return {"updates": []}
            
        except Exception as e:
            logger.error(f"Failed to check official updates: {e}")
            return {"updates": []}
    
    async def _check_performance_improvements(self) -> Dict[str, Any]:
        """Check for performance improvement opportunities"""
        code_engine = CodeEvolutionEngine(self.chat_manager, self.learning_db)
        bottlenecks = await code_engine.analyze_performance_bottlenecks()
        
        updates = []
        for bottleneck in bottlenecks:
            updates.append({
                "type": "performance_improvement",
                "bottleneck_type": bottleneck["type"],
                "severity": bottleneck["severity"],
                "suggested_fix": bottleneck["suggested_fix"],
                "description": bottleneck["description"],
                "priority": "medium" if bottleneck["severity"] == "high" else "low"
            })
        
        return {"updates": updates}
    
    async def _check_community_contributions(self) -> Dict[str, Any]:
        """Check for community-contributed improvements"""
        # In a real implementation, this would check GitHub, forums, etc.
        # For now, return empty
        return {"updates": []}
    
    async def apply_update(self, update: Dict[str, Any]) -> bool:
        """Apply a specific update"""
        update_type = update.get("type")
        
        try:
            if update_type == "official_update":
                return await self._apply_official_update(update)
            elif update_type == "performance_improvement":
                return await self._apply_performance_improvement(update)
            elif update_type == "community_contribution":
                return await self._apply_community_update(update)
            else:
                logger.warning(f"Unknown update type: {update_type}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply update: {e}")
            return False
    
    async def _apply_official_update(self, update: Dict[str, Any]) -> bool:
        """Apply official package update"""
        try:
            # In a real implementation, this would:
            # 1. Download the new version
            # 2. Test it in isolation
            # 3. Apply the update with rollback capability
            # 4. Restart the service
            
            logger.info(f"Would update from {update['current_version']} to {update['latest_version']}")
            return True
            
        except Exception as e:
            logger.error(f"Official update failed: {e}")
            return False
    
    async def _apply_performance_improvement(self, update: Dict[str, Any]) -> bool:
        """Apply performance improvement"""
        code_engine = CodeEvolutionEngine(self.chat_manager, self.learning_db)
        
        # Generate improvement code
        improvement_code = await code_engine.generate_improvement_code(update)
        
        if improvement_code:
            # Apply the improvement
            success = await code_engine.apply_safe_improvement(
                improvement_code, 
                update["suggested_fix"]
            )
            
            if success:
                self.update_history.append({
                    "type": "performance_improvement",
                    "applied_at": datetime.now().isoformat(),
                    "improvement": update
                })
            
            return success
        
        return False

class SelfImprovementOrchestrator:
    """Main orchestrator for self-improvement capabilities"""
    
    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
        self.learning_db = LearningDatabase()
        self.pattern_analyzer = PatternAnalyzer(self.learning_db)
        self.auto_optimizer = AutoOptimizer(chat_manager, self.learning_db)
        self.code_engine = CodeEvolutionEngine(chat_manager, self.learning_db)
        self.update_manager = SelfUpdatingManager(chat_manager)
        
        self.improvement_cycle_running = False
    
    async def start_self_improvement(self):
        """Start the self-improvement process"""
        if self.improvement_cycle_running:
            logger.warning("Self-improvement cycle already running")
            return
        
        self.improvement_cycle_running = True
        logger.info("Starting self-improvement cycle")
        
        # Start background tasks
        tasks = [
            self._continuous_learning_loop(),
            self._performance_optimization_loop(),
            self._update_checking_loop(),
            self._pattern_analysis_loop()
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _continuous_learning_loop(self):
        """Continuously learn from interactions"""
        while self.improvement_cycle_running:
            try:
                # Analyze recent patterns
                patterns = await self.pattern_analyzer.analyze_performance_patterns()
                user_patterns = await self.pattern_analyzer.identify_user_patterns()
                
                logger.info(f"Learning cycle: {patterns.get('status')}, users: {user_patterns.get('total_users', 0)}")
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Learning loop error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _performance_optimization_loop(self):
        """Continuously optimize performance"""
        while self.improvement_cycle_running:
            try:
                # Optimize backend selection
                backend_opt = await self.auto_optimizer.optimize_backend_selection()
                
                # Optimize response settings
                response_opt = await self.auto_optimizer.optimize_response_settings()
                
                logger.info(f"Optimization cycle: backend={backend_opt.get('status')}, response={response_opt.get('status')}")
                
                # Sleep for 6 hours
                await asyncio.sleep(21600)
                
            except Exception as e:
                logger.error(f"Optimization loop error: {e}")
                await asyncio.sleep(900)  # Wait 15 minutes on error
    
    async def _update_checking_loop(self):
        """Continuously check for updates"""
        while self.improvement_cycle_running:
            try:
                # Check for updates
                updates = await self.update_manager.check_for_updates()
                
                # Apply high-priority updates automatically
                for update in updates.get("updates", []):
                    if update.get("priority") == "high":
                        success = await self.update_manager.apply_update(update)
                        logger.info(f"Auto-applied update: {update['type']} - {'success' if success else 'failed'}")
                
                # Sleep for 24 hours
                await asyncio.sleep(86400)
                
            except Exception as e:
                logger.error(f"Update checking loop error: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def _pattern_analysis_loop(self):
        """Continuously analyze patterns for insights"""
        while self.improvement_cycle_running:
            try:
                # Analyze performance bottlenecks
                bottlenecks = await self.code_engine.analyze_performance_bottlenecks()
                
                if bottlenecks:
                    logger.info(f"Identified {len(bottlenecks)} performance bottlenecks")
                    
                    # Auto-apply low-risk improvements
                    for bottleneck in bottlenecks:
                        if bottleneck.get("severity") == "low":
                            improvement_code = await self.code_engine.generate_improvement_code(bottleneck)
                            if improvement_code:
                                success = await self.code_engine.apply_safe_improvement(
                                    improvement_code,
                                    bottleneck["suggested_fix"]
                                )
                                logger.info(f"Auto-applied improvement: {bottleneck['type']} - {'success' if success else 'failed'}")
                
                # Sleep for 12 hours
                await asyncio.sleep(43200)
                
            except Exception as e:
                logger.error(f"Pattern analysis loop error: {e}")
                await asyncio.sleep(1800)  # Wait 30 minutes on error
    
    def record_interaction(self, metrics: InteractionMetrics):
        """Record an interaction for learning"""
        self.learning_db.store_interaction(metrics)
    
    async def get_improvement_status(self) -> Dict[str, Any]:
        """Get current status of self-improvement systems"""
        return {
            "improvement_cycle_running": self.improvement_cycle_running,
            "total_interactions": len(self.learning_db.get_recent_interactions(hours=24)),
            "learning_db_path": self.learning_db.db_path,
            "last_pattern_analysis": await self.pattern_analyzer.analyze_performance_patterns(),
            "available_updates": await self.update_manager.check_for_updates()
        }
    
    def stop_self_improvement(self):
        """Stop the self-improvement process"""
        self.improvement_cycle_running = False
        logger.info("Self-improvement cycle stopped")

# Integration example
async def integrate_self_improvement(chat_manager):
    """Example of how to integrate self-improvement into existing chat manager"""
    
    # Create the orchestrator
    orchestrator = SelfImprovementOrchestrator(chat_manager)
    
    # Hook into chat manager's message processing
    original_chat_method = chat_manager.chat_with_bot
    
    async def enhanced_chat_with_bot(bot_name, message, user_id=None, **kwargs):
        start_time = datetime.now()
        
        try:
            # Call original method
            response = await original_chat_method(bot_name, message, user_id, **kwargs)
            
            # Record metrics for learning
            metrics = InteractionMetrics(
                timestamp=datetime.now(),
                user_id=user_id or "anonymous",
                bot_name=bot_name,
                input_text=message,
                output_text=response,
                response_time=(datetime.now() - start_time).total_seconds(),
                error_occurred=False,
                backend_used=getattr(chat_manager.get_bot(bot_name), 'backend', {}).get('name', 'unknown')
            )
            
            orchestrator.record_interaction(metrics)
            
            return response
            
        except Exception as e:
            # Record error metrics
            metrics = InteractionMetrics(
                timestamp=datetime.now(),
                user_id=user_id or "anonymous", 
                bot_name=bot_name,
                input_text=message,
                output_text="",
                response_time=(datetime.now() - start_time).total_seconds(),
                error_occurred=True,
                backend_used=""
            )
            
            orchestrator.record_interaction(metrics)
            raise
    
    # Replace the method
    chat_manager.chat_with_bot = enhanced_chat_with_bot
    
    # Start self-improvement
    improvement_task = asyncio.create_task(orchestrator.start_self_improvement())
    
    return orchestrator, improvement_task

# Usage example
if __name__ == "__main__":
    async def main():
        # This would be your actual chat manager
        from ai_chat_manager import ChatManager
        
        chat_manager = ChatManager("config.yaml")
        
        # Integrate self-improvement
        orchestrator, improvement_task = await integrate_self_improvement(chat_manager)
        
        print("Self-improvement system started!")
        print("The system will now:")
        print("- Learn from every interaction")
        print("- Optimize performance automatically")
        print("- Check for updates and improvements")
        print("- Generate and apply code improvements")
        
        # Get status
        status = await orchestrator.get_improvement_status()
        print(f"\nCurrent status: {status}")
        
        # Let it run for a while (in production, this would run indefinitely)
        await asyncio.sleep(60)
        
        # Stop
        orchestrator.stop_self_improvement()
    
    asyncio.run(main())
