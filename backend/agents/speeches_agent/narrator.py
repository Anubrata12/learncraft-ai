from fastapi import FastAPI
import edge_tts
from pathlib import Path

app = FastAPI()

# ---------------------------------
#  Base Directories
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]         # → backend/
DATA_DIR = BASE_DIR / "data"                           # → backend/data/
SCRIPT_DIR = DATA_DIR / "scripts"                      # → backend/data/scripts/
OUT_DIR = DATA_DIR / "speeches"                        # → backend/data/speeches/

SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Script file inside data/scripts/
SCRIPT_PATH = SCRIPT_DIR / "algebra.md"

VOICE = "en-US-AriaNeural"


# ---------------------------------
#  Load script from file
# ---------------------------------
def load_script() -> str:
    print("Looking for script at:", SCRIPT_PATH)
    if not SCRIPT_PATH.exists():
        return f"Script file missing at: {SCRIPT_PATH}"
    return SCRIPT_PATH.read_text(encoding="utf-8")



# ---------------------------------
#  Text → Speech
# ---------------------------------
async def synthesize(filename="algebra_edgetts.mp3"):
    text = load_script()
    output_file = OUT_DIR / filename

    tts = edge_tts.Communicate(text, VOICE)
    await tts.save(str(output_file))

    return output_file


# ---------------------------------
#  API Route
# ---------------------------------
@app.get("/narrate")
async def narrate():
    audio_file = await synthesize()
    return {"file": str(audio_file)}

# import markdown
# from bs4 import BeautifulSoup
#
# def clean_markdown(md_text: str) -> str:
#     html = markdown.markdown(md_text)
#     soup = BeautifulSoup(html, "html.parser")
#     return soup.get_text()
#
# raw = SCRIPT_PATH.read_text()
# script_text = clean_markdown(raw)
# tts = edge_tts.Communicate(script_text, VOICE)
