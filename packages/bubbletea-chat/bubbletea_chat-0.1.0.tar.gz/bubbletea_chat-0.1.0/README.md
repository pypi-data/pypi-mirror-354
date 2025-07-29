# BubbleTea Python SDK (Minimal)

Build AI chatbots for the BubbleTea platform with simple Python functions.

**Note**: This is the minimal version without LLM and CLI support. For the full-featured version with AI capabilities, see the complete package.

## Installation

```bash
pip install bubbletea
```

## Quick Start

Create a simple chatbot in `my_bot.py`:

```python
import bubbletea as bt

@bt.chatbot
def my_chatbot(message: str):
    # Your bot logic here
    if "image" in message.lower():
        yield bt.Image("https://picsum.photos/400/300")
        yield bt.Text("Here's a random image for you!")
    else:
        yield bt.Text(f"You said: {message}")
```

Run it locally:

```bash
python my_bot.py
```

## Features

### 📦 Components

BubbleTea supports rich components for building engaging chatbot experiences:

- **Text**: Plain text messages
- **Image**: Images with optional alt text  
- **Markdown**: Rich formatted text

### 🔄 Streaming Support

BubbleTea automatically detects generator functions and streams responses:

```python
@bt.chatbot
async def streaming_bot(message: str):
    yield bt.Text("Processing your request...")
    
    # Simulate some async work
    import asyncio
    await asyncio.sleep(1)
    
    yield bt.Markdown("## Here's your response")
    yield bt.Image("https://example.com/image.jpg")
    yield bt.Text("All done!")
```

## Examples

### Simple Echo Bot

```python
import bubbletea as bt

@bt.chatbot
def echo_bot(message: str):
    return bt.Text(f"Echo: {message}")
```

### Multi-Modal Bot

```python
import bubbletea as bt

@bt.chatbot
def multimodal_bot(message: str):
    yield bt.Markdown("# Welcome to the Multi-Modal Bot!")
    
    yield bt.Text("I can show you different types of content:")
    
    yield bt.Markdown("""
    - 📝 **Text** messages
    - 🖼️ **Images** with descriptions  
    - 📊 **Markdown** formatting
    """)
    
    yield bt.Image(
        "https://picsum.photos/400/300",
        alt="A random beautiful image"
    )
    
    yield bt.Text("Pretty cool, right? 😎")
```

### Streaming Bot

```python
import bubbletea as bt
import asyncio

@bt.chatbot
async def streaming_bot(message: str):
    yield bt.Text("Hello! Let me process your message...")
    await asyncio.sleep(1)
    
    words = message.split()
    yield bt.Text("You said: ")
    for word in words:
        yield bt.Text(f"{word} ")
        await asyncio.sleep(0.3)
    
    yield bt.Markdown("## Analysis Complete!")
```

## API Reference

### Decorators

- `@bt.chatbot` - Create a chatbot from a function
- `@bt.chatbot(name="custom-name")` - Set a custom bot name
- `@bt.chatbot(stream=False)` - Force non-streaming mode

### Components

- `bt.Text(content: str)` - Plain text message
- `bt.Image(url: str, alt: str = None)` - Image component
- `bt.Markdown(content: str)` - Markdown formatted text

### Server

- `bt.run_server(chatbot, port=8000, host="0.0.0.0")` - Run a chatbot server

## Testing Your Bot

Start your bot:

```bash
python my_bot.py
```

Test with curl:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "message": "Hello bot!"}'
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.