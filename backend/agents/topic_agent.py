import os
from dotenv import load_dotenv
from google.adk import Agent

load_dotenv()

INSTRUCTIONS = """
You are a Topic Extraction Agent.

Task:
- Receive user input text (educational request).
- Extract a **maximum of 2 words** summarizing the main topic.
- Lowercase, remove special characters, replace spaces with underscores.
- Return ONLY the topic string. No extra text.

Examples:
Input: "explain quantum physics to a 4th grader"
Output: "quantum_physics"

Input: "teach basic algebra to beginners"
Output: "basic_algebra"
"""

topic_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="topic_agent",
    description="Extracts a short topic name (1-2 words) from input text",
    instruction=INSTRUCTIONS,
    tools=[],  # No tools needed
)
