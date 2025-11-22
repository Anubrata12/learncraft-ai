import asyncio
import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.adk.tools import AgentTool
from google.genai.types import Content, Part

from agents.narrator import narrator_agent
from agents.slide_agent import slide_agent

load_dotenv()

INSTRUCTIONS = """
Generate a complete educational script based on the user's topic.

Once the script is generated, 
using the same script you MUST call the 'slide_agent' agent and then the 'narrator_agent' agent sequentially.

1. Call the 'slide_agent' agent with the complete script content (the tool input).
2. Call the 'narrator' agent with the complete script content (the tool input).

After both tools return, your final output should ONLY be the MP3 file path provided by the 'narrator_agent' agen
"""

# Orchestrator agent with narrator tool
orchestrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="orchestrator",
    description="Minimal orchestrator agent",
    instruction=INSTRUCTIONS,
    tools=[AgentTool(agent=narrator_agent), AgentTool(agent=slide_agent)]
)

runner = InMemoryRunner(
    app_name="orchestrator-app",
    agent=orchestrator_agent
)

# Simple session helper
def get_session() -> Session:
    session = asyncio.run(
        runner.session_service.get_session(
            app_name="orchestrator-app",
            session_id="session-001",
            user_id="user-001"
        )
    )
    if session is None:
        session = asyncio.run(
            runner.session_service.create_session(
                app_name="orchestrator-app",
                user_id="user-001",
                session_id="session-001"
            )
        )
    return session

def run_agent(topic: str) -> str:
    session = get_session()
    content = Content(parts=[Part(text=topic)])

    events = runner.run(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    )

    # Loop through events and detect tool_output from narrator
    for event in events:
        if hasattr(event, "tool_output") and event.tool_output:
            # narrator returns absolute MP3 path here
            return event.tool_output

    return "No MP3 generated"
