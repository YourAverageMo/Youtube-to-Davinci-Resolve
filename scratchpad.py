import tempfile
import subprocess
from pathlib import Path
import yt_dlp

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"


'''
yt-dlp commands:

--windows-filenames
--trim-filenames 99
--remux-video mp4
'''

TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"


def get_video_title(url: str) -> str:
    # Define download options with no actual download
    ydl_opts = {
        'quiet': True,  # Suppress all output
        'noplaylist': True,  # Only get info for a single video
    }

    # Create a YoutubeDL object
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Extract info without downloading

    # Return the title
    return info.get('title', 'No title found')

def download_video(url: str) -> Path:
    # set/make temp dir for download
    temp_dir = Path(tempfile.gettempdir(), 'youtube_to_davinci_resolve')

    try:
        temp_dir.mkdir(exist_ok=True)
    except FileNotFoundError:
        print(
            f"Your temp folder ({temp_dir.parent}) was not found. For caution, the script will not create it. please double check your temp dir and try again.\nExiting script..."
        )
        exit()
    subprocess.run([
        'auto-editor',
        url,
    ], cwd=fr"{temp_dir.parent}")

print(get_video_title(TEST_LINK))

# download_video(TEST_LINK)
