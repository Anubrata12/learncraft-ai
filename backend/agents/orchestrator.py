import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import AgentTool

from agents.topic_agent import topic_agent
from agents.script_agent import script_agent
from agents.narrator import narrator_agent
from agents.slide_agent import slide_agent
from agents.video_compiler_agent import video_compiler

load_dotenv()

INSTRUCTIONS = """

You are the Orchestrator.

Your task is:

1. Receive the user's input text.
2. Call the 'topic_agent' to generate a short topic name (max 2 words) from the input.
3. Call the 'script_agent' to generate a complete educational script based on the user's input.
4. Using the SAME script content from step 3 and the topic from step 2:
   - First call the 'slide_agent' tool with the script and the topic.
   - Then call the 'narrator_agent' tool with the script and the topic.
   - Third call the 'video_compiler' tool with:
        - the MP3 file path returned by the 'narrator_agent'
        - the list of slides file paths returned by the 'slide_agent'
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
        AgentTool(agent=script_agent),
        AgentTool(agent=slide_agent),
        AgentTool(agent=narrator_agent),
        AgentTool(agent=video_compiler)
    ],
)
