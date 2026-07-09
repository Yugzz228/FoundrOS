"""Entrypoint for the FoundrOS Prototype."""

import os
import sys
import logging
from dotenv import load_dotenv
from foundros.models.idea import StartupIdea
from foundros.services.llm import LLMService
from foundros.orchestrator.runner import Orchestrator

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    
    # Check for API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY environment variable not found. LLM calls will fail unless using a mock service or a local provider that doesn't require a key.")
    
    print("Welcome to FoundrOS v1.0 Prototype")
    print("----------------------------------")
    title = input("Enter Startup Title: ")
    industry = input("Enter Industry: ")
    description = input("Enter Startup Description: ")
    
    idea = StartupIdea(
        title=title,
        industry=industry,
        description=description
    )
    
    # Initialize services
    llm_service = LLMService(api_key=api_key)
    orchestrator = Orchestrator(llm_service=llm_service)
    
    print("\n[Running Simulation...]\n")
    report = orchestrator.run(idea)
    
    # Save the report
    output_file = "final_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\n[Simulation Complete] Report saved to {output_file}")

if __name__ == "__main__":
    main()
