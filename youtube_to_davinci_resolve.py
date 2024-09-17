import subprocess
import re
import tempfile
from pathlib import Path
import yt_dlp

# TODO move global vars to a json file

UNWANTED_WORDS = [
    'Sound', 'effect', 'for editing', 'editing', '(dl in desc)', '-', '()',
    "''"
]
# yes im using an asmongold clip... bite me
TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"


def get_video_title(url: str) -> str:
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
    }
    # Extract info without downloading
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info.get('title', 'No title found')


def sanitize_filename(filename: str) -> str:
    # Remove any Windows unsafe characters
    filename = re.sub(r'[\/:*?"<>|]', '', filename)

    # Remove extra spaces and trim
    filename = ' '.join(filename.split())

    # Remove specific words
    for phrase in UNWANTED_WORDS:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        filename = pattern.sub('', filename)

    # Remove extra spaces left after removing words
    filename = ' '.join(filename.split())
    filename = filename.title()

    if not filename:
        filename = 'Untitled'

    return filename


def get_link() -> str:
    """gets last item in users clipboard."""
    link = subprocess.getoutput("powershell.exe -Command Get-Clipboard")
    return link
