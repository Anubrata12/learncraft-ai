import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import AgentTool

from agents.topic_agent import topic_agent
from agents.narrator import narrator_agent
from agents.slide_agent import slide_agent

load_dotenv()

INSTRUCTIONS = """
You are the Orchestrator.

Your task is:

1. Receive the user's input text.
2. Call the 'topic_agent' to generate a short topic name (max 2 words) from the input.
3. Generate a complete, clean educational script based on the user's input.
4. Using the SAME script content:
   - First call the 'slide_agent' tool with the script and the topic.
   - Then call the 'narrator_agent' tool with the script and the topic.
5. When the narrator_agent returns the MP3 file path,
   your FINAL MESSAGE must contain ONLY that file path.
   Absolutely no extra text, no quotes, no JSON, no explanation.
   Example of final output:
   /app/data/speeches/quantum_physics.mp3
"""


orchestrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="orchestrator",
    description="Generates slides + narration for a user query",
    instruction=INSTRUCTIONS,
    tools=[
        AgentTool(agent=topic_agent),
        AgentTool(agent=slide_agent),
        AgentTool(agent=narrator_agent),
    ],
)
