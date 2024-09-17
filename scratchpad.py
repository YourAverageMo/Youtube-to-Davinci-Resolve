from youtube_to_davinci_resolve import *

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"
'''
yt-dlp commands:

--windows-filenames
--trim-filenames 99
--remux-video mp4
'''


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

    # TODO download video




download_video(TEST_LINK)
