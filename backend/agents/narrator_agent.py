import os
from dotenv import load_dotenv
from google.adk import Agent
from tools.tts_tool import tts_tool

load_dotenv()

INSTRUCTIONS = """
You are a narrator agent.

Your task:
- You receive a script and a topic as input.
- You MUST call tts_tool(text=<script>, topic=<topic>).
- After the tool finishes, return ONLY the absolute path of the generated MP3 file.
- Do not add explanations, formatting, or additional text.
"""

narrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="NarratorAgent",
    description="Converts script text into narrated MP3 audio.",
    instruction=INSTRUCTIONS,
    tools=[tts_tool],
    output_key="audio_path"
)