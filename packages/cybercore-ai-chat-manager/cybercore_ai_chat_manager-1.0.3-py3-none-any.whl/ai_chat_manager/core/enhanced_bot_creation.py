"""
Enhanced Bot Creation System for AI Chat Manager

This module provides sophisticated bot creation capabilities including:
- Advanced personality system with trait-based behavior
- Skill-based bot architecture
- Dynamic learning and adaptation
- Multi-modal capabilities
- Plugin system for extensibility
- Context-aware response generation
- Performance optimization
"""

import json
import asyncio
import logging
import uuid
from typing import Dict, List, Any, Optional, Union, Callable, Set, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import importlib
import inspect

from ..core.types import Message, ChatResponse, MessageRole, ContentType
from ..core.config import Config, BotConfig
from ..core.exceptions import ValidationError, BotNotFoundError
from ..core.bot import Bot

logger = logging.getLogger(__name__)

# ============================================================================
# ENHANCED PERSONALITY SYSTEM
# ============================================================================

class PersonalityTrait(Enum):
    """Core personality traits that influence bot behavior"""
    FRIENDLINESS = "friendliness"
    FORMALITY = "formality"
    CREATIVITY = "creativity"
    ANALYTICAL = "analytical"
    EMPATHY = "empathy"
    HUMOR = "humor"
    PATIENCE = "patience"
    ASSERTIVENESS = "assertiveness"
    CURIOSITY = "curiosity"
    OPTIMISM = "optimism"
    CAUTIOUSNESS = "cautiousness"
    EXPRESSIVENESS = "expressiveness"

@dataclass
class PersonalityProfile:
    """Enhanced personality profile with dynamic trait system"""
    traits: Dict[PersonalityTrait, float] = field(default_factory=dict)
    speaking_style: str = "balanced"
    energy_level: float = 0.7
    detail_level: float = 0.7
    interaction_preference: str = "collaborative"
    cultural_context: str = "neutral"
    
    def __post_init__(self):
        # Ensure all traits have default values
        for trait in PersonalityTrait:
            if trait not in self.traits:
                self.traits[trait] = 0.5
    
    def get_trait(self, trait: PersonalityTrait) -> float:
        """Get trait value (0.0 to 1.0)"""
        return self.traits.get(trait, 0.5)
    
    def set_trait(self, trait: PersonalityTrait, value: float):
        """Set trait value with validation"""
        self.traits[trait] = max(0.0, min(1.0, value))
    
    def adjust_trait(self, trait: PersonalityTrait, delta: float):
        """Adjust trait by delta amount"""
        current = self.get_trait(trait)
        self.set_trait(trait, current + delta)
    
    def get_personality_description(self) -> str:
        """Generate natural language description of personality"""
        descriptions = []
        
        # Analyze dominant traits
        high_traits = [trait for trait, value in self.traits.items() if value > 0.7]
        low_traits = [trait for trait, value in self.traits.items() if value < 0.3]
        
        if PersonalityTrait.FRIENDLINESS in high_traits:
            descriptions.append("warm and approachable")
        if PersonalityTrait.ANALYTICAL in high_traits:
            descriptions.append("logical and methodical")
        if PersonalityTrait.CREATIVITY in high_traits:
            descriptions.append("imaginative and innovative")
        if PersonalityTrait.EMPATHY in high_traits:
            descriptions.append("understanding and compassionate")
        if PersonalityTrait.HUMOR in high_traits:
            descriptions.append("witty and entertaining")
        
        if PersonalityTrait.FORMALITY in high_traits:
            descriptions.append("professional and structured")
        elif PersonalityTrait.FORMALITY in low_traits:
            descriptions.append("casual and relaxed")
        
        return ", ".join(descriptions) if descriptions else "balanced and adaptable"
    
    def generate_response_modifiers(self) -> Dict[str, Any]:
        """Generate response modifiers based on personality"""
        modifiers = {}
        
        # Temperature adjustment based on creativity
        creativity = self.get_trait(PersonalityTrait.CREATIVITY)
        modifiers["temperature"] = 0.3 + (creativity * 0.7)
        
        # Response length based on detail level and expressiveness
        expressiveness = self.get_trait(PersonalityTrait.EXPRESSIVENESS)
        modifiers["max_tokens"] = int(100 + (self.detail_level * expressiveness * 400))
        
        # Top-p based on cautiousness
        cautiousness = self.get_trait(PersonalityTrait.CAUTIOUSNESS)
        modifiers["top_p"] = 0.5 + (1 - cautiousness) * 0.5
        
        return modifiers

# ============================================================================
# SKILL SYSTEM
# ============================================================================

class BotSkill(ABC):
    """Abstract base class for bot skills"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
        self.proficiency = 0.5  # 0.0 to 1.0
        self.usage_count = 0
        self.success_rate = 1.0
    
    @abstractmethod
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        """Check if this skill can handle the given message"""
        pass
    
    @abstractmethod
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        """Execute the skill and return response or None"""
        pass
    
    def update_performance(self, success: bool):
        """Update skill performance metrics"""
        self.usage_count += 1
        if success:
            self.success_rate = ((self.success_rate * (self.usage_count - 1)) + 1.0) / self.usage_count
        else:
            self.success_rate = ((self.success_rate * (self.usage_count - 1)) + 0.0) / self.usage_count
        
        # Adjust proficiency based on usage and success
        if success and self.proficiency < 1.0:
            self.proficiency = min(1.0, self.proficiency + 0.01)
        elif not success and self.proficiency > 0.0:
            self.proficiency = max(0.0, self.proficiency - 0.005)

class ResearchSkill(BotSkill):
    """Research and information gathering skill"""
    
    def __init__(self):
        super().__init__("research", "Information gathering and fact-checking")
    
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        research_keywords = ["research", "find", "look up", "information", "facts", "data", "study"]
        return any(keyword in message.content.lower() for keyword in research_keywords)
    
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        # Simulate research capability
        return f"📚 Research mode activated. I'll help you find reliable information about: {message.content}"

class CreativeWritingSkill(BotSkill):
    """Creative writing and storytelling skill"""
    
    def __init__(self):
        super().__init__("creative_writing", "Creative content generation and storytelling")
    
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        creative_keywords = ["write", "story", "poem", "creative", "imagine", "fiction", "character"]
        return any(keyword in message.content.lower() for keyword in creative_keywords)
    
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        return "✨ Creative mode engaged! Let me help you craft something imaginative..."

class AnalysisSkill(BotSkill):
    """Data analysis and logical reasoning skill"""
    
    def __init__(self):
        super().__init__("analysis", "Data analysis and logical reasoning")
    
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        analysis_keywords = ["analyze", "compare", "evaluate", "data", "statistics", "logic", "reasoning"]
        return any(keyword in message.content.lower() for keyword in analysis_keywords)
    
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        return "🧮 Analysis mode activated. I'll break this down systematically..."

class ProblemSolvingSkill(BotSkill):
    """Problem solving and troubleshooting skill"""
    
    def __init__(self):
        super().__init__("problem_solving", "Problem identification and solution development")
    
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        problem_keywords = ["problem", "issue", "help", "solve", "fix", "troubleshoot", "broken"]
        return any(keyword in message.content.lower() for keyword in problem_keywords)
    
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        return "🔧 Problem-solving mode engaged. Let me help you work through this step by step..."

class EmotionalSupportSkill(BotSkill):
    """Emotional support and empathetic responses"""
    
    def __init__(self):
        super().__init__("emotional_support", "Providing empathetic and supportive responses")
    
    async def can_handle(self, message: Message, context: Dict[str, Any]) -> bool:
        emotional_keywords = ["feel", "emotion", "sad", "happy", "anxious", "stress", "support", "comfort"]
        return any(keyword in message.content.lower() for keyword in emotional_keywords)
    
    async def execute(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        return "💙 I'm here to listen and support you. Let's talk about what's on your mind..."

# ============================================================================
# ENHANCED BOT CONFIGURATION
# ============================================================================

@dataclass
class EnhancedBotConfig:
    """Enhanced bot configuration with advanced features"""
    name: str
    backend: str
    personality_profile: PersonalityProfile = field(default_factory=PersonalityProfile)
    skills: List[str] = field(default_factory=list)
    
    # Core settings
    system_prompt_template: str = ""
    base_temperature: float = 0.7
    max_context_length: int = 4000
    memory_enabled: bool = True
    learning_enabled: bool = False
    
    # Advanced features
    adaptive_personality: bool = True
    context_awareness: bool = True
    multi_modal: bool = False
    voice_enabled: bool = False
    
    # Learning and adaptation
    user_preference_learning: bool = True
    conversation_style_adaptation: bool = True
    performance_optimization: bool = True
    
    # Content and safety
    content_filter_enabled: bool = True
    safety_level: str = "medium"
    allowed_topics: List[str] = field(default_factory=list)
    blocked_topics: List[str] = field(default_factory=list)
    
    # Plugin system
    enabled_plugins: List[str] = field(default_factory=list)
    plugin_config: Dict[str, Any] = field(default_factory=dict)
    
    # Performance settings
    response_caching: bool = True
    async_processing: bool = True
    batch_mode: bool = False
    
    def to_bot_config(self) -> BotConfig:
        """Convert to standard BotConfig"""
        return BotConfig(
            name=self.name,
            backend=self.backend,
            system_prompt=self._generate_system_prompt(),
            memory_enabled=self.memory_enabled,
            learning_enabled=self.learning_enabled,
            max_context_length=self.max_context_length,
            temperature=self.base_temperature,
            content_filter_enabled=self.content_filter_enabled,
            safety_level=self.safety_level,
            allowed_topics=self.allowed_topics,
            blocked_topics=self.blocked_topics
        )
    
    def _generate_system_prompt(self) -> str:
        """Generate system prompt based on configuration"""
        if self.system_prompt_template:
            return self.system_prompt_template.format(
                personality=self.personality_profile.get_personality_description(),
                skills=", ".join(self.skills) if self.skills else "general assistance",
                energy=self.personality_profile.energy_level,
                detail=self.personality_profile.detail_level
            )
        
        base_prompt = f"You are {self.name}, an AI assistant with the following characteristics: {self.personality_profile.get_personality_description()}."
        
        if self.skills:
            base_prompt += f" You specialize in: {', '.join(self.skills)}."
        
        base_prompt += f" Your speaking style is {self.personality_profile.speaking_style}."
        
        return base_prompt

# ============================================================================
# ENHANCED BOT CLASS
# ============================================================================

class EnhancedBot(Bot):
    """Enhanced bot with advanced personality, skills, and learning capabilities"""
    
    def __init__(self, name: str, config: Config, backend, enhanced_config: EnhancedBotConfig, user_id: Optional[str] = None):
        # Initialize base bot
        base_config = enhanced_config.to_bot_config()
        config.set_bot_config(name, base_config)
        super().__init__(name, config, backend, user_id)
        
        # Enhanced features
        self.enhanced_config = enhanced_config
        self.personality_profile = enhanced_config.personality_profile
        self.skills = self._initialize_skills()
        self.context_memory = ContextMemory()
        self.adaptation_engine = AdaptationEngine(self)
        self.plugin_manager = BotPluginManager(self)
        
        # Performance tracking
        self.performance_metrics = {
            "response_satisfaction": [],
            "skill_usage": {},
            "personality_adjustments": [],
            "context_hits": 0,
            "learning_iterations": 0
        }
        
        # State
        self.current_context = {}
        self.conversation_style_profile = {}
        self.user_preferences = {}
        
        logger.info(f"Enhanced bot '{name}' initialized with {len(self.skills)} skills")
    
    def _initialize_skills(self) -> Dict[str, BotSkill]:
        """Initialize bot skills based on configuration"""
        available_skills = {
            "research": ResearchSkill,
            "creative_writing": CreativeWritingSkill,
            "analysis": AnalysisSkill,
            "problem_solving": ProblemSolvingSkill,
            "emotional_support": EmotionalSupportSkill
        }
        
        initialized_skills = {}
        for skill_name in self.enhanced_config.skills:
            if skill_name in available_skills:
                initialized_skills[skill_name] = available_skills[skill_name]()
                logger.debug(f"Initialized skill: {skill_name}")
        
        return initialized_skills
    
    async def chat(self, user_message: str, stream: bool = False, **kwargs) -> Union[ChatResponse, Any]:
        """Enhanced chat with personality adaptation and skill routing"""
        
        # Pre-processing
        await self._pre_process_message(user_message)
        
        # Create message object
        message = Message(
            role=MessageRole.USER,
            content=user_message,
            conversation_id=self.conversation_history.id,
            session_id=self.session_id
        )
        
        # Context analysis
        context = await self._analyze_context(message)
        
        # Skill routing
        skill_response = await self._route_to_skills(message, context)
        
        if skill_response:
            # Skill handled the message
            response_content = skill_response
        else:
            # Generate personality-aware response modifiers
            response_modifiers = self.personality_profile.generate_response_modifiers()
            kwargs.update(response_modifiers)
            
            # Use base chat functionality with enhancements
            chat_response = await super().chat(user_message, stream, **kwargs)
            
            if hasattr(chat_response, 'content'):
                response_content = chat_response.content
            else:
                response_content = str(chat_response)
        
        # Post-processing
        enhanced_response = await self._post_process_response(message, response_content, context)
        
        # Adaptation and learning
        if self.enhanced_config.adaptive_personality:
            await self.adaptation_engine.adapt_from_interaction(message, enhanced_response)
        
        # Update context memory
        if self.enhanced_config.context_awareness:
            self.context_memory.update(message, enhanced_response, context)
        
        return enhanced_response
    
    async def _pre_process_message(self, message: str):
        """Pre-process incoming message"""
        # Update conversation style analysis
        if self.enhanced_config.conversation_style_adaptation:
            await self._analyze_conversation_style(message)
        
        # Load user preferences
        if self.enhanced_config.user_preference_learning:
            await self._load_user_preferences()
    
    async def _analyze_context(self, message: Message) -> Dict[str, Any]:
        """Analyze message context for enhanced understanding"""
        context = {
            "message_type": self._classify_message_type(message.content),
            "emotional_tone": self._analyze_emotional_tone(message.content),
            "complexity_level": self._assess_complexity(message.content),
            "topic_category": self._categorize_topic(message.content),
            "urgency_level": self._assess_urgency(message.content),
            "previous_context": self.context_memory.get_relevant_context(message)
        }
        
        self.current_context = context
        return context
    
    def _classify_message_type(self, content: str) -> str:
        """Classify the type of message"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["?", "how", "what", "why", "when", "where", "who"]):
            return "question"
        elif any(word in content_lower for word in ["help", "please", "can you", "could you"]):
            return "request"
        elif any(word in content_lower for word in ["think", "opinion", "feel", "believe"]):
            return "opinion_seeking"
        elif any(word in content_lower for word in ["create", "write", "generate", "make"]):
            return "creative_request"
        else:
            return "conversational"
    
    def _analyze_emotional_tone(self, content: str) -> str:
        """Analyze emotional tone of message"""
        content_lower = content.lower()
        
        positive_words = ["happy", "excited", "great", "awesome", "love", "wonderful"]
        negative_words = ["sad", "angry", "frustrated", "disappointed", "hate", "terrible"]
        neutral_words = ["think", "consider", "maybe", "perhaps", "possibly"]
        
        positive_score = sum(1 for word in positive_words if word in content_lower)
        negative_score = sum(1 for word in negative_words if word in content_lower)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"
    
    def _assess_complexity(self, content: str) -> str:
        """Assess the complexity level of the message"""
        word_count = len(content.split())
        technical_terms = ["algorithm", "analysis", "methodology", "implementation", "optimization"]
        
        if word_count > 50 or any(term in content.lower() for term in technical_terms):
            return "high"
        elif word_count > 20:
            return "medium"
        else:
            return "low"
    
    def _categorize_topic(self, content: str) -> str:
        """Categorize the topic of conversation"""
        categories = {
            "technology": ["tech", "computer", "software", "programming", "code", "AI"],
            "science": ["research", "study", "experiment", "theory", "analysis"],
            "creative": ["write", "story", "art", "creative", "design", "imagine"],
            "personal": ["feel", "life", "personal", "relationship", "emotion"],
            "business": ["work", "business", "management", "strategy", "project"],
            "education": ["learn", "teach", "study", "education", "knowledge"]
        }
        
        content_lower = content.lower()
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return "general"
    
    def _assess_urgency(self, content: str) -> str:
        """Assess urgency level of the message"""
        urgent_words = ["urgent", "emergency", "asap", "immediately", "critical", "help"]
        
        if any(word in content.lower() for word in urgent_words):
            return "high"
        elif "?" in content:
            return "medium"
        else:
            return "low"
    
    async def _route_to_skills(self, message: Message, context: Dict[str, Any]) -> Optional[str]:
        """Route message to appropriate skill if applicable"""
        
        # Check each skill to see if it can handle the message
        for skill_name, skill in self.skills.items():
            if skill.enabled and await skill.can_handle(message, context):
                try:
                    response = await skill.execute(message, context)
                    if response:
                        skill.update_performance(True)
                        self.performance_metrics["skill_usage"][skill_name] = \
                            self.performance_metrics["skill_usage"].get(skill_name, 0) + 1
                        return response
                except Exception as e:
                    skill.update_performance(False)
                    logger.error(f"Skill {skill_name} failed: {e}")
        
        return None
    
    async def _post_process_response(self, message: Message, response: str, context: Dict[str, Any]) -> str:
        """Post-process response with personality and context enhancements"""
        
        # Apply personality-based modifications
        enhanced_response = self._apply_personality_modifications(response, context)
        
        # Add contextual elements if appropriate
        if context.get("urgency_level") == "high":
            enhanced_response = "I understand this is urgent. " + enhanced_response
        
        if context.get("emotional_tone") == "negative":
            empathy_level = self.personality_profile.get_trait(PersonalityTrait.EMPATHY)
            if empathy_level > 0.7:
                enhanced_response = "I can sense this might be difficult. " + enhanced_response
        
        return enhanced_response
    
    def _apply_personality_modifications(self, response: str, context: Dict[str, Any]) -> str:
        """Apply personality-based modifications to response"""
        
        # Adjust formality
        formality = self.personality_profile.get_trait(PersonalityTrait.FORMALITY)
        if formality > 0.8:
            # Make more formal
            response = response.replace("can't", "cannot").replace("won't", "will not")
        elif formality < 0.3:
            # Make more casual
            response = response.replace("cannot", "can't").replace("will not", "won't")
        
        # Add humor if appropriate
        humor = self.personality_profile.get_trait(PersonalityTrait.HUMOR)
        if humor > 0.7 and context.get("emotional_tone") != "negative":
            # Could add appropriate humor here
            pass
        
        # Adjust enthusiasm
        optimism = self.personality_profile.get_trait(PersonalityTrait.OPTIMISM)
        if optimism > 0.8:
            response = response.replace("This might", "This will likely")
            response = response.replace("could be", "should be")
        
        return response
    
    async def _analyze_conversation_style(self, message: str):
        """Analyze user's conversation style for adaptation"""
        
        style_indicators = {
            "formal": len([w for w in message.split() if len(w) > 6]) / len(message.split()),
            "casual": message.count("'") + message.count("like") + message.count("just"),
            "technical": len([w for w in message.split() if w.lower() in ["implementation", "algorithm", "methodology"]]),
            "emotional": len([w for w in message.split() if w.lower() in ["feel", "emotion", "think", "believe"]])
        }
        
        # Update conversation style profile
        for style, score in style_indicators.items():
            if style not in self.conversation_style_profile:
                self.conversation_style_profile[style] = []
            self.conversation_style_profile[style].append(score)
            
            # Keep only recent history
            if len(self.conversation_style_profile[style]) > 10:
                self.conversation_style_profile[style] = self.conversation_style_profile[style][-10:]
    
    async def _load_user_preferences(self):
        """Load and update user preferences"""
        # This would load from persistent storage
        # For now, simulate with in-memory tracking
        pass
    
    def get_enhanced_stats(self) -> Dict[str, Any]:
        """Get enhanced statistics including personality and skills"""
        base_stats = self.get_stats()
        
        enhanced_stats = {
            **base_stats,
            "personality_traits": {trait.value: score for trait, score in self.personality_profile.traits.items()},
            "active_skills": list(self.skills.keys()),
            "skill_performance": {name: {
                "usage_count": skill.usage_count,
                "success_rate": skill.success_rate,
                "proficiency": skill.proficiency
            } for name, skill in self.skills.items()},
            "context_memory_size": len(self.context_memory.contexts),
            "personality_adaptations": len(self.performance_metrics["personality_adjustments"]),
            "conversation_style": self.conversation_style_profile
        }
        
        return enhanced_stats
    
    async def adapt_personality(self, feedback: Dict[str, Any]):
        """Adapt personality based on feedback"""
        
        if "trait_adjustments" in feedback:
            for trait_name, adjustment in feedback["trait_adjustments"].items():
                try:
                    trait = PersonalityTrait(trait_name)
                    self.personality_profile.adjust_trait(trait, adjustment)
                    self.performance_metrics["personality_adjustments"].append({
                        "trait": trait_name,
                        "adjustment": adjustment,
                        "timestamp": datetime.now()
                    })
                except ValueError:
                    logger.warning(f"Unknown personality trait: {trait_name}")
        
        # Regenerate system prompt with new personality
        new_system_prompt = self.enhanced_config._generate_system_prompt()
        # Update bot configuration
        # This would require updating the underlying bot configuration

# ============================================================================
# CONTEXT MEMORY SYSTEM
# ============================================================================

@dataclass
class ContextEntry:
    """Individual context memory entry"""
    timestamp: datetime
    user_message: Message
    bot_response: str
    context_data: Dict[str, Any]
    relevance_score: float = 1.0
    access_count: int = 0
    
    def decay_relevance(self, hours_passed: float):
        """Decay relevance over time"""
        decay_rate = 0.1  # 10% per hour
        self.relevance_score *= (1 - decay_rate) ** hours_passed

class ContextMemory:
    """Advanced context memory system for enhanced conversation awareness"""
    
    def __init__(self, max_contexts: int = 100):
        self.contexts: List[ContextEntry] = []
        self.max_contexts = max_contexts
        self.topic_index: Dict[str, List[int]] = {}  # Topic -> context indices
        self.emotional_index: Dict[str, List[int]] = {}  # Emotion -> context indices
    
    def update(self, message: Message, response: str, context: Dict[str, Any]):
        """Update context memory with new interaction"""
        
        entry = ContextEntry(
            timestamp=datetime.now(),
            user_message=message,
            bot_response=response,
            context_data=context
        )
        
        self.contexts.append(entry)
        
        # Update indices
        topic = context.get("topic_category", "general")
        if topic not in self.topic_index:
            self.topic_index[topic] = []
        self.topic_index[topic].append(len(self.contexts) - 1)
        
        emotion = context.get("emotional_tone", "neutral")
        if emotion not in self.emotional_index:
            self.emotional_index[emotion] = []
        self.emotional_index[emotion].append(len(self.contexts) - 1)
        
        # Maintain size limit
        if len(self.contexts) > self.max_contexts:
            self._cleanup_old_contexts()
    
    def get_relevant_context(self, message: Message, max_results: int = 5) -> List[ContextEntry]:
        """Get relevant context for current message"""
        
        if not self.contexts:
            return []
        
        # Decay relevance scores
        now = datetime.now()
        for context in self.contexts:
            hours_passed = (now - context.timestamp).total_seconds() / 3600
            context.decay_relevance(hours_passed)
        
        # Score contexts by relevance
        scored_contexts = []
        
        for i, context in enumerate(self.contexts):
            score = self._calculate_relevance_score(message, context)
            scored_contexts.append((score, i, context))
        
        # Sort by score and return top results
        scored_contexts.sort(key=lambda x: x[0], reverse=True)
        return [context for _, _, context in scored_contexts[:max_results]]
    
    def _calculate_relevance_score(self, current_message: Message, context_entry: ContextEntry) -> float:
        """Calculate relevance score between current message and context entry"""
        
        score = context_entry.relevance_score
        
        # Keyword similarity
        current_words = set(current_message.content.lower().split())
        context_words = set(context_entry.user_message.content.lower().split())
        word_overlap = len(current_words.intersection(context_words))
        score += word_overlap * 0.1
        
        # Topic similarity
        # This would use more sophisticated topic modeling in a real implementation
        
        # Recency bonus
        hours_old = (datetime.now() - context_entry.timestamp).total_seconds() / 3600
        if hours_old < 1:
            score += 0.5
        elif hours_old < 24:
            score += 0.2
        
        return score
    
    def _cleanup_old_contexts(self):
        """Remove least relevant contexts to maintain size limit"""
        
        # Sort by relevance score
        self.contexts.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Keep only the most relevant contexts
        removed_count = len(self.contexts) - self.max_contexts
        self.contexts = self.contexts[:self.max_contexts]
        
        # Rebuild indices
        self._rebuild_indices()
        
        logger.debug(f"Cleaned up {removed_count} old contexts")
    
    def _rebuild_indices(self):
        """Rebuild topic and emotional indices"""
        self.topic_index.clear()
        self.emotional_index.clear()
        
        for i, context in enumerate(self.contexts):
            topic = context.context_data.get("topic_category", "general")
            if topic not in self.topic_index:
                self.topic_index[topic] = []
            self.topic_index[topic].append(i)
            
            emotion = context.context_data.get("emotional_tone", "neutral")
            if emotion not in self.emotional_index:
                self.emotional_index[emotion] = []
            self.emotional_index[emotion].append(i)

# ============================================================================
# ADAPTATION ENGINE
# ============================================================================

class AdaptationEngine:
    """Engine for dynamic personality and behavior adaptation"""
    
    def __init__(self, bot: EnhancedBot):
        self.bot = bot
        self.adaptation_history: List[Dict[str, Any]] = []
        self.user_feedback_buffer: List[Dict[str, Any]] = []
        self.adaptation_threshold = 0.1  # Minimum change required for adaptation
    
    async def adapt_from_interaction(self, message: Message, response: str):
        """Adapt bot behavior based on interaction"""
        
        # Analyze interaction for adaptation signals
        adaptation_signals = self._analyze_interaction(message, response)
        
        # Apply adaptations if signals are strong enough
        for signal_type, strength in adaptation_signals.items():
            if abs(strength) > self.adaptation_threshold:
                await self._apply_adaptation(signal_type, strength)
    
    def _analyze_interaction(self, message: Message, response: str) -> Dict[str, float]:
        """Analyze interaction for adaptation signals"""
        
        signals = {}
        
        # Analyze message characteristics
        message_length = len(message.content.split())
        response_length = len(response.split())
        
        # Length adaptation signal
        if message_length < 10 and response_length > 50:
            signals["reduce_verbosity"] = 0.2
        elif message_length > 30 and response_length < 20:
            signals["increase_verbosity"] = 0.2
        
        # Formality adaptation signal
        formal_words = ["please", "thank you", "appreciate", "could you"]
        casual_words = ["hey", "cool", "awesome", "yeah"]
        
        formal_count = sum(1 for word in formal_words if word in message.content.lower())
        casual_count = sum(1 for word in casual_words if word in message.content.lower())
        
        if formal_count > casual_count:
            signals["increase_formality"] = 0.1
        elif casual_count > formal_count:
            signals["decrease_formality"] = 0.1
        
        return signals
    
    async def _apply_adaptation(self, signal_type: str, strength: float):
        """Apply specific adaptation based on signal"""
        
        adaptation_applied = False
        
        if signal_type == "reduce_verbosity":
            self.bot.personality_profile.detail_level = max(0.1, self.bot.personality_profile.detail_level - strength)
            adaptation_applied = True
        
        elif signal_type == "increase_verbosity":
            self.bot.personality_profile.detail_level = min(1.0, self.bot.personality_profile.detail_level + strength)
            adaptation_applied = True
        
        elif signal_type == "increase_formality":
            self.bot.personality_profile.adjust_trait(PersonalityTrait.FORMALITY, strength)
            adaptation_applied = True
        
        elif signal_type == "decrease_formality":
            self.bot.personality_profile.adjust_trait(PersonalityTrait.FORMALITY, -strength)
            adaptation_applied = True
        
        if adaptation_applied:
            self.adaptation_history.append({
                "type": signal_type,
                "strength": strength,
                "timestamp": datetime.now(),
                "personality_state": {trait.value: value for trait, value in self.bot.personality_profile.traits.items()}
            })
            
            logger.debug(f"Applied adaptation: {signal_type} with strength {strength}")
    
    def add_user_feedback(self, feedback: Dict[str, Any]):
        """Add user feedback for adaptation"""
        
        feedback["timestamp"] = datetime.now()
        self.user_feedback_buffer.append(feedback)
        
        # Process feedback if buffer is full
        if len(self.user_feedback_buffer) >= 5:
            asyncio.create_task(self._process_feedback_batch())
    
    async def _process_feedback_batch(self):
        """Process accumulated user feedback"""
        
        if not self.user_feedback_buffer:
            return
        
        # Analyze feedback patterns
        feedback_analysis = self._analyze_feedback_patterns()
        
        # Apply adaptations based on feedback
        for adaptation_type, strength in feedback_analysis.items():
            if abs(strength) > self.adaptation_threshold:
                await self._apply_adaptation(adaptation_type, strength)
        
        # Clear buffer
        self.user_feedback_buffer.clear()
    
    def _analyze_feedback_patterns(self) -> Dict[str, float]:
        """Analyze patterns in user feedback"""
        
        patterns = {}
        
        # This would implement sophisticated feedback analysis
        # For now, return empty patterns
        return patterns

# ============================================================================
# PLUGIN SYSTEM
# ============================================================================

class BotPlugin(ABC):
    """Abstract base class for bot plugins"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = True
    
    @abstractmethod
    async def initialize(self, bot: EnhancedBot) -> bool:
        """Initialize the plugin with the bot"""
        pass
    
    @abstractmethod
    async def process_message(self, message: Message, context: Dict[str, Any]) -> Optional[Message]:
        """Process incoming message"""
        pass
    
    @abstractmethod
    async def process_response(self, response: str, context: Dict[str, Any]) -> Optional[str]:
        """Process outgoing response"""
        pass
    
    async def cleanup(self):
        """Cleanup plugin resources"""
        pass

class BotPluginManager:
    """Manager for bot plugins"""
    
    def __init__(self, bot: EnhancedBot):
        self.bot = bot
        self.plugins: Dict[str, BotPlugin] = {}
        self.plugin_order: List[str] = []
    
    async def load_plugin(self, plugin_class: type, config: Dict[str, Any] = None) -> bool:
        """Load a plugin"""
        
        try:
            plugin = plugin_class()
            
            if await plugin.initialize(self.bot):
                self.plugins[plugin.name] = plugin
                self.plugin_order.append(plugin.name)
                logger.info(f"Loaded plugin: {plugin.name} v{plugin.version}")
                return True
            else:
                logger.error(f"Failed to initialize plugin: {plugin.name}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading plugin: {e}")
            return False
    
    async def process_message_chain(self, message: Message, context: Dict[str, Any]) -> Message:
        """Process message through plugin chain"""
        
        current_message = message
        
        for plugin_name in self.plugin_order:
            plugin = self.plugins.get(plugin_name)
            if plugin and plugin.enabled:
                try:
                    processed = await plugin.process_message(current_message, context)
                    if processed:
                        current_message = processed
                except Exception as e:
                    logger.error(f"Plugin {plugin_name} message processing failed: {e}")
        
        return current_message
    
    async def process_response_chain(self, response: str, context: Dict[str, Any]) -> str:
        """Process response through plugin chain"""
        
        current_response = response
        
        for plugin_name in self.plugin_order:
            plugin = self.plugins.get(plugin_name)
            if plugin and plugin.enabled:
                try:
                    processed = await plugin.process_response(current_response, context)
                    if processed:
                        current_response = processed
                except Exception as e:
                    logger.error(f"Plugin {plugin_name} response processing failed: {e}")
        
        return current_response
    
    async def unload_all_plugins(self):
        """Unload all plugins"""
        
        for plugin in self.plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up plugin {plugin.name}: {e}")
        
        self.plugins.clear()
        self.plugin_order.clear()

# ============================================================================
# BOT FACTORY AND CREATION UTILITIES
# ============================================================================

class EnhancedBotFactory:
    """Factory for creating enhanced bots with various configurations"""
    
    @staticmethod
    def create_personality_bot(
        name: str,
        backend: str,
        personality_type: str,
        skills: List[str] = None,
        **kwargs
    ) -> EnhancedBotConfig:
        """Create bot with predefined personality type"""
        
        personality_templates = {
            "helpful_assistant": PersonalityProfile(
                traits={
                    PersonalityTrait.FRIENDLINESS: 0.9,
                    PersonalityTrait.PATIENCE: 0.9,
                    PersonalityTrait.EMPATHY: 0.8,
                    PersonalityTrait.FORMALITY: 0.6
                },
                speaking_style="warm and professional",
                detail_level=0.7
            ),
            
            "creative_companion": PersonalityProfile(
                traits={
                    PersonalityTrait.CREATIVITY: 0.95,
                    PersonalityTrait.EXPRESSIVENESS: 0.9,
                    PersonalityTrait.CURIOSITY: 0.85,
                    PersonalityTrait.OPTIMISM: 0.8
                },
                speaking_style="imaginative and inspiring",
                detail_level=0.8,
                energy_level=0.9
            ),
            
            "analytical_expert": PersonalityProfile(
                traits={
                    PersonalityTrait.ANALYTICAL: 0.95,
                    PersonalityTrait.CAUTIOUSNESS: 0.8,
                    PersonalityTrait.PATIENCE: 0.9,
                    PersonalityTrait.FORMALITY: 0.8
                },
                speaking_style="precise and methodical",
                detail_level=0.9,
                energy_level=0.6
            ),
            
            "empathetic_counselor": PersonalityProfile(
                traits={
                    PersonalityTrait.EMPATHY: 0.95,
                    PersonalityTrait.PATIENCE: 0.95,
                    PersonalityTrait.FRIENDLINESS: 0.9,
                    PersonalityTrait.CAUTIOUSNESS: 0.8
                },
                speaking_style="warm and understanding",
                detail_level=0.7,
                interaction_preference="supportive"
            )
        }
        
        personality = personality_templates.get(personality_type, personality_templates["helpful_assistant"])
        
        return EnhancedBotConfig(
            name=name,
            backend=backend,
            personality_profile=personality,
            skills=skills or [],
            **kwargs
        )
    
    @staticmethod
    def create_skill_based_bot(
        name: str,
        backend: str,
        primary_skills: List[str],
        **kwargs
    ) -> EnhancedBotConfig:
        """Create bot optimized for specific skills"""
        
        # Adjust personality based on primary skills
        personality = PersonalityProfile()
        
        if "creative_writing" in primary_skills:
            personality.set_trait(PersonalityTrait.CREATIVITY, 0.9)
            personality.set_trait(PersonalityTrait.EXPRESSIVENESS, 0.8)
        
        if "analysis" in primary_skills:
            personality.set_trait(PersonalityTrait.ANALYTICAL, 0.9)
            personality.set_trait(PersonalityTrait.CAUTIOUSNESS, 0.8)
        
        if "emotional_support" in primary_skills:
            personality.set_trait(PersonalityTrait.EMPATHY, 0.9)
            personality.set_trait(PersonalityTrait.PATIENCE, 0.9)
        
        return EnhancedBotConfig(
            name=name,
            backend=backend,
            personality_profile=personality,
            skills=primary_skills,
            **kwargs
        )
    
    @staticmethod
    async def create_and_deploy_bot(
        config: EnhancedBotConfig,
        manager_config: Config,
        backend
    ) -> EnhancedBot:
        """Create and deploy an enhanced bot"""
        
        bot = EnhancedBot(
            name=config.name,
            config=manager_config,
            backend=backend,
            enhanced_config=config
        )
        
        return bot

# ============================================================================
# USAGE EXAMPLES AND UTILITIES
# ============================================================================

def create_example_bots() -> List[EnhancedBotConfig]:
    """Create example bot configurations"""
    
    examples = []
    
    # Creative writing assistant
    examples.append(EnhancedBotFactory.create_personality_bot(
        name="creative_muse",
        backend="openai",
        personality_type="creative_companion",
        skills=["creative_writing", "problem_solving"],
        system_prompt_template="You are {name}, a {personality} writing assistant. Your expertise in {skills} helps users create compelling content.",
        adaptive_personality=True,
        learning_enabled=True
    ))
    
    # Data analysis expert
    examples.append(EnhancedBotFactory.create_skill_based_bot(
        name="data_analyst",
        backend="openai",
        primary_skills=["analysis", "research"],
        system_prompt_template="You are {name}, an expert data analyst. You excel at {skills} and provide clear, actionable insights.",
        performance_optimization=True,
        context_awareness=True
    ))
    
    # Emotional support companion
    examples.append(EnhancedBotFactory.create_personality_bot(
        name="wellness_guide",
        backend="anthropic",
        personality_type="empathetic_counselor",
        skills=["emotional_support", "problem_solving"],
        user_preference_learning=True,
        conversation_style_adaptation=True
    ))
    
    return examples

# Export main classes and functions
__all__ = [
    "PersonalityTrait",
    "PersonalityProfile", 
    "BotSkill",
    "EnhancedBotConfig",
    "EnhancedBot",
    "ContextMemory",
    "AdaptationEngine",
    "BotPlugin",
    "BotPluginManager",
    "EnhancedBotFactory",
    "create_example_bots"
]