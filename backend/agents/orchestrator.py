import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import AgentTool

from agents.topic_agent import topic_agent
from agents.script_agent import script_agent
from agents.narrator_agent import narrator_agent
from agents.slide_agent import slide_agent
from agents.video_compiler_agent import video_compiler_agent
from agents.exercise_agent import exercise_agent
from tools.state_tool import save_topic, load_topic

load_dotenv()

INSTRUCTIONS = """

You are the Orchestrator.

RULE 1 — Exercise Mode
-----------------------
If the user message contains:
"exercise", "practice", "questions", "quiz", "test"

- First call load_topic
- Then call ExerciseAgent with:
    the topic returned from load_topic as a string

- Store the result:
    $store("exercise_text", exercise_text)

- Return only the exercise output.
- Do NOT run the video pipeline in this mode.


RULE 2 — Full Video Pipeline
----------------------------

Your task is:

1. Receive the user's input text.
2. Call the 'topic_agent' to generate a short topic name (max 2 words) from the input.
    - After receiving the topic_name, IMMEDIATELY call save_topic(topic_name=...).
3. Call the 'script_agent' to generate a complete educational script based on the user's input.
4. Using the SAME script content from step 3 and the topic from step 2:
   - First call the 'slide_agent' with the script and the topic.
   - Then call the 'narrator_agent' with the script and the topic.
   - Third call the 'video_compiler_agent'. 
     IMPORTANT: You must pass exactly ONE argument named 'request'.
     The value of 'request' must be a JSON string containing the following keys:
        - "topic": the topic from step 2
        - "audio_paths": the list of MP3 file paths returned by the 'narrator_agent'
        - "image_paths": the list of slides file paths returned by the 'slide_agent'    
     Example of the argument structure: 
     request='{"topic": "triangle", "audio_paths": ["/path/to/audio.mp3","/path/to/audio.mp3"], "image_paths": ["/path/1.png", "/path/2.png"]}'

5. When the 'video_compiler_agent' returns the MP4 file path,
   your FINAL MESSAGE must contain ONLY that file path.
   Absolutely no extra text, no quotes, no JSON, no explanation.
   Example of final output:
   /app/data/videos/quantum_physics.mp4
"""

orchestrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="orchestrator",
    description="Generates the educational video by orchestrating multiple specialized agents.",
    instruction=INSTRUCTIONS,
    tools=[
        AgentTool(agent=topic_agent),
        AgentTool(agent=script_agent),
        AgentTool(agent=slide_agent),
        AgentTool(agent=narrator_agent),
        AgentTool(agent=video_compiler_agent),
        AgentTool(agent=exercise_agent),
        save_topic,
        load_topic,
    ],
)
