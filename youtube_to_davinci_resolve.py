import subprocess
import re
import tempfile
from pathlib import Path
import yt_dlp

# TODO emojis in video_title may cause issues. keep an eye on it
# TODO move global vars to a json file
# TODO before that convert global vars to dict so its easier to incorporate json later
UNWANTED_WORDS = [
    'Sound', 'effect', 'for editing', 'editing', '(dl in desc)', '-', '()',
    "''", '.'
]
SFX_KEYWORDS = [
    'sfx',
    'sound effect',
    'sound effects',
]
# yes im using an asmongold clip... bite me
TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"
AUTO_DELETE_TEMP = False


def get_clipboard() -> str:
    """gets last item in users clipboard."""
    link = subprocess.getoutput("powershell.exe -Command Get-Clipboard")
    return link


def get_video_title(url: str) -> str:
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
    }
    # Extract info without downloading
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info.get('title', 'No title found')


def is_sfx(video_title: str) -> bool:
    return any(word.lower() in video_title.lower() for word in SFX_KEYWORDS)


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

    # max filename length
    if len(filename) > 99:
        filename = filename[:99]

    if not filename:
        filename = 'Untitled'

    return filename


def download_video(url: str, video_title: str) -> Path:
    # set/make temp dir for download
    temp_dir = Path(tempfile.gettempdir(), 'youtube_to_davinci_resolve')
    try:
        temp_dir.mkdir(exist_ok=True)
    except FileNotFoundError:
        print(
            f"Your temp folder ({temp_dir.parent}) was not found. For caution, the script will not create it. please double check your temp dir and try again.\nExiting script..."
        )
        exit()

    result = subprocess.run([
        'yt-dlp',
        '--format',
        'bv+ba[ext=m4a]/ba[ext=aac]',  # best video + m4a or aac
        '--remux-video',
        'mp4',
        '-P',
        temp_dir,
        '--output',
        f"{video_title}.%(ext)s",
        url,
    ])

    if result.returncode == 0:
        # Find the downloaded file in the temp_dir
        file = list(temp_dir.glob(f"{video_title}*"))[0]
        return file
    else:
        return False
