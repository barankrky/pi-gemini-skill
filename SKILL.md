---
name: gemini-api
description: Google Gemini web API integration for AI agents. Provides chat, streaming, file upload, image generation, and deep research capabilities via reverse-engineered Gemini web client.
license: MIT
---

# Gemini API Skill

A pi skill for interacting with Google Gemini through the web API. Supports chat, streaming, file attachments, image generation, video/audio creation, and deep research workflows.

## Setup

### Install Dependencies

```bash
pip install gemini-webapi
# Optional: for browser cookie auto-import
pip install gemini-webapi[browser]
```

### Authentication via Environment Variables

Set your Google Gemini cookies as environment variables:

```bash
# Required cookies from gemini.google.com
export GEMINI_1PSID="your__Secure-1PSID_value"
export GEMINI_1PSIDTS="your__Secure-1PSIDTS_value"  # Optional for some accounts

# Optional: Cookie cache path (for persistent sessions)
export GEMINI_COOKIE_PATH="/tmp/gemini_cookies"
```

### Find Your Cookies

1. Go to https://gemini.google.com and log in
2. Press F12 → Network tab → refresh the page
3. Click any request and copy the cookie values for:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS` (if present)

## Usage

### Initialize Client

```python
import asyncio
import os
from gemini_webapi import GeminiClient

async def main():
    # From environment variables (manual method)
    client = GeminiClient(
        secure_1psid=os.getenv("GEMINI_1PSID"),
        secure_1psidts=os.getenv("GEMINI_1PSIDTS"),
    )
    await client.init()
    
    # Or auto-import from browser (requires gemini-webapi[browser])
    # client = GeminiClient()
    # await client.init()
```

### Basic Chat

```python
output = await client.generate_content("What is quantum computing?")
print(output.text)
```

### Streaming Response

```python
async for output in client.generate_content_stream("Explain relativity"):
    print(output.text_delta, end="", flush=True)
```

### Chat Session (Multi-turn)

```python
chat = client.start_chat()
response1 = await chat.send_message("My name is Alice")
response2 = await chat.send_message("What's my name?")
print(response2.text)  # References "Alice"
```

### File Upload

```python
# Attach files to context
output = await client.generate_content(
    "Describe this image",
    files=["/path/to/image.png", "/path/to/document.pdf"]
)
```

### Continue Previous Conversation

```python
# Read existing chat by ID
history = await client.read_chat("c_xxxxxxxxxxxx")

# Continue from it
chat = client.start_chat(metadata=history.metadata)
response = await chat.send_message("Follow up question")
```

### Image Generation

```python
output = await client.generate_content(
    "A futuristic city at sunset, cyberpunk style",
    model="gemini-2.0-flash-exp-image-generation"
)
for img in output.generated_images:
    img.save("output.png")
```

### Deep Research

```python
# Full research workflow
result = await client.deep_research("Impact of AI on healthcare 2024-2030")
print(result.final_output.text)
```

Or step-by-step:

```python
# 1. Create plan
plan = await client.create_deep_research_plan("Climate change solutions")

# 2. Start research
start_output = await client.start_deep_research(plan)

# 3. Wait for completion
result = await client.wait_for_deep_research(plan, timeout=300)
```

## Examples

Run the example scripts:

```bash
# Basic chat
python examples/basic_chat.py

# Streaming demo
python examples/streaming_chat.py

# File upload
python examples/file_upload.py

# Deep research
python examples/deep_research.py
```

## API Reference

### Client Methods

| Method | Description |
|--------|-------------|
| `init()` | Initialize client and get access token |
| `close()` | Close client and save cookies |
| `generate_content(prompt, files, model, ...)` | Generate response |
| `generate_content_stream(...)` | Stream response |
| `start_chat(metadata, cid)` | Start chat session |
| `list_chats()` | List recent conversations |
| `read_chat(cid)` | Read conversation history |
| `delete_chat(cid)` | Delete conversation |
| `list_models()` | List available models |
| `deep_research(prompt)` | Full research cycle |

### Model Options

- `Model.UNSPECIFIED` - Default model
- `"gemini-2.0-flash"` - Fast model
- `"gemini-2.0-pro"` - Pro model
- `"gemini-2.0-flash-exp-image-generation"` - Image generation

### Output Types

```python
# ModelOutput attributes
output.text                          # Response text
output.candidates                    # List of Candidate objects
output.thoughts                      # Gemini's chain of thought
output.generated_images              # GeneratedImage objects
output.generated_videos              # GeneratedVideo objects
output.generated_media               # Audio/Media objects
output.deep_research_plan            # DeepResearchPlan (if enabled)
```

## Error Handling

```python
from gemini_webapi.exceptions import (
    APIError, AuthError, GeminiError,
    UsageLimitExceeded, TemporarilyBlocked
)

try:
    output = await client.generate_content(prompt)
except AuthError:
    print("Invalid cookies - re-authenticate")
except UsageLimitExceeded:
    print("Rate limit hit - wait and retry")
except TemporarilyBlocked:
    print("IP blocked - try different network/proxy")
```

## Notes

- Client auto-refreshes cookies every 10 minutes by default
- Set `GEMINI_COOKIE_PATH` to persist cookies across restarts
- Some accounts may not have `__Secure-1PSIDTS` - try without it
- Deep research requires eligible account (not all accounts have access)