import os
from pathlib import Path
from typing import Dict, Any
import edge_tts
from dotenv import load_dotenv

load_dotenv()

BASE_OUTPUT_DIR = Path("/app/data/speeches")
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


async def tts_tool(text: str, topic: str) -> Dict[str, Any]:
    """
    Converts the given text, splits into sections and converts it into speech and saves it as MP3 files.
    Args:
        text: The full script text to be converted into speech.
        topic: The topic name for organizing output files.
    Returns:
        Success: {"status": "success", "data": [list of absolute MP3 file paths]}
        Error: {"status": "error", "error_message": "..."}
    """
    # Split text into sections
    script_sections = [line.strip() for line in text.split('\n') if line.strip()]

    # Ensure safe filename
    safe_topic = topic.replace(" ", "_").lower() if topic else "script"
    OUTPUT_DIR = BASE_OUTPUT_DIR / safe_topic
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    transcript_file = OUTPUT_DIR / f"{safe_topic}.txt"

    generated_paths: list[str] = []

    print(f"TTS_TOOL*******: Generating {len(script_sections)} MP3 files for topic '{safe_topic}'")

    try:
        for i, section_text in enumerate(script_sections):
            output_file = OUTPUT_DIR / f"{safe_topic}_{i+1}.mp3"

            #write section_text to transcript file
            with open(transcript_file, "a", encoding="utf-8") as tf:
                tf.write(f"Section {i + 1}:\n{section_text}\n\n")

            print(f"TTS_TOOL*******: Generating section {i + 1} at {output_file}")

            try:
                tts = edge_tts.Communicate(section_text, os.getenv("MODEL_TTS"))
                await tts.save(str(output_file))
                generated_paths.append(str(output_file.resolve()))
            except Exception as e:
                print(f"TTS_TOOL ERROR: Failed to generate audio for section {i + 1}: {e}")

        print(f"TTS_TOOL*******: Successfully saved {len(generated_paths)} files.")
        return {"status": "success", "data": generated_paths}
    except Exception as e:
        error_message = f"TTS_TOOL ERROR: An error occurred during TTS processing: {e}"
        print(error_message)
        return {"status": "error", "error_message": error_message}
