import os
from dotenv import load_dotenv
from google.adk import Agent

load_dotenv()

INSTRUCTIONS = """
You are an Answer Generator Agent.

Your job:
- Receive the exercises stored in the orchestrator's session.
- Generate answers for each exercise.
- Number answers to match exercises exactly.
- Provide clear, beginner-friendly explanations.
- Return the output in this format:

ANSWER_OUTPUT:
1. Answer...
2. Answer...
"""

answer_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="AnswerAgent",
    description="Generates answers for exercises previously generated.",
    instruction=INSTRUCTIONS,
    tools=[],
    output_key="answers"
)
