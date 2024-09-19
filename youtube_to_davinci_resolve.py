import subprocess
import re
import tempfile
from pathlib import Path
import yt_dlp

# NOTE auto-editor doesnt seem to play nice with audio files unless you use your own ffmpeg path. so to keep this script user friendly workflow for sfx will be: download video with only audio as a video file > run auto-editor on it returning a video file > ffmpeg convert to mp3
# TODO delete_file() function.
# TODO emojis in video_title may cause issues. keep an eye on it
# TODO move global vars to a json file
# TODO before that convert global vars to dict so its easier to incorporate json later
# TODO add hd and variants to 👇🏽
UNWANTED_WORDS = [
    'sound', 'effect', 'for editing', 'editing', '(dl in desc)', '-', '()',
    "''", '.'
]
SFX_KEYWORDS = [
    'sfx',
    'sound effect',
    'sound effects',
]
# yes im using an asmongold clip... bite me
TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"
TEST_LINK_SFX = "https://www.youtube.com/watch?v=X_-_AMdA4eE&list=PL41KByPmtbD7Jdoe7bH8gqobDCMin4x4H&index=2"
TEST_LINK_SFX2 = "https://www.youtube.com/watch?v=_98eA_BZZB0&list=PLGJIkLnskxQNfvMPkaRmb8KQLF3qb9Qoz&index=10"
TEST_LINK_SFX3 = "https://www.youtube.com/watch?v=Rk74KCkSCnM&list=PLGJIkLnskxQNfvMPkaRmb8KQLF3qb9Qoz&index=8"
AUTO_DELETE_TEMP = False
SFX_TRIM_MARGIN = {
    'aggressive': '-0.05s,0s',
    'standard': '0s,0s',
    'loose': '0.5s,0.5s',
}
SFX_SAVE_DIR = Path(
    r"D:\Editing Stuff\SFX\Meme sound Clips, Mario, Cartoon Sounds, Funny Etc\Recent"
)


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


def download_video(url: str, video_title: str, is_sfx: bool = False) -> Path:
    if is_sfx:
        download_format = 'ba[ext=m4a]/ba[ext=aac]'  # only audio, save space
    else:
        download_format = 'bv+ba[ext=m4a]/ba[ext=aac]'  # best video + m4a or aac

    # run yt-dlp in cmd
    result = subprocess.run([
        'yt-dlp',
        '--no-playlist',  # currently no playlists maybe future
        '--format',
        download_format,
        '--remux-video',
        'mp4',
        '-P',
        temp_dir,
        '--output',
        f"{video_title}.%(ext)s",
        url,
    ])

    # find file and return it
    if result.returncode == 0:
        # Find the downloaded file in the temp_dir
        video_path_download = list(temp_dir.glob(f"{video_title}*"))[0]
        return video_path_download
    else:
        return False


# TODO in gui make --margin adjustable
# FIXME save into temp folder instead. the converted file goes into save_dir
def trim_video(video_path: Path) -> Path:
    # input video and trimmed video will have same name so put it into diff dir
    # declare save file location, name, & extension.
    trimmed_dir = temp_dir / "trimmed"
    trimmed_dir.mkdir(exist_ok=True)
    # run yt-dlp in cmd
    result = subprocess.run(
        [
            'auto-editor',
            video_path.name,
            '--margin',
            '-0.05s,0s',
            '--no-open',
            '--output',
            f"{trimmed_dir / video_path.stem}",  # exclude ext
        ],
        cwd=fr"{video_path.parent}",
    )

    if result.returncode == 0:
        video_path_trimmed = trimmed_dir / video_path.name
        return video_path_trimmed


def convert_sfx(video_path: Path) -> Path:
    # declare save file location, name, & extension
    video_path_converted = sfx_save_dir / f"{video_path.stem}.mp3"

    # run ffmpeg in cmd
    result = subprocess.run(
        [
            'ffmpeg', '-i', video_path.name, '-c:a', 'libmp3lame', '-b:a',
            '320k',
            str(video_path_converted)
        ],
        cwd=fr"{video_path.parent}",
    )
    if result.returncode == 0:
        return video_path_converted


# set/make temp dir for download
try:
    temp_dir = Path(tempfile.gettempdir(), 'youtube_to_davinci_resolve')
    temp_dir.mkdir(exist_ok=True)
except FileNotFoundError:
    print(
        f"Your temp folder ({temp_dir.parent}) was not found. For caution, the script will not create it. please double check your temp dir and try again.\nExiting script..."
    )
    exit()

# check if save path exists
sfx_save_dir = SFX_SAVE_DIR if SFX_SAVE_DIR.exists(
) else Path().home() / "Downloads"
