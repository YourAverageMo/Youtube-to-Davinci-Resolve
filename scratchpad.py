from youtube_to_davinci_resolve import *

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"

# current working auto-editor:
# auto-editor "test.m4a" --margin 0s

# current working ffmpeg:
# ffmpeg -i "input.m4a" -c:a libmp3lame -b:a 320k "output.mp3"

# yt-dlp --remux-video mp4 --format "bv+ba[ext=m4a]/ba[ext=aac]" "https://www.youtube.com/watch?v=xxfl7NCzBAA&pp=ygUIc2Z4IG1lbWU%3D"
'''
yt-dlp commands:

--windows-filenames
--trim-filenames 99
--remux-video mp4
'''


def download_video(url: str, video_title: str, is_sfx: bool = False) -> Path:
    # set/make temp dir for download
    temp_dir = Path(tempfile.gettempdir(), 'youtube_to_davinci_resolve')
    try:
        temp_dir.mkdir(exist_ok=True)
    except FileNotFoundError:
        print(
            f"Your temp folder ({temp_dir.parent}) was not found. For caution, the script will not create it. please double check your temp dir and try again.\nExiting script..."
        )
        exit()

    # determine if clip is sfx
    if is_sfx:
        download_format = 'ba[ext=m4a]/ba[ext=aac]'  # only audio, save space
        print("is sfx")
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
        file = list(temp_dir.glob(f"{video_title}*"))[0]
        return file
    else:
        return False


video_title = get_video_title(TEST_LINK)
download_video(TEST_LINK, video_title, is_sfx(video_title))
