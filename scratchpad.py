# from youtube_to_davinci_resolve import *
from pprint import pprint
from pathlib import Path
import json

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"

# current working auto-editor:
# auto-editor "test.m4a" --margin 0s

# current working ffmpeg:
# ffmpeg -i "input.m4a" -c:a libmp3lame -b:a 320k "output.mp3"

# yt-dlp --remux-video mp4 --format "bv+ba[ext=m4a]/ba[ext=aac]" "https://www.youtube.com/watch?v=xxfl7NCzBAA&pp=ygUIc2Z4IG1lbWU%3D"

download_dir = Path().home() / "Downloads" / "Youtube"


def load_settings():
    settings_file = download_dir / "settings.json"
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {
            "UNWANTED_WORDS": [
                "sound", "effect", "for editing", "editing", "(dl in desc)",
                "-", "()", "''", "."
            ],
            "SFX_KEYWORDS": ["sfx", "sound effect", "sound effects"],
            "SFX_TRIM_MARGIN": {
                "aggressive": "-0.05s,0s",
                "standard": "0s,0s",
                "loose": "0.5s,0.5s"
            },
            "SFX_SAVE_DIR":
            "D:/Editing Stuff/SFX/Meme sound Clips, Mario, Cartoon Sounds, Funny Etc/Recent",
            "AUTO_DELETE_TEMP":
            True,
            "SAVE_TO_PROJECT_FOLDER":
            True
        }
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
    return settings


settings = load_settings()
UNWANTED_WORDS = settings["UNWANTED_WORDS"]
SFX_KEYWORDS = settings["SFX_KEYWORDS"]
SFX_TRIM_MARGIN = settings["SFX_TRIM_MARGIN"]
SFX_SAVE_DIR = settings["SFX_SAVE_DIR"]
AUTO_DELETE_TEMP = settings["AUTO_DELETE_TEMP"]
SAVE_TO_PROJECT_FOLDER = settings["SAVE_TO_PROJECT_FOLDER"]

# cleaning memory
del settings
