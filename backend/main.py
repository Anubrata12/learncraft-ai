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
    # Default user fallback
    user_id = user_id or "anon"

    # Always ADK session (UUID inside)
    session = await ADKSessionManager.get_or_create_session(
        runner=runner,
        user_id=user_id
    )

    content = Content(parts=[Part(text=topic)])

    mp3_path = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content
    ):
        # DEBUG PRINTS
        print("EVENT TYPE:", type(event))
        print("EVENT RAW:", event)

        if event.content and event.content.parts:
            part = event.content.parts[0]
            print("PART TEXT:", part.text)

            # Narrator_agent final output (just the mp3 path)
            if part.text:
                clean_part = part.text.strip()
                if clean_part.endswith(".mp3"):
                    mp3_path = clean_part
                    print("🎯 CAPTURED MP3:", clean_part)

    print("FINAL MP3 PATH:", mp3_path)

    return {
        "session_id": session.id,
        "user_id": user_id,
        "mp3": mp3_path or "No MP3 generated"
    }
