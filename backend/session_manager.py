# backend/session_manager.py
import uuid
from google.adk.sessions import Session

class ADKSessionManager:

    @staticmethod
    async def get_or_create_session(runner, user_id: str) -> Session:
        # Generate a unique session_id for this request OR client
        session_id = str(uuid.uuid4())

        # Try to fetch (usually None for UUID)
        session = await runner.session_service.get_session(
            app_name="learncraft-ai",
            session_id=session_id,
            user_id=user_id,
        )

        if session is None:
            session = await runner.session_service.create_session(
                app_name="learncraft-ai",
                session_id=session_id,
                user_id=user_id,
            )

        return session
