import asyncio
import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.adk.tools import AgentTool
from google.genai.types import Content, Part

from agents.narrator import narrator_agent

load_dotenv()

INSTRUCTIONS = """
Generate a complete educational script based on the user's topic.
Call the narrator agent to convert the script to MP3.
Return ONLY the MP3 file path, never the script itself.
"""

# Orchestrator agent with narrator tool
orchestrator_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="orchestrator",
    description="Minimal orchestrator agent",
    instruction=INSTRUCTIONS,
    tools=[AgentTool(agent=narrator_agent)]
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
