import os
from pathlib import Path
import edge_tts
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("/app/data/speeches")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def tts_tool(text: str, topic: str) -> str:
    # Ensure safe filename
    safe_topic = topic.replace(" ", "_").lower() if topic else "script"
    output_file = OUTPUT_DIR / f"{safe_topic}.mp3"

    print(f"TTS_TOOL*******: Generating MP3 for topic '{safe_topic}' at {output_file}")

    tts = edge_tts.Communicate(text, os.getenv("MODEL_TTS"))
    await tts.save(str(output_file))

    print(f"TTS_TOOL*******: Saved MP3 at {output_file}")
    return str(output_file.resolve())
