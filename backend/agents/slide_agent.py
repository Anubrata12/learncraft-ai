import os
from dotenv import load_dotenv

from google.adk import Agent
from tools.slide_tool import generate_structured_script, generate_slides_from_sections
import os

load_dotenv()

INSTRUCTIONS = """ 
You are a slide generation agent.
Your job:
1. You receive a script as input and the topic name.
2. Parse the script into sections (title + content). 
3. For each section, create slides using `generate_slides_from_sections(sections, topic)`.
4. Return ONLY the absolute file paths of the generated slides in a list format.
"""

slide_agent = Agent(
    name="slideAgent",
    description="Generates presentation slides from a structured script.",
    model=os.getenv("MODEL_TEXT"),
    instruction=INSTRUCTIONS,
    tools=[generate_slides_from_sections],  # topic will be passed dynamically by orchestrator
    output_key="slide_paths"
)
