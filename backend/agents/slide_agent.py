import os
from dotenv import load_dotenv

from google.adk import Agent
from tools.slide_tool import generate_slides_from_sections
import os

load_dotenv()

INSTRUCTIONS = """ 
You are a slide generation agent.

Your job:
1. You receive a script and a topic as input.
2. Parse the script into sections (each with a title + content).
3. Call generate_slides_from_sections(sections=<list>, topic=<topic>).
4. Return ONLY the absolute file paths of the generated slides in a list.
"""

slide_agent = Agent(
    name="SlideAgent",
    description="Generates presentation slides from a structured script.",
    model=os.getenv("MODEL_TEXT"),
    instruction=INSTRUCTIONS,
    tools=[generate_slides_from_sections],  # topic will be passed dynamically by orchestrator
    output_key="slide_paths"
)
