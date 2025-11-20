import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai.types import Content, Part

# Load environment variables
load_dotenv()

# Get model name from .env
model_name = os.getenv("MODEL")
if not model_name:
    raise ValueError("MODEL environment variable is not set.")

# Define the orchestrator agent
main_agent = Agent(
    model=model_name,
    name="orchestrator",
    description="Main orchestrator agent",
    instruction="You coordinate tools and generate lessons.",
    tools=[]  # Add AgentTool(agent=...) here when ready
)

# Create runner and session
runner = InMemoryRunner(
    app_name="orchestrator-app",
    agent=main_agent
)
session = Session(
    id="session-001",
    app_name="orchestrator-app",
    user_id="user-001"
)


# Execution function
def run_agent(topic: str) -> str:
    try:
        content = Content(parts=[Part(text=topic)])
        events = runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        )
        final_text = ""
        for event in events:
            if hasattr(event, "text"):
                final_text = event.text
        return final_text
    except Exception as e:
        print(f"Agent error: {e}")
        return f"Error: {str(e)}"



