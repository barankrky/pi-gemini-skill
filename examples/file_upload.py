#!/usr/bin/env python3
"""File upload and multi-modal input example."""
import asyncio
import os
from gemini_webapi import GeminiClient

async def main():
    client = GeminiClient(
        secure_1psid=os.getenv("GEMINI_1PSID"),
        secure_1psidts=os.getenv("GEMINI_1PSIDTS"),
    )
    await client.init()
    
    try:
        # Upload files for context
        # Replace with actual file paths
        files = []
        for filepath in files:
            if os.path.exists(filepath):
                response = await client.generate_content(
                    "Analyze this file and summarize its contents",
                    files=[filepath]
                )
                print(f"\n{filepath}:")
                print(response.text)
        
        # Image-specific prompt
        # response = await client.generate_content(
        #     "What do you see in this image?",
        #     files=["/path/to/image.jpg"]
        # )
        # print(response.text)
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())