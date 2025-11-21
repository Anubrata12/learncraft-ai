from pathlib import Path
import edge_tts

# Output directory
OUT_DIR = Path("/app/data/speeches")
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-US-AriaNeural"

# --- IMPORTANT: must be async for ADK ---
async def tts_tool(text: str, filename="algebra.mp3") -> str:
    output_file = OUT_DIR / filename

    print("TOOL CALL: Generating TTS for text length:", len(text))

    tts = edge_tts.Communicate(text, VOICE)
    await tts.save(str(output_file))   # <-- no crash

    print("TOOL CALL: Saved MP3:", output_file)

    return str(output_file.resolve())
