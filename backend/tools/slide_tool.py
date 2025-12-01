from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import traceback

# Recommended: Create a 'data' folder at the project root for outputs
PROJECT_ROOT = Path(__file__).resolve().parents[1] # Navigates up from tts_tool.py -> tools -> backend -> learncraft-ai
BASE_OUTPUT_DIR = PROJECT_ROOT / "data" / "slides"

# Ensure the directory is created
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# ... rest of tts_tool.py ...

SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080

# TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def create_slide_image(title: str, content: str, save_path: Path):

    try :
        """Generates a clean, modern slide PNG."""
        img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), (245, 247, 250))
        draw = ImageDraw.Draw(img)

        # Gradient background (subtle)
        for i in range(SLIDE_HEIGHT):
            color = (245 - i // 30, 247 - i // 40, 250 - i // 50)
            draw.line([(0, i), (SLIDE_WIDTH, i)], fill=color)

        # Load fonts
        # title_font = ImageFont.truetype(TITLE_FONT, 72)
        # body_font = ImageFont.truetype(BODY_FONT, 48)

        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

        # Title box
        draw.rectangle([(0, 0), (SLIDE_WIDTH, 180)], fill=(25, 40, 60))
        draw.text((80, 50), title, font=title_font, fill="white")

        # Content text
        wrapped_text = textwrap.fill(content, width=55)
        draw.multiline_text(
            (80, 240),
            wrapped_text,
            font=body_font,
            fill=(20, 20, 20),
            spacing=15
        )

        img.save(str(save_path))

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        print("SLIDE_TOOL ERROR********** : create_slide_image")
        print(error_msg)

def generate_structured_script(file_path: str):
    '''Parses the script file into a structured format with sections.
        Arguments:
            filePath: The absolute path to the script file.
        Returns:
            A dictionary with status and structured script data.
            Success: {"status": "success", "data": [...]}
            Error: {"status": "error", "error_message": "..."}
    '''
    if not os.path.exists(file_path):
        return {"status": "error", "error_message": f"Script file not found at {file_path}"}
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    sections = []
    current_title = None
    current_body = []

    for line in lines:
        line = line.strip()
        # A non-empty line with no indentation starts a new section
        if line and not line.startswith("[") and current_title is None:
            current_title = line
            current_body = []
            continue
        # A blank line means the section ended
        if line == "" and current_title:
            sections.append({"title": current_title, "content": "\n".join(current_body).strip()})
            current_title = None
            current_body = []
            continue
        # Regular body lines
        if current_title:
            current_body.append(line)
    # Add the last section if it's not empty
    if current_title:
        sections.append({"title": current_title, "content": "\n".join(current_body).strip()})

    return {"status": "success", "data": sections}


def generate_slides_from_sections(sections: list[dict], topic: str) -> dict:
    """
    Creates a simple markdown slide file for each section.

    Args:
        sections: List of dicts like [{"title": "...", "content": "..."}]
        output_dir: Directory to save slide files.

    Returns:
        {"status": "success", "data": [list of file paths]}
        OR
        {"status": "error", "error_message": "..."}
    """
    try:
        safe_topic = topic.replace(" ", "_").lower() if topic else "default_topic"
        output_dir = BASE_OUTPUT_DIR / safe_topic
        output_dir.mkdir(parents=True, exist_ok=True)

        slide_paths = []
        print(f"SLIDE_TOOL*******: Generating styled PNG slides for '{safe_topic}' in {output_dir}")

        for i, section in enumerate(sections, start=1):
       #     slide_path = os.path.join(output_dir, f"slide_{i}.png")
            slide_path = output_dir / f"slide_{i}.png"

            print(f"SLIDE_TOOL*******: SIDE PATH '{slide_path}' in {output_dir}")

            title = section.get("title", f"Slide {i}")
            content = section.get("content", "")

            create_slide_image(title, content, slide_path)
            slide_paths.append(os.path.abspath(slide_path))

        return {"status": "success", "data": slide_paths}

    except Exception as e:
        error_msg = f"{e}\n{traceback.format_exc()}"
        print("SLIDE_TOOL ERROR**********")
        print(error_msg)
        return {"status": "error", "error_message": f"{e}\n{traceback.format_exc()}"}