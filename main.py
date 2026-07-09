"""Entrypoint for the FoundrOS V2 Architecture."""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from foundros.models.idea import StartupIdea
from foundros.services.llm import AsyncLLMService
from foundros.orchestrator.runner import Orchestrator

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_simulation():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found. Ensure mock/local service if testing.")
    
    print("Welcome to FoundrOS v2.0")
    print("------------------------")
    title = input("Enter Startup Title: ")
    industry = input("Enter Industry: ")
    description = input("Enter Startup Description: ")
    
    idea = StartupIdea(
        title=title,
        industry=industry,
        description=description
    )
    
    llm_service = AsyncLLMService(api_key=api_key)
    orchestrator = Orchestrator(llm_service=llm_service)
    
    print("\n[Running Async Event-Driven Simulation...]\n")
    report = await orchestrator.run(idea)
    
    output_file = "final_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\n[Simulation Complete] Report saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
