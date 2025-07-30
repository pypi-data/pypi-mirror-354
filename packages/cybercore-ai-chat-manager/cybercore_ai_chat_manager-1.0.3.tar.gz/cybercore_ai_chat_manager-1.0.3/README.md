# AI Chat Manager

A comprehensive Python package for managing AI-powered chat conversations with support for multiple backends, enhanced features, and extensible architecture.

## Features

- **Multiple AI Backends**: Support for OpenAI, Venice AI, HuggingFace, ElevenLabs, and more
- **Streaming Support**: Real-time streaming responses
- **Function Calling**: Advanced function calling capabilities
- **Vision Support**: Image understanding with compatible models
- **Audio Generation**: Text-to-speech with ElevenLabs
- **Conversation Management**: Persistent conversation history with smart context handling
- **Rate Limiting**: Built-in rate limiting and retry logic
- **Error Handling**: Comprehensive error handling and conversion
- **CLI Interface**: Easy-to-use command line interface
- **Extensible**: Plugin architecture for adding new backends

## Installation

```bash
pip install cybercore-ai-chat-manager
```

## Quick Start

```python
from ai_chat_manager import ChatManager, Config
from ai_chat_manager.backends import OpenAIBackend

# Create configuration
config = Config()
config.add_backend("openai", {
    "api_key": "your-openai-api-key",
    "model": "gpt-3.5-turbo"
})

# Create chat manager
manager = ChatManager(config)

# Start a conversation
response = await manager.chat("Hello, how are you?", backend="openai")
print(response.content)
```

## Project Structure

```
ai_chat_manager/
├── __init__.py                  # Main package init
├── core/
│   ├── __init__.py
│   ├── types.py                 # Core type definitions
│   ├── exceptions.py            # Exception definitions
│   ├── config.py                # Configuration management
│   ├── bot.py                   # Bot implementation
│   └── manager.py               # Chat manager
├── backends/
│   ├── __init__.py              # Backend registry
│   ├── base.py                  # Base backend class
│   ├── openai_backend.py
│   ├── venice_backend.py
│   ├── huggingface_backend.py
│   └── elevenlabs_backend.py
├── cli/
│   ├── __init__.py
│   ├── main.py                  # Main CLI
│   └── wrapper.py               # CLI wrapper
├── utils/
│   ├── __init__.py
│   └── helpers.py               # Utility functions
└── examples/
    ├── basic.py
    └── advanced.py
```

## Backend Support

### OpenAI
- GPT-3.5, GPT-4, and all variants
- Function calling
- Vision support (GPT-4V)
- Streaming responses

### Venice AI
- Privacy-focused AI platform
- Anonymous and censorship-resistant
- OpenAI-compatible API
- Enhanced privacy controls

### HuggingFace
- Inference API support
- Local model support
- Wide variety of open-source models
- Custom model hosting

### ElevenLabs
- High-quality text-to-speech
- Voice cloning
- Multiple voice models
- Streaming audio generation

## Configuration

The package uses a comprehensive configuration system:

```python
from ai_chat_manager.core.config import Config, BackendConfig

config = Config()

# Add OpenAI backend
openai_config = BackendConfig(
    name="openai",
    backend_type="openai",
    api_key="your-api-key",
    model="gpt-4",
    max_tokens=2000,
    temperature=0.7
)
config.add_backend_config(openai_config)
```

## Error Handling

The package provides comprehensive error handling:

```python
from ai_chat_manager.core.exceptions import (
    BackendError, AuthenticationError, RateLimitError,
    ModelNotFoundError, QuotaExceededError
)

try:
    response = await manager.chat("Hello")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded")
except BackendError as e:
    print(f"Backend error: {e}")
```

## CLI Usage

```bash
# Initialize configuration
ai-chat-manager init

# Basic commands (all three work identically)
ai-chat-manager --help
acm --help
chat-manager --help

# Backend management
ai-chat-manager backend add openai
ai-chat-manager backend list

# Bot management
ai-chat-manager bot create assistant
ai-chat-manager bot list

# Start chatting
ai-chat-manager chat assistant

# System status
ai-chat-manager status
ai-chat-manager doctor
```

## Examples

See the `examples/` directory for more detailed usage examples:

- `basic.py`: Simple chat interactions
- `advanced.py`: Advanced features like function calling, streaming, and conversation management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Support for OpenAI, Venice AI, HuggingFace, and ElevenLabs
- Comprehensive configuration system
- CLI interface with three command aliases: `ai-chat-manager`, `acm`, `chat-manager`
- Error handling and retry logic
- Conversation management
- Streaming support
- Function calling
