from youtube_to_davinci_resolve import *

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"

# yt-dlp --remux-video mp4 --format "bv+ba[ext=m4a]/ba[ext=aac]" "https://www.youtube.com/watch?v=xxfl7NCzBAA&pp=ygUIc2Z4IG1lbWU%3D"
'''
yt-dlp commands:

--windows-filenames
--trim-filenames 99
--remux-video mp4
'''


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


file = download_video(TEST_LINK, sanitize_filename(get_video_title(TEST_LINK)))
print(file)
