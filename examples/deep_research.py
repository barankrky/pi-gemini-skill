#!/usr/bin/env python3
"""Deep research workflow example."""
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
        # Check if account has deep research access
        status = await client.inspect_account_status()
        print("Account status:", status.get("summary"))
        
        if not status.get("summary", {}).get("deep_research_feature_present"):
            print("Deep research not available for this account")
            return
        
        # Full research workflow
        print("Starting deep research on 'Impact of renewable energy on global economy'...")
        
        # Create plan first (optional - let you review/confirm)
        plan = await client.create_deep_research_plan(
            "Impact of renewable energy on global economy 2024-2030"
        )
        print(f"Plan title: {plan.title}")
        print(f"Research ID: {plan.research_id}")
        print("Steps:", [s.title for s in plan.steps])
        
        # Continue with the plan
        result = await client.deep_research(
            "Impact of renewable energy on global economy 2024-2030",
            poll_interval=15,
            timeout=300
        )
        
        if result.done and result.final_output:
            print("\n=== Research Complete ===")
            print(result.final_output.text[:2000])
        else:
            print("Research timed out or incomplete")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())