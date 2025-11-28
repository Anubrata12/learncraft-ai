import os
from dotenv import load_dotenv
from google.adk import Agent

load_dotenv()

INSTRUCTIONS = """
You are an Exercise Generator Agent.

Your job:
- Receive a script from the orchestrator.
- Generate 5–10 practice questions based on the script.
- Questions should be clear, simple, and beginner-friendly.
- Do NOT generate answers unless explicitly asked.

Return the output in the following format exactly:

EXERCISE_OUTPUT:
1. Question...
2. Question...
"""


exercise_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="ExerciseAgent",
    description="Generates practice questions for a given topic.",
    instruction=INSTRUCTIONS,
    tools=[],  # no tools needed
    output_key="exercise_text"
)