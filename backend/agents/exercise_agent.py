import os
from dotenv import load_dotenv
from google.adk import Agent

load_dotenv()

INSTRUCTIONS = """
You are an Exercise Generator Agent.

Your job:
- Receive a topic from the orchestrator.
- Generate 5–10 practice questions about that topic.
- Questions should be clear, simple, and beginner-friendly.
- Do NOT generate answers unless explicitly asked.
- Return ONLY the questions in clean numbered list format.
"""

exercise_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="ExerciseAgent",
    description="Generates practice questions for a given topic.",
    instruction=INSTRUCTIONS,
    tools=[],  # no tools needed
    output_key="exercise_text"
)