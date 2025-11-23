import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import AgentTool

from agents.narrator import narrator_agent
from agents.slide_agent import slide_agent

load_dotenv()

INSTRUCTIONS = """
Generate a complete educational script based on the user's topic.

Once the script is generated, 
using the same script you MUST call the 'slide_agent' agent and then the 'narrator_agent' agent sequentially.

1. Call the 'slide_agent' agent with the complete script content (the tool input).
2. Call the 'narrator' agent with the complete script content (the tool input).

After both tools return, your final output should ONLY be the MP3 file path provided by the 'narrator_agent' agent
"""

orchestrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="orchestrator",
    description="Orchestrator agent",
    instruction=INSTRUCTIONS,
    tools=[
        AgentTool(agent=slide_agent),
        AgentTool(agent=narrator_agent)
    ]
)
