import os
from pathlib import Path
import edge_tts
from dotenv import load_dotenv


load_dotenv()

# Input directory
SCRIPT_PATH = Path("/app/data/scripts/algebra.md")
# Output directory
OUTPUT_DIR = Path("/app/data/speeches")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FILENAME = "algebra.mp3"


def load_script() -> str:
    print("[DEBUG] Loading script from:", SCRIPT_PATH.resolve())
    return SCRIPT_PATH.read_text(encoding="utf-8")

# --- IMPORTANT: must be async for ADK ---
async def tts_tool(text: str) -> str:
    print("TTS_TOOL*******: Starting TTS generation")
    output_file = OUTPUT_DIR / FILENAME

    print("TOOL CALL: Generating TTS for text length:", len(text))

    tts = edge_tts.Communicate(text, os.getenv("MODEL_TTS"))
    await tts.save(str(output_file))   # <-- no crash

    print("TOOL CALL: Saved MP3:", output_file)

    return str(output_file.resolve())
