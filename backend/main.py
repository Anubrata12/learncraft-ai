# main.py
import logging
# --- 1. Set Logging Level to DEBUG ---
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logging.getLogger("google.adk").setLevel(logging.DEBUG)

from fastapi import FastAPI
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai.types import Content, Part
import uuid
import re

from agents.orchestrator import orchestrator_agent

app = FastAPI()

# ADK session service
session_service = InMemorySessionService()

# Google ADK Runner
runner = Runner(
    app_name="learncraft-ai",
    agent=orchestrator_agent,
    session_service=session_service,
    plugins=[
        LoggingPlugin() # <-- Registration of the plugin
    ]
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
    mp4_path = None
    exercises = None
    answers = None  # add this at the top with mp4_path, exercises

    async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content
    ):
        #print("EVENT TYPE:", type(event))
        #print("EVENT RAW:", event)

        if event.content and event.content.parts:
            part = event.content.parts[0]
            if not part.text:
                continue

            clean = part.text.strip()

            if clean.endswith(".mp4"):
                mp4_path = clean

            elif "EXERCISE_OUTPUT:" in clean:
                exercises = clean.replace("EXERCISE_OUTPUT:", "").strip()

            elif "ANSWER_OUTPUT:" in clean:  # <-- new line
                answers = clean.replace("ANSWER_OUTPUT:", "").strip()

            elif re.match(r"^\d+\.", clean):
                if exercises is None:
                    exercises = clean
                else:
                    exercises += "\n" + clean

    # ---- Final Response ----
    return {
        "session_id": session.id,
        "user_id": user_id,
        "mp4": mp4_path,
        "exercises": exercises,
        "answers": answers,  # <-- new line
    }
