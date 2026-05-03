#!/usr/bin/env python3
"""Helper module for Gemini API integration with pi agents."""
import asyncio
import os
from typing import Optional, List, Any
from contextlib import asynccontextmanager
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model
from gemini_webapi.exceptions import GeminiError


class GeminiSkill:
    """
    Wrapper class for Gemini API with environment variable authentication.
    
    Usage:
        async with GeminiSkill() as gemini:
            response = await gemini.chat("Hello")
    """
    
    def __init__(
        self,
        secure_1psid: Optional[str] = None,
        secure_1psidts: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """Initialize with optional cookie values (defaults to env vars)."""
        self._secure_1psid = secure_1psid or os.getenv("GEMINI_1PSID")
        self._secure_1psidts = secure_1psidts or os.getenv("GEMINI_1PSIDTS")
        self._proxy = proxy
        self.client: Optional[GeminiClient] = None
    
    async def __aenter__(self):
        self.client = GeminiClient(
            secure_1psid=self._secure_1psid,
            secure_1psidts=self._secure_1psidts,
            proxy=self._proxy,
        )
        await self.client.init()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.close()
        return False
    
    async def chat(
        self,
        prompt: str,
        files: Optional[List[Any]] = None,
        model: str = "unspecified",
        stream: bool = False,
    ):
        """Generate a chat response."""
        if not self.client:
            raise RuntimeError("Client not initialized - use async context manager")
        
        model_enum = {
            "flash": Model.GEMINI_FLASH,
            "pro": Model.GEMINI_PRO,
        }.get(model.lower(), Model.UNSPECIFIED)
        
        if stream:
            return self.client.generate_content_stream(prompt, files=files, model=model_enum)
        return await self.client.generate_content(prompt, files=files, model=model_enum)
    
    async def analyze_image(self, prompt: str, image_path: str):
        """Analyze an image with Gemini."""
        return await self.chat(f"{prompt}\n\n[Image attached]", files=[image_path])
    
    async def create_research(self, topic: str, timeout: int = 300):
        """Run deep research on a topic."""
        if not self.client:
            raise RuntimeError("Client not initialized - use async context manager")
        
        status = await self.client.inspect_account_status()
        if not status.get("summary", {}).get("deep_research_feature_present"):
            raise GeminiError("Deep research not available for this account")
        
        return await self.client.deep_research(topic, timeout=timeout)
    
    def list_chats(self):
        """List recent conversations."""
        if not self.client:
            raise RuntimeError("Client not initialized")
        return self.client.list_chats()
    
    async def continue_chat(self, cid: str, prompt: str):
        """Continue a previous conversation."""
        if not self.client:
            raise RuntimeError("Client not initialized")
        
        history = await self.client.read_chat(cid)
        if not history:
            raise ValueError(f"Could not read chat {cid}")
        
        chat = self.client.start_chat(metadata=history.metadata)
        return await chat.send_message(prompt)


# Convenience function for quick use
async def quick_chat(prompt: str, **kwargs) -> str:
    """Quick one-shot chat without context manager."""
    async with GeminiSkill() as gemini:
        result = await gemini.chat(prompt, **kwargs)
        return result.text


if __name__ == "__main__":
    # Demo usage
    async def demo():
        async with GeminiSkill() as g:
            print("Testing Gemini API integration...")
            
            # Basic chat
            resp = await g.chat("Explain quantum computing in one sentence")
            print("Response:", resp.text)
            
    asyncio.run(demo())