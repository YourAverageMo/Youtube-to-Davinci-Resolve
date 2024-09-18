from youtube_to_davinci_resolve import *

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"

# current working auto-editor:
# auto-editor "test.m4a" --margin 0s

# current working ffmpeg:
# ffmpeg -i "input.m4a" -c:a libmp3lame -b:a 320k "output.mp3"

# yt-dlp --remux-video mp4 --format "bv+ba[ext=m4a]/ba[ext=aac]" "https://www.youtube.com/watch?v=xxfl7NCzBAA&pp=ygUIc2Z4IG1lbWU%3D"


# TODO in gui make --margin adjustable
# FIXME save into temp folder instead. the converted file goes into save_dir
def trim_video(video_path: Path) -> Path:

    # check if save path exists
    save_dir = SFX_SAVE_DIR if SFX_SAVE_DIR.exists(
    ) else Path().home() / "Downloads"
    # declare save file location, name, & extension
    video_path_trimmed = save_dir / video_path.name

    # run yt-dlp in cmd
    result = subprocess.run(
        [
            'auto-editor',
            video_path.name,
            '--margin',
            '-0.05s,0s',
            '--no-open',
            '--output',
            f"{save_dir / video_path.stem}",
        ],
        cwd=fr"{video_path.parent}",
    )
    if result.returncode == 0:
        return video_path_trimmed



# video_title = get_video_title(TEST_LINK_SFX3)
# is_sfx_in_video_title = is_sfx(video_title)
# video_title = sanitize_filename(video_title)
# video_path_download = download_video(TEST_LINK_SFX3, video_title,
#                                      is_sfx_in_video_title)
# video_path_trimmed = trim_video(video_path_download)
# video_path_converted = convert_sfx(video_path_trimmed)