#!/usr/bin/env python3
"""Basic Gemini chat example."""
import asyncio
import os
from gemini_webapi import GeminiClient

async def main():
    # Initialize client from env vars
    client = GeminiClient(
        secure_1psid=os.getenv("GEMINI_1PSID"),
        secure_1psidts=os.getenv("GEMINI_1PSIDTS"),
    )
    await client.init()
    
    try:
        # Simple question
        response = await client.generate_content(
            "What are the key differences between Python and JavaScript?"
        )
        print("Response:", response.text)
        
        # List available models
        models = client.list_models()
        print(f"\nAvailable models: {[m.model_name for m in models or []]}")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())