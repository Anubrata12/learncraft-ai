from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from tools.slide_tool import generate_structured_script, generate_slides_from_sections


INSTRUCTIONS = """ 
You are a slide generation agent.
Your job:
1. You receive a script as input.
2. Parse the script into sections, each section contains a title and content. 
3. For each section, create a slide with the title and content with help of generate_slides_from_sections to /app/data/slides/algebra.
4. Return ONLY the absolute file paths of the generated slides in a list format.
"""

slide_agent = Agent(
    name = "slideAgent",
    description = "Generates presentation slides from a structured script.",
    model = Gemini(model = "gemini-2.5-flash-lite"),
    instruction= INSTRUCTIONS,
    tools = [generate_slides_from_sections],
    output_key = "slide_paths"
)