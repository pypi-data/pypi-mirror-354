"""
Basic Usage Examples for AI Chat Manager

This file demonstrates basic usage patterns and common scenarios
for getting started with the AI Chat Manager.
"""

import asyncio
import os
from pathlib import Path

# Import the AI Chat Manager
from ai_chat_manager import ChatManager, create_chat_manager
from ai_chat_manager.core.config import BackendConfig, BotConfig
from ai_chat_manager.backends import create_openai_backend, create_venice_backend

async def example_1_basic_setup():
    """Example 1: Basic setup and first conversation"""
    print("=== Example 1: Basic Setup ===")
    
    # Create a chat manager with default configuration
    manager = ChatManager("examples_config.yaml")
    
    # Add an OpenAI backend (you'll need to set your API key)
    if os.getenv("OPENAI_API_KEY"):
        manager.create_backend(
            name="openai",
            backend_type="openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo"
        )
        
        # Create a simple assistant bot
        assistant = manager.create_bot(
            name="assistant",
            backend="openai",
            system_prompt="You are a helpful AI assistant. Be concise and friendly.",
            memory_enabled=True
        )
        
        # Have a conversation
        response = await manager.chat_with_bot("assistant", "Hello! What can you help me with?")
        print(f"Assistant: {response}")
        
        response = await manager.chat_with_bot("assistant", "Tell me a short joke")
        print(f"Assistant: {response}")
        
    else:
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")

async def example_2_multiple_backends():
    """Example 2: Using multiple backends"""
    print("\n=== Example 2: Multiple Backends ===")
    
    # Create manager
    manager = ChatManager("examples_config.yaml")
    
    # Add multiple backends
    backends_added = []
    
    if os.getenv("OPENAI_API_KEY"):
        manager.create_backend(
            name="openai",
            backend_type="openai", 
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo"
        )
        backends_added.append("openai")
    
    if os.getenv("VENICE_API_KEY"):
        manager.create_backend(
            name="venice",
            backend_type="venice",
            api_key=os.getenv("VENICE_API_KEY"),
            privacy_level="enhanced"
        )
        backends_added.append("venice")
    
    if os.getenv("HUGGINGFACE_API_KEY"):
        manager.create_backend(
            name="huggingface",
            backend_type="huggingface",
            api_key=os.getenv("HUGGINGFACE_API_KEY"),
            model="microsoft/DialoGPT-large"
        )
        backends_added.append("huggingface")
    
    print(f"Added backends: {backends_added}")
    
    # Create different bots for different purposes
    for backend in backends_added:
        bot_name = f"{backend}_assistant"
        manager.create_bot(
            name=bot_name,
            backend=backend,
            system_prompt=f"You are an AI assistant powered by {backend}. Be helpful and mention your backend.",
            personality="helpful"
        )
        
        # Test each bot
        response = await manager.chat_with_bot(bot_name, "Introduce yourself briefly")
        print(f"{bot_name}: {response}")

async def example_3_bot_templates():
    """Example 3: Using bot templates"""
    print("\n=== Example 3: Bot Templates ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    manager = ChatManager("examples_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create bots from templates
    templates = ["assistant", "creative", "researcher", "teacher"]
    
    for template in templates:
        bot = manager.create_bot_from_template(
            name=f"{template}_bot",
            template=template,
            backend="openai"
        )
        
        # Test each template
        test_message = {
            "assistant": "Help me plan my day",
            "creative": "Write a haiku about programming",
            "researcher": "Explain quantum computing",
            "teacher": "Teach me basic calculus"
        }
        
        response = await bot.chat(test_message[template])
        print(f"\n{template.title()} Bot:")
        print(f"User: {test_message[template]}")
        print(f"Bot: {response.content}")

async def example_4_conversation_memory():
    """Example 4: Conversation memory and context"""
    print("\n=== Example 4: Conversation Memory ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    manager = ChatManager("examples_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create bot with memory enabled
    memory_bot = manager.create_bot(
        name="memory_bot",
        backend="openai",
        system_prompt="You are a helpful assistant with perfect memory. Remember details from our conversation.",
        memory_enabled=True,
        max_context_length=8000
    )
    
    # Have a conversation that builds context
    conversation = [
        "My name is Alice and I'm learning Python programming.",
        "What's a good way to start learning?",
        "I'm particularly interested in data science applications.",
        "Can you recommend some libraries for data analysis?",
        "What did I say my name was earlier?"  # Test memory
    ]
    
    for message in conversation:
        response = await manager.chat_with_bot("memory_bot", message)
        print(f"\nUser: {message}")
        print(f"Bot: {response}")

async def example_5_user_sessions():
    """Example 5: User sessions and personalization"""
    print("\n=== Example 5: User Sessions ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    manager = ChatManager("examples_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create bot with personalization
    personal_bot = manager.create_bot(
        name="personal_assistant",
        backend="openai",
        system_prompt="You are a personal assistant. Remember user preferences and adapt your responses.",
        memory_enabled=True,
        personalization_enabled=True,
        learning_enabled=True
    )
    
    # Simulate different users
    users = ["alice", "bob", "charlie"]
    
    for user_id in users:
        print(f"\n--- Conversation with {user_id} ---")
        
        # Each user has their own conversation context
        bot = manager.get_bot("personal_assistant", user_id=user_id)
        
        # User-specific messages
        user_messages = {
            "alice": "I prefer formal communication and detailed explanations.",
            "bob": "Keep it casual and brief, I'm always in a hurry.",
            "charlie": "I love creative analogies and examples in explanations."
        }
        
        # Set user preference
        response = await bot.chat(user_messages[user_id])
        print(f"{user_id}: {user_messages[user_id]}")
        print(f"Bot: {response.content}")
        
        # Ask the same question to see personalized responses
        question = "Explain how machine learning works"
        response = await bot.chat(question)
        print(f"\n{user_id}: {question}")
        print(f"Bot: {response.content[:150]}...")

async def example_6_error_handling():
    """Example 6: Error handling and resilience"""
    print("\n=== Example 6: Error Handling ===")
    
    manager = ChatManager("examples_config.yaml")
    
    # Try to use a non-existent backend
    try:
        manager.create_bot("test_bot", "nonexistent_backend")
    except Exception as e:
        print(f"✓ Caught expected error: {e}")
    
    # Try to chat with non-existent bot
    try:
        await manager.chat_with_bot("nonexistent_bot", "Hello")
    except Exception as e:
        print(f"✓ Caught expected error: {e}")
    
    # Try with invalid API key
    try:
        manager.create_backend(
            name="bad_openai",
            backend_type="openai",
            api_key="invalid_key",
            model="gpt-3.5-turbo"
        )
        
        manager.create_bot("bad_bot", "bad_openai")
        await manager.chat_with_bot("bad_bot", "Hello")
        
    except Exception as e:
        print(f"✓ Caught authentication error: {e}")

async def example_7_system_monitoring():
    """Example 7: System monitoring and metrics"""
    print("\n=== Example 7: System Monitoring ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    manager = ChatManager("examples_config.yaml")
    
    # Add backend
    manager.create_backend(
        name="openai",
        backend_type="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create bot
    manager.create_bot("monitor_bot", "openai")
    
    # Have some conversations to generate metrics
    messages = [
        "Hello, how are you?",
        "What's the weather like?",
        "Tell me about artificial intelligence",
        "Can you help me with Python?",
        "What's your favorite color?"
    ]
    
    for message in messages:
        await manager.chat_with_bot("monitor_bot", message)
    
    # Get system status
    status = manager.get_system_status()
    print(f"System Status:")
    print(f"- Total Requests: {status['system'].get('total_requests', 0)}")
    print(f"- Success Rate: {status['system'].get('success_rate', 0)*100:.1f}%")
    print(f"- Active Bots: {status['system'].get('active_bots', 0)}")
    print(f"- Active Users: {status['system'].get('active_users', 0)}")
    
    # Get detailed metrics
    detailed_metrics = manager.get_detailed_metrics()
    print(f"\nDetailed Metrics:")
    print(f"- Average Response Time: {detailed_metrics['system_metrics'].get('average_response_time', 0):.2f}s")
    print(f"- Total Tokens: {detailed_metrics['system_metrics'].get('total_tokens', 0):,}")
    print(f"- Total Cost: ${detailed_metrics['system_metrics'].get('total_cost', 0):.4f}")

async def example_8_factory_pattern():
    """Example 8: Using factory functions for quick setup"""
    print("\n=== Example 8: Factory Pattern ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    # Use the factory function for quick setup
    manager = create_chat_manager(
        config_path="examples_config.yaml",
        backends={
            "openai": {
                "type": "openai",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-3.5-turbo"
            }
        },
        bots={
            "quick_assistant": {
                "backend": "openai",
                "template": "assistant"
            },
            "creative_writer": {
                "backend": "openai", 
                "template": "creative",
                "learning_enabled": True
            }
        }
    )
    
    # Test the bots
    response1 = await manager.chat_with_bot("quick_assistant", "What can you help me with?")
    print(f"Quick Assistant: {response1}")
    
    response2 = await manager.chat_with_bot("creative_writer", "Write a short story about a robot")
    print(f"\nCreative Writer: {response2}")

async def example_9_cleanup_and_context():
    """Example 9: Proper cleanup and context management"""
    print("\n=== Example 9: Cleanup and Context Management ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Set OPENAI_API_KEY environment variable to run this example")
        return
    
    # Use async context manager for proper cleanup
    async with ChatManager("examples_config.yaml") as manager:
        # Setup
        manager.create_backend(
            name="openai",
            backend_type="openai",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create bot with context manager
        async with manager.get_bot("assistant", user_id="demo_user") as bot:
            response = await bot.chat("Hello! This is a context-managed conversation.")
            print(f"Bot: {response.content}")
            
            # Bot state will be automatically saved when exiting context
        
        print("✓ Bot context closed and state saved")
    
    print("✓ Manager context closed and cleanup completed")

async def main():
    """Run all examples"""
    print("🚀 AI Chat Manager Examples")
    print("=" * 50)
    
    # Clean up any existing config from previous runs
    config_file = Path("examples_config.yaml")
    if config_file.exists():
        config_file.unlink()
    
    examples = [
        example_1_basic_setup,
        example_2_multiple_backends,
        example_3_bot_templates,
        example_4_conversation_memory,
        example_5_user_sessions,
        example_6_error_handling,
        example_7_system_monitoring,
        example_8_factory_pattern,
        example_9_cleanup_and_context,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            await example()
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}")
        
        if i < len(examples):
            print("\n" + "-" * 50)
    
    print("\n✅ Examples completed!")

if __name__ == "__main__":
    # Set up environment variables with dummy values for demo
    # In real usage, set these to your actual API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("💡 Tip: Set environment variables for full examples:")
        print("   export OPENAI_API_KEY='your-openai-key'")
        print("   export VENICE_API_KEY='your-venice-key'")
        print("   export HUGGINGFACE_API_KEY='your-hf-key'")
        print("   export ELEVENLABS_API_KEY='your-elevenlabs-key'")
        print()
    
    asyncio.run(main())