# main.py
from fastapi import FastAPI
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part
import uuid

from agents.root_agent import root_agent

app = FastAPI()

# ADK session service
session_service = InMemorySessionService()

# Google ADK Runner
runner = Runner(
    app_name="learncraft-ai",
    agent=root_agent,
    session_service=session_service
)


@app.get("/generate")
async def generate(topic: str, user_id: str = "anon", session_id: str | None = None):
    # --- Reuse existing session if provided ---
    if session_id:
        try:
            session = await session_service.get_session(
                app_name=runner.app_name,
                session_id=session_id,
                user_id=user_id
            )
        except Exception:
            # if not found, create fresh session
            session = await session_service.create_session(
                app_name=runner.app_name,
                session_id=session_id,
                user_id=user_id
            )

    # --- Create new session for first-time call ---
    else:
        session_id = str(uuid.uuid4())
        session = await session_service.create_session(
            app_name=runner.app_name,
            session_id=session_id,
            user_id=user_id
        )


    content = Content(parts=[Part(text=topic)])
    mp3_path = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content
    ):
        print("EVENT TYPE:", type(event))
        print("EVENT RAW:", event)

        if event.content and event.content.parts:
            part = event.content.parts[0]
            print("PART TEXT:", part.text)

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
