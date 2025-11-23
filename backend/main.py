# main.py
from fastapi import FastAPI
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

from agents.orchestrator import orchestrator_agent
from session_manager import ADKSessionManager

app = FastAPI()

# Google ADK Runner
runner = InMemoryRunner(
    app_name="learncraft-ai",
    agent=orchestrator_agent
)


@app.get("/generate")
async def generate(topic: str, user_id: str | None = None):
    # Default user if ui does not pass one
    user_id = user_id or "anon"

    # Fetch or create ADK session (UUID inside)
    session = await ADKSessionManager.get_or_create_session(
        runner=runner,
        user_id=user_id
    )

    content = Content(parts=[Part(text=topic)])
    mp3_path = None

    async for event in runner.run_async(
        user_id=user_id,          # user input
        session_id=session.id,    # uuid session
        new_message=content
    ):
        if getattr(event, "tool_output", None):
            mp3_path = event.tool_output

    return {
        "session_id": session.id,
        "user_id": user_id,
        "mp3": mp3_path or "No MP3 generated"
    }
