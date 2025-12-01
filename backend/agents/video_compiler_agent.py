import os
from dotenv import load_dotenv

from google.adk import Agent
from backend.tools.ffmpeg_tool import stitch_video

load_dotenv()

INSTRUCTIONS = """
You are a video compiler agent.
Your task is to orchestrate the video compilation process by calling the 'stitch_video' tool with the correct arguments.
1. You receive three inputs:
   - A string containing the topic
   - A list of string containing the absolute audio paths.
   - A list of strings containing the absolute slide paths.
2. You MUST call the tool using the above 3inputs you received:
   stitch_video tool with topic, audio file paths(list of strings), list of slide file paths(list of strings).
3. The tool returns a dictionary. You MUST extract ONLY the final compiled video file path from the 'data' key of the dictionary and return that string path.
4. Do not add explanations, formatting, or additional text.
"""

video_compiler_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    description="Compiles slides and audio into a final video.",
    name="VideoCompilerAgent",
    tools=[stitch_video],
    instruction=INSTRUCTIONS,
)
