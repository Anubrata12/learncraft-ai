import os
from dotenv import load_dotenv
from google.adk import Agent
from tools.tts_tool import tts_tool

load_dotenv()

INSTRUCTIONS = """
You are the Narrator Agent. Your goal is to create the audio narration for the script.

Your steps:

1. You will receive a structured script containing multiple sections.
2. For each section:
   - Use the heading only as a guide for tone and meaning.
   - DO NOT read headings aloud.
   - Rewrite the section content into a smooth conversational narration.
3. Keep the number of narration sections the same as the number of script sections.
4. Combine the finalized narration lines into a SINGLE string, with each section separated by exactly ONE newline character ("\\n"). No blank extra lines.
5. Call tts_tool EXACTLY ONCE using the full narration string:
       tts_tool(text=<final narration>, topic=<topic>)

---- OUTPUT FORMAT RULES (IMPORTANT) ----

6. You MUST return ONLY the output from tts_tool.

7. The returned output MUST be in this exact format:

["/path/audio_1.mp3", "/path/audio_2.mp3", ...]

8. Do NOT add:
   - Backticks
   - Markdown formatting (` ```json `)
   - Keys like {"audio_path": ...} or {"result": ...}
   - Status messages
   - Explanations
   - Quotes around the JSON array itself

The FIRST character of your output must be `[` and the FINAL character must be `]`.
"""

narrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="NarratorAgent",
    description="Converts script text into spoken narration and audio files.",
    instruction=INSTRUCTIONS,
    tools=[tts_tool],
    output_key="audio_path"
)
