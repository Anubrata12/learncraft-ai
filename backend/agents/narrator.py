from pathlib import Path
import asyncio

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai.types import Content, Part

from tools.tts_tool import tts_tool

SCRIPT_PATH = Path("/app/data/scripts/algebra.md")
if not SCRIPT_PATH.exists():
    print("[WARNING] Script missing at:", SCRIPT_PATH.resolve())


def load_script() -> str:
    print("[DEBUG] Loading script from:", SCRIPT_PATH.resolve())
    return SCRIPT_PATH.read_text(encoding="utf-8")


INSTRUCTIONS = """
You are a narrator agent.
Your job:
1. Receive the full script text.
2. Call tts_tool(text) to generate MP3.
3. Return ONLY the absolute audio file path.
"""

narrator_agent = Agent(
    model="gemini-2.5-flash",
    name="narrator",
    description="Turns a script into MP3 via TTS tool.",
    instruction=INSTRUCTIONS,
    tools=[tts_tool],
)

runner = InMemoryRunner(
    app_name="narrator-app",
    agent=narrator_agent,
)

# Lazy session loader
def get_session() -> Session:
    """
    Ensures session exists.
    ADK sessions are async → must use asyncio.run().
    """
    try:
        # Attempt to fetch existing session
        return asyncio.run(
            runner.session_service.get_session(
                app_name="narrator-app",
                session_id="session-001"
            )
        )
    except Exception:
        print("[INFO] Session not found → creating new session")

        return asyncio.run(
            runner.session_service.create_session(
                app_name="narrator-app",
                user_id="user-001",
                session_id="session-001"
            )
        )


# TTS synthesis
def synthesize_via_agent() -> str:
    session = get_session()
    script_text = load_script()

    try:
        # Create message
        content = Content(parts=[Part(text=script_text)])

        # Run agent (sync generator)
        events = runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        )

        # Extract MP3 path
        mp3_path = ""
        for event in events:
            if hasattr(event, "text") and event.text:
                mp3_path = event.text

        return mp3_path

    except Exception as e:
        print(f"[ERROR] Agent execution failed: {e}")
        return ""
