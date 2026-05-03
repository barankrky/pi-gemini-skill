# pi-gemini-skill

A pi skill that provides Google Gemini integration for AI agents. Supports chat, streaming, file uploads, image generation, video/audio creation, and deep research workflows.

## Features

- **Chat & Streaming** - Interactive conversations with Gemini models
- **File Upload** - Attach images and documents for context
- **Image Generation** - Generate and edit images with Gemini
- **Deep Research** - Full research workflow with status polling
- **Chat Sessions** - Multi-turn conversations with history
- **Environment Variable Auth** - Simple cookie-based authentication

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/pi-gemini-skill.git
cd pi-gemini-skill

# Install dependencies
pip install gemini-webapi

# Optional: browser cookie auto-import
pip install gemini-webapi[browser]
```

## Setup Authentication

Set environment variables with your Gemini cookies:

```bash
export GEMINI_1PSID="your__Secure-1PSID_value"
export GEMINI_1PSIDTS="your__Secure-1PSIDTS_value"  # Optional
```

Find your cookies at https://gemini.google.com → F12 → Network tab → refresh → copy cookie values.

## Usage

### With pi

```
/skill:pi-gemini-skill
```

### Direct Python

```python
import asyncio
from gemini_helper import GeminiSkill

async def main():
    async with GeminiSkill() as g:
        response = await g.chat("What is quantum computing?")
        print(response.text)
        
        # Use flash model
        response = await g.chat("Explain AI", model="flash")
        print(response.text)

asyncio.run(main())
```

### Run Examples

```bash
python examples/basic_chat.py
python examples/streaming_chat.py
python examples/deep_research.py
```

## Repository Structure

```
pi-gemini-skill/
├── SKILL.md              # Pi skill definition
├── gemini_helper.py      # Helper module
├── examples/             # Usage examples
├── scripts/              # Helper scripts
└── README.md             # This file
```

## Requirements

- Python 3.10+
- gemini-webapi library
- Google Gemini account with cookies

## License

MIT