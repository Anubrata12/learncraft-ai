import os
import traceback

def generate_structured_script(filePath : str):
    '''Parses the script file into a structured format with sections.
    Arguments:
        filePath: The absolute path to the script file.
    Returns:
        A dictionary with status and structured script data.
        Success: {"status": "success", "data": [...]}
        Error: {"status": "error", "error_message": "..."}
    '''

    print(f"Reading script from: {filePath}")
    if not os.path.exists(filePath):
        print(f"Error: Script file not found at {filePath}")
        return {"status": "error", "error_message": f"Script file not found at {filePath}"}
    with open(filePath, "r", encoding="utf-8") as f:
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
            sections.append({
                "title": current_title,
                "content": "\n".join(current_body).strip()
            })
            current_title = None
            current_body = []
            continue
        # Regular body lines
        if current_title:
            current_body.append(line)
    # Add the last section if it's not empty
    if current_title:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_body).strip()
        })
    return {"status": "success", "data": sections}


def generate_slides_from_sections(sections: list[dict], output_dir: str) -> dict:
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
        os.makedirs(output_dir, exist_ok=True)

        slide_paths = []

        for i, section in enumerate(sections, start=1):
            title = section.get("title", f"Slide {i}")
            content = section.get("content", "")

            slide_text = f"# {title}\n\n{content}\n"

            slide_path = os.path.join(output_dir, f"slide_{i}.md")

            with open(slide_path, "w", encoding="utf-8") as f:
                f.write(slide_text)

            slide_paths.append(os.path.abspath(slide_path))

        return {"status": "success", "data": slide_paths}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"{e}\n{traceback.format_exc()}"
        }


