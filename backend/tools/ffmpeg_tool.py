import os
import subprocess
from typing import List, Dict, Any


def stitch_video(topic: str, audio_path: str, slide_paths: List[str]) -> dict:
    """
    Defines the video compilation logic using FFmpeg and returns the final video path.
    Args:
        topic: String - The topic name for the video (used in naming the output file).
        audio_path: String - Absolute path to the narrated MP3 file.
        slide_paths: List of absolute paths to slide image files.
    Returns:
        Success: {"status": "success", "data": "<absolute_video_path>"}
        Error: {"status": "error", "error_message": "..."}
    """
    safe_topic = topic.replace(" ", "_").lower() if topic else "default_topic"
    output_dir = "/app/data/videos"
    concat_file_path = os.path.join(output_dir, f"{safe_topic}.txt")

    print('ffmpeg_tool parameters received:')
    print(f"Audio Path: {audio_path}")
    print(f"Slide Paths: {slide_paths}")
    print(f"Topic: {topic}")

    try:
        # 0. Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        final_video_path = os.path.abspath(os.path.join(output_dir, f"{safe_topic}.mp4"))

        # 1. Create a minimal concat input file (essential for FFmpeg stitching)
        if slide_paths:
            with open(concat_file_path, "w") as f:
                for slide in slide_paths:
                    # 'duration 5' is a placeholder for real timing data
                    f.write(f"file '{slide}'\nduration 15\n")
                # The last slide needs to be listed again without duration to ensure it lasts until the end of the audio
                f.write(f"file '{slide_paths[-1]}'\n")

        # 2. FFmpeg command to stitch slides and audio
        ffmpeg_command = [
            "ffmpeg",
            "-f", "concat", "-safe", "0", "-i", concat_file_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-shortest",  # End video when the shortest input (audio) ends
            final_video_path
        ]

        try:
            # The 'check=True' flag raises a CalledProcessError if FFmpeg fails
            print("FFmpeg*******: Starting Video generation with FFmpeg...")
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            error_detail = f"FFmpeg execution failed with error: {e.stderr.decode('utf-8')}"
            print(f'FFmpeg*******: Video generation failed with: {error_detail}')
            return {"status": "error", "error_message": error_detail}

        # If execution were successful (or simulated successfully):
        return {"status": "success", "data": final_video_path}

    except (IOError, OSError) as e:
        # Handle errors related to file system operations (creating dir, writing concat file)
        return {"status": "error", "error_message": f"File system error during setup: {e}"}
    except Exception as e:
        # Catch any other unexpected errors
        return {"status": "error", "error_message": f"An unexpected error occurred during compilation: {e}"}

