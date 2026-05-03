#!/usr/bin/env python3
"""Streaming Gemini chat example."""
import asyncio
import os
from gemini_webapi import GeminiClient

async def main():
    client = GeminiClient(
        secure_1psid=os.getenv("GEMINI_1PSID"),
        secure_1psidts=os.getenv("GEMINI_1PSIDTS"),
    )
    await client.init(verbose=True)
    
    try:
        print("Streaming response: ", end="", flush=True)
        async for output in client.generate_content_stream(
            "Write a short story about a robot learning to paint"
        ):
            print(output.text_delta, end="", flush=True)
        print("\n")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())