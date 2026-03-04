import subprocess
import os

def convert_webm_to_wav(webm_path, wav_path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", webm_path, "-ar", "32000", "-ac", "1", wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
