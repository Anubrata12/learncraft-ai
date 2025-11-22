import os
from dotenv import load_dotenv

from google.adk import Agent
#from tools.ffmpeg_tool import stitch_video

load_dotenv()

INSTRUCTIONS = """
You are a video compiler agent.
Your task:
- You receive audio and slide file paths as input.
- You MUST call stitch_video(audio_path=<audio_path>, slide_paths=<slide_paths>).
- After the tool finishes, return ONLY the absolute path of the final compiled video file.
- Do not add explanations, formatting, or additional text.
"""

VIDEO_COMPILER = Agent(
    model=os.getenv("MODEL_TEXT"),
    description="Compiles slides and audio into a final video.",
    name="video_compiler",
    tools=[],
    instruction=INSTRUCTIONS,
)