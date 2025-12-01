from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import traceback


SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080

TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def create_slide_image(title: str, content: str, save_path: str):
    """Generates a clean, modern slide PNG."""
    img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Gradient background (subtle)
    for i in range(SLIDE_HEIGHT):
        color = (245 - i // 30, 247 - i // 40, 250 - i // 50)
        draw.line([(0, i), (SLIDE_WIDTH, i)], fill=color)

    # Load fonts
    title_font = ImageFont.truetype(TITLE_FONT, 72)
    body_font = ImageFont.truetype(BODY_FONT, 48)

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

    img.save(save_path)


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
        output_dir = os.path.join("/app/data/slides", safe_topic)
        os.makedirs(output_dir, exist_ok=True)

        slide_paths = []
        print(f"SLIDE_TOOL*******: Generating styled PNG slides for '{safe_topic}' in {output_dir}")

        for i, section in enumerate(sections, start=1):
            slide_path = os.path.join(output_dir, f"slide_{i}.png")
            title = section.get("title", f"Slide {i}")
            content = section.get("content", "")

            create_slide_image(title, content, slide_path)
            slide_paths.append(os.path.abspath(slide_path))

        return {"status": "success", "data": slide_paths}

    except Exception as e:
        return {"status": "error", "error_message": f"{e}\n{traceback.format_exc()}"}