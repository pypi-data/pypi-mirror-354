"""
Advanced Features Examples for AI Chat Manager

This file demonstrates advanced usage patterns including streaming,
function calling, custom backends, and enterprise features.
"""

import asyncio
import json
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ai_chat_manager import ChatManager
from ai_chat_manager.core.types import Message, MessageRole, FunctionCall
from ai_chat_manager.backends.base import BaseBackend
from ai_chat_manager.core.config import BackendConfig, BackendType

async def example_1_streaming_responses():
    """Example 1: Streaming responses for real-time interaction"""
    print("=== Example 1: Streaming Responses ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable for streaming example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add backend with streaming support
    manager.create_backend(
        name="openai_stream",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        supports_streaming=True
    )
    
    # Create streaming bot
    streaming_bot = manager.create_bot(
        name="stream_bot",
        backend="openai_stream",
        system_prompt="You are a helpful assistant. Provide detailed, flowing responses."
    )
    
    print("Streaming response:")
    print("User: Tell me a story about AI")
    print("Bot: ", end="", flush=True)
    
    # Get streaming response
    async for chunk in streaming_bot.backend.stream_completion(
        [Message(role=MessageRole.USER, content="Tell me a short story about AI")],
        max_tokens=200
    ):
        if chunk.content:
            print(chunk.content, end="", flush=True)
        
        if chunk.is_final:
            break
    
    print("\n✓ Streaming completed")

async def example_2_function_calling():
    """Example 2: Function calling capabilities"""
    print("\n=== Example 2: Function Calling ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable for function calling example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai_functions",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        supports_functions=True
    )
    
    # Define available functions
    def get_weather(location: str, units: str = "celsius") -> Dict[str, Any]:
        """Get weather information for a location"""
        # Simulate weather API call
        return {
            "location": location,
            "temperature": 22 if units == "celsius" else 72,
            "condition": "sunny",
            "humidity": 65,
            "units": units
        }
    
    def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> Dict[str, Any]:
        """Calculate tip amount"""
        tip_amount = bill_amount * (tip_percentage / 100)
        total = bill_amount + tip_amount
        return {
            "bill_amount": bill_amount,
            "tip_percentage": tip_percentage,
            "tip_amount": round(tip_amount, 2),
            "total_amount": round(total, 2)
        }
    
    # Create function-enabled bot
    function_bot = manager.create_bot(
        name="function_bot",
        backend="openai_functions",
        system_prompt="You are a helpful assistant with access to weather and calculation functions.",
        function_calling_enabled=True,
        available_functions=["get_weather", "calculate_tip"]
    )
    
    # Register functions with the bot's function manager
    function_bot.function_manager.available_functions["get_weather"] = get_weather
    function_bot.function_manager.available_functions["calculate_tip"] = calculate_tip
    
    # Test function calling
    test_messages = [
        "What's the weather like in New York?",
        "Calculate a 18% tip on a $85.50 bill"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        
        # In a real implementation, this would automatically detect and call functions
        # For demo purposes, we'll simulate the function calling process
        if "weather" in message.lower():
            # Simulate function call detection
            function_result = get_weather("New York")
            response_text = f"The weather in New York is {function_result['condition']} with a temperature of {function_result['temperature']}°{function_result['units'][0].upper()} and {function_result['humidity']}% humidity."
        elif "tip" in message.lower():
            function_result = calculate_tip(85.50, 18.0)
            response_text = f"For a bill of ${function_result['bill_amount']}, an {function_result['tip_percentage']}% tip would be ${function_result['tip_amount']}, making the total ${function_result['total_amount']}."
        else:
            response = await function_bot.chat(message)
            response_text = response.content
        
        print(f"Bot: {response_text}")

async def example_3_custom_backend():
    """Example 3: Creating a custom backend"""
    print("\n=== Example 3: Custom Backend ===")
    
    class EchoBackend(BaseBackend):
        """Simple echo backend for demonstration"""
        
        def _get_auth_headers(self) -> Dict[str, str]:
            return {}
        
        def _prepare_messages(self, messages: List[Message]) -> str:
            return messages[-1].content if messages else ""
        
        def _build_request_data(self, messages: List[Message], **kwargs) -> Dict[str, Any]:
            return {"text": self._prepare_messages(messages)}
        
        async def chat_completion(self, messages: List[Message], **kwargs):
            """Echo the user's message with a prefix"""
            from ..core.types import ChatResponse, Usage, FinishReason
            
            user_message = messages[-1].content if messages else "No message"
            echo_response = f"Echo: {user_message}"
            
            return ChatResponse(
                content=echo_response,
                model="echo-v1",
                backend=self.name,
                finish_reason=FinishReason.STOP,
                usage=Usage(
                    prompt_tokens=len(user_message.split()),
                    completion_tokens=len(echo_response.split()),
                    total_tokens=len(user_message.split()) + len(echo_response.split())
                )
            )
    
    # Register custom backend
    from ai_chat_manager.backends import register_backend
    register_backend(
        name="echo",
        backend_class=EchoBackend,
        backend_type=BackendType.CUSTOM,
        description="Simple echo backend for testing",
        features=["chat_completion"]
    )
    
    # Use custom backend
    manager = ChatManager("advanced_config.yaml")
    
    # Create backend config
    echo_config = BackendConfig(
        name="echo",
        backend_type=BackendType.CUSTOM,
        model="echo-v1"
    )
    
    # Add custom backend
    echo_backend = EchoBackend(echo_config)
    manager.backends["echo"] = echo_backend
    
    # Create bot with custom backend
    echo_bot = manager.create_bot(
        name="echo_bot",
        backend="echo",
        system_prompt="You are an echo bot."
    )
    
    # Test custom backend
    test_messages = [
        "Hello, custom backend!",
        "This is a test of the echo functionality",
        "Custom backends are powerful!"
    ]
    
    for message in test_messages:
        response = await echo_bot.chat(message)
        print(f"User: {message}")
        print(f"Echo Bot: {response.content}")

async def example_4_audio_generation():
    """Example 4: Audio generation with ElevenLabs"""
    print("\n=== Example 4: Audio Generation ===")
    
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("⚠️ Set ELEVENLABS_API_KEY environment variable for audio example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add ElevenLabs backend
    manager.create_backend(
        name="elevenlabs",
        backend_type="elevenlabs",
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        model="eleven_monolingual_v1",
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
        save_audio=True,
        audio_output_dir="./audio_output"
    )
    
    # Create TTS bot
    tts_bot = manager.create_bot(
        name="voice_bot",
        backend="elevenlabs",
        system_prompt="You provide text that will be converted to speech."
    )
    
    # Generate speech
    text_to_speak = "Hello! This is an example of text-to-speech generation using ElevenLabs."
    response = await tts_bot.chat(text_to_speak)
    
    print(f"Text: {text_to_speak}")
    print(f"Response: {response.content}")
    
    if hasattr(response, 'metadata') and 'audio_file_path' in response.metadata:
        print(f"Audio saved to: {response.metadata['audio_file_path']}")
    
    print("✓ Audio generation completed")

async def example_5_multi_user_system():
    """Example 5: Multi-user system with user isolation"""
    print("\n=== Example 5: Multi-User System ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable for multi-user example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create shared bot configuration
    manager.create_bot(
        name="personal_assistant",
        backend="openai",
        system_prompt="You are a personal assistant. Remember user-specific information and preferences.",
        memory_enabled=True,
        personalization_enabled=True
    )
    
    # Simulate multiple users
    users = [
        {"id": "user1", "name": "Alice", "preference": "formal communication"},
        {"id": "user2", "name": "Bob", "preference": "casual and brief responses"},
        {"id": "user3", "name": "Charlie", "preference": "detailed explanations with examples"}
    ]
    
    # Each user has isolated conversations
    for user in users:
        print(f"\n--- {user['name']}'s Session ---")
        
        # Get user-specific bot instance
        bot = manager.get_bot("personal_assistant", user_id=user["id"])
        
        # Set user preference
        await bot.chat(f"My name is {user['name']} and I prefer {user['preference']}.")
        
        # Ask the same question to see personalized responses
        response = await bot.chat("Explain the concept of machine learning in one paragraph.")
        print(f"{user['name']}: Explain machine learning")
        print(f"Assistant: {response.content[:100]}...")
        
        # Show user stats
        stats = bot.get_stats()
        print(f"Messages in {user['name']}'s session: {stats['message_count']}")

async def example_6_load_balancing():
    """Example 6: Load balancing across multiple backends"""
    print("\n=== Example 6: Load Balancing ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable for load balancing example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add multiple backend instances for load balancing
    backends = [
        {"name": "openai_1", "weight": 1.0},
        {"name": "openai_2", "weight": 1.0},
        {"name": "openai_3", "weight": 0.5}  # Lower weight = less traffic
    ]
    
    for backend in backends:
        manager.create_backend(
            name=backend["name"],
            backend_type="openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo"
        )
        
        # Add to load balancer with weight
        manager.load_balancer.add_backend(backend["name"], weight=backend["weight"])
    
    # Create bot that uses load balancing
    manager.create_bot(
        name="balanced_bot",
        backend="openai_1",  # Default backend
        system_prompt="You are a load-balanced assistant."
    )
    
    # Simulate requests to show load balancing
    available_backends = [b["name"] for b in backends]
    
    print("Load balancing simulation:")
    for i in range(10):
        # Select backend using load balancer
        selected_backend = manager.load_balancer.select_backend(available_backends)
        print(f"Request {i+1}: Routed to {selected_backend}")
        
        # Simulate response time and success
        import random
        response_time = random.uniform(0.5, 2.0)
        success = random.random() > 0.1  # 90% success rate
        
        # Record metrics
        manager.load_balancer.record_request(selected_backend, success, response_time)
    
    # Show load balancer status
    print("\nLoad Balancer Status:")
    for backend_name in available_backends:
        health = manager.load_balancer.backend_health.get(backend_name)
        if health:
            print(f"{backend_name}: {health.success_rate:.1%} success rate, {health.response_time:.2f}s avg response")

async def example_7_conversation_analytics():
    """Example 7: Advanced conversation analytics"""
    print("\n=== Example 7: Conversation Analytics ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable for analytics example")
        return
    
    manager = ChatManager("advanced_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create analytics-enabled bot
    analytics_bot = manager.create_bot(
        name="analytics_bot",
        backend="openai",
        memory_enabled=True,
        learning_enabled=True,
        personalization_enabled=True
    )
    
    # Simulate a conversation session
    conversation_topics = [
        "Tell me about artificial intelligence",
        "How does machine learning work?",
        "What are neural networks?",
        "Explain deep learning",
        "What's the difference between AI and ML?",
        "Can you give me examples of AI applications?",
        "How is AI used in healthcare?",
        "What are the ethical considerations of AI?",
        "What's the future of artificial intelligence?",
        "Thank you for the informative conversation!"
    ]
    
    print("Simulating conversation for analytics...")
    start_time = datetime.now()
    
    for message in conversation_topics:
        response = await analytics_bot.chat(message)
        # Simulate some processing delay
        await asyncio.sleep(0.1)
    
    end_time = datetime.now()
    
    # Get conversation analytics
    conversation_summary = analytics_bot.conversation_history.get_summary()
    bot_stats = analytics_bot.get_stats()
    
    print(f"\n📊 Conversation Analytics:")
    print(f"Duration: {conversation_summary.duration_minutes:.1f} minutes")
    print(f"Total messages: {conversation_summary.message_count}")
    print(f"Participants: {', '.join(conversation_summary.unique_participants)}")
    print(f"Total tokens used: {bot_stats.get('total_tokens_used', 'N/A')}")
    print(f"Average response time: {bot_stats.get('average_response_time', 0):.2f}s")
    print(f"Total cost: ${bot_stats.get('total_cost', 0):.4f}")
    
    # Topic analysis (simplified)
    all_messages = " ".join([msg.content for msg in analytics_bot.conversation_history.messages])
    ai_terms = ["AI", "artificial intelligence", "machine learning", "neural", "deep learning"]
    topic_counts = {term: all_messages.lower().count(term.lower()) for term in ai_terms}
    
    print(f"\nTopic frequency:")
    for term, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {term}: {count} mentions")

async def example_8_enterprise_features():
    """Example 8: Enterprise features - monitoring, backup, security"""
    print("\n=== Example 8: Enterprise Features ===")
    
    manager = ChatManager("advanced_config.yaml")
    
    # Configure global settings for enterprise use
    from ai_chat_manager.core.config import GlobalConfig
    
    enterprise_config = GlobalConfig(
        log_level="INFO",
        audit_logging=True,
        metrics_enabled=True,
        health_check_enabled=True,
        backup_enabled=True,
        backup_interval_hours=6,
        encryption_enabled=True,
        session_timeout_minutes=30
    )
    
    manager.config.set_global_config(enterprise_config)
    
    # Add monitoring event handlers
    def on_message_processed(bot, message, response):
        """Log message processing for audit"""
        print(f"AUDIT: User message processed by {bot.name} at {datetime.now()}")
    
    def on_error_occurred(error):
        """Log errors for monitoring"""
        print(f"ERROR: {error} at {datetime.now()}")
    
    # Add event handlers
    manager.add_event_handler("message_processed", on_message_processed)
    manager.add_event_handler("error_occurred", on_error_occurred)
    
    # Generate system report
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_status": manager.get_system_status(),
        "detailed_metrics": manager.get_detailed_metrics(),
        "configuration_summary": {
            "total_backends": len(manager.list_backends()),
            "total_bots": len(manager.list_bots()),
            "active_users": len(manager.list_active_users()),
        }
    }
    
    print("📈 Enterprise System Report:")
    print(f"Timestamp: {report['timestamp']}")
    print(f"System uptime: {report['system_status']['system'].get('uptime_hours', 0):.1f} hours")
    print(f"Total backends: {report['configuration_summary']['total_backends']}")
    print(f"Total bots: {report['configuration_summary']['total_bots']}")
    print(f"Active users: {report['configuration_summary']['active_users']}")
    
    # Export system data for backup
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    manager.export_system_data(backup_file)
    print(f"✓ System backup exported to {backup_file}")
    
    # Validate all configurations
    validation_errors = manager.validate_configuration()
    if any(validation_errors.values()):
        print("⚠️ Configuration validation issues found:")
        for section, errors in validation_errors.items():
            if errors:
                print(f"  {section}: {len(errors)} issues")
    else:
        print("✅ All configurations valid")

async def main():
    """Run all advanced examples"""
    print("🚀 AI Chat Manager Advanced Examples")
    print("=" * 60)
    
    # Clean up any existing config
    from pathlib import Path
    config_file = Path("advanced_config.yaml")
    if config_file.exists():
        config_file.unlink()
    
    examples = [
        example_1_streaming_responses,
        example_2_function_calling,
        example_3_custom_backend,
        example_4_audio_generation,
        example_5_multi_user_system,
        example_6_load_balancing,
        example_7_conversation_analytics,
        example_8_enterprise_features,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            await example()
        except Exception as e:
            print(f"\n❌ Advanced Example {i} failed: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(examples):
            print("\n" + "-" * 60)
    
    print("\n✅ Advanced examples completed!")

if __name__ == "__main__":
    asyncio.run(main())