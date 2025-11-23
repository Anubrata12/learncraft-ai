import os
import traceback

def generate_structured_script(file_path: str):
    if not os.path.exists(file_path):
        return {"status": "error", "error_message": f"Script file not found at {file_path}"}
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    sections = []
    current_title = None
    current_body = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith("[") and current_title is None:
            current_title = line
            current_body = []
            continue
        if line == "" and current_title:
            sections.append({"title": current_title, "content": "\n".join(current_body).strip()})
            current_title = None
            current_body = []
            continue
        if current_title:
            current_body.append(line)

    if current_title:
        sections.append({"title": current_title, "content": "\n".join(current_body).strip()})

    return {"status": "success", "data": sections}


def generate_slides_from_sections(sections: list[dict], topic: str) -> dict:
    """Create markdown slides in topic-named folder."""
    try:
        safe_topic = topic.replace(" ", "_").lower() if topic else "default_topic"
        output_dir = os.path.join("/app/data/slides", safe_topic)
        os.makedirs(output_dir, exist_ok=True)

        slide_paths = []
        for i, section in enumerate(sections, start=1):
            slide_path = os.path.join(output_dir, f"slide_{i}.md")
            slide_text = f"# {section.get('title', f'Slide {i}')}\n\n{section.get('content', '')}\n"
            with open(slide_path, "w", encoding="utf-8") as f:
                f.write(slide_text)
            slide_paths.append(os.path.abspath(slide_path))

        return {"status": "success", "data": slide_paths}

    except Exception as e:
        return {"status": "error", "error_message": f"{e}\n{traceback.format_exc()}"}
