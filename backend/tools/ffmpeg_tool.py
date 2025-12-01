import os
import subprocess
from typing import List, Dict, Any
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Use a path relative to the project directory
BASE_OUTPUT_DIR = PROJECT_ROOT / "data" / "videos"

# This will create learncraft-ai/data/videos/
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_audio_duration(file_path: str) -> float:
    """Uses ffprobe to get exact duration of an audio file in seconds."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        # Check=True ensures it raises an error if ffprobe fails
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        # Return 0.0 or raise the error, 0.0 stops the segment from being included
        return 0.0

def stitch_video(topic: str, audio_paths: List[str], slide_paths: List[str]) -> dict:
    """
    Stitches multiple audio/image pairs into a final video using temporary segments for sync.
    Args:
        topic: String - The topic name for the video.
        audio_paths: List of absolute paths to the narrated MP3 files (one per slide).
        slide_paths: List of absolute paths to slide image files.
    Returns:
        Success: {"status": "success", "data": "<absolute_video_path>"}
        Error: {"status": "error", "error_message": "..."}
    """
    safe_topic = topic.replace(" ", "_").lower() if topic else "default_topic"
    OUTPUT_DIR = BASE_OUTPUT_DIR / safe_topic
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_txt_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_segments.txt")
    final_output = os.path.join(OUTPUT_DIR, f"{safe_topic}.mp4")

    temp_segments: List[str] = []

    print('ffmpeg_tool parameters received:')
    print(f"Audio Path: {audio_paths}")
    print(f"Slide Paths: {slide_paths}")
    print(f"Topic: {topic}")

    try:
        # 0. Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print(f"OUTPUT_DIR: {OUTPUT_DIR}")

        # 1. Iterate over slides and audio files to create temporary video segments
        for i, (slide, audio) in enumerate(zip(slide_paths, audio_paths)):
            duration = get_audio_duration(audio)

            if duration <= 0:
                print(f"Skipping segment {i} due to zero or negative audio duration.")
                continue

            segment_out = os.path.join(OUTPUT_DIR, f"temp_{safe_topic}_{i}.mp4")
            temp_segments.append(segment_out)

            # FFmpeg command to combine 1 image + 1 audio for the exact audio duration
            # -loop 1: ensures the image is displayed
            # -t: sets the duration of the output file
            cmd_segment = [
                "ffmpeg", "-y",  # -y: Overwrite output files without asking
                "-loop", "1", "-i", slide,
                "-i", audio,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                segment_out
            ]

            print(f"FFmpeg*******: Creating segment {i}...")
            subprocess.run(cmd_segment, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Stitch the temporary segments together using the concat demuxer
        if not temp_segments:
            return {"status": "error", "error_message": "No valid video segments were created."}

        with open(input_txt_path, "w") as f:
            for segment in temp_segments:
                f.write(f"file '{segment}'\n")

        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", input_txt_path,
            "-c", "copy",  # Fast copy since all segments are already encoded
            final_output
        ]

        print("FFmpeg*******: Stitching final video...")
        subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 3. Cleanup temporary files
        for segment in temp_segments:
            os.remove(segment)

        return {"status": "success", "data": final_output}

    except subprocess.CalledProcessError as e:
        error_detail = f"FFmpeg execution failed: {e.stderr.decode('utf-8')}"
        print(f'FFmpeg*******: Video generation failed with: {error_detail}')
        return {"status": "error", "error_message": error_detail}

    except Exception as e:
        # Catch any other unexpected errors
        return {"status": "error", "error_message": f"An unexpected error occurred during compilation: {e}"}