import subprocess
import re
import tempfile
from pathlib import Path
import yt_dlp
from collections import Counter

# NOTE auto-editor doesnt seem to play nice with audio files unless you use your own ffmpeg path. so to keep this script user friendly workflow for sfx will be: download video with only audio as a video file > run auto-editor on it returning a video file > ffmpeg convert to mp3
# TODO use IS_GUESS_PROJECT_FOLDER
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
TEST_LINK2 = "https://www.youtube.com/watch?v=qLGxQBEd948"
AUTO_DELETE_TEMP = True
SFX_TRIM_MARGIN = {
    'aggressive': '-0.05s,0s',
    'standard': '0s,0s',
    'loose': '0.5s,0.5s',
}
SFX_SAVE_DIR = Path(
    r"D:\Editing Stuff\SFX\Meme sound Clips, Mario, Cartoon Sounds, Funny Etc\Recent"
)

IS_GUESS_PROJECT_FOLDER = False


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
        save_dir = temp_dir
    else:
        download_format = 'bv+ba[ext=m4a]/ba[ext=aac]'  # best video + m4a or aac
        save_dir = temp_dir

    # delete file if already exists. i know... bite me
    some_random_variable_name = save_dir / video_title
    for some_random_variable_name in save_dir.glob(f"{video_title}*"):
        some_random_variable_name.unlink()
        print(f"Deleted file: {some_random_variable_name}")

    # run yt-dlp in cmd
    result = subprocess.run([
        'yt-dlp',
        '--no-playlist',  # currently no playlists maybe future
        '--format',
        download_format,
        '--remux-video',
        'mp4',
        '-P',
        save_dir,
        '--output',
        f"{video_title}.%(ext)s",
        url,
    ])

    # find file and return it
    if result.returncode == 0:
        video_path_download = list(save_dir.glob(f"{video_title}*"))[0]
        return video_path_download
    else:
        return False


# TODO in gui make --margin adjustable
def trim_sfx(video_path: Path) -> Path:
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


def convert_video(video_path: Path) -> Path:
    # declare save file location, name, & extension
    video_path_converted = download_dir / f"{video_path.stem}.mp4"

    # run ffmpeg in cmd
    result = subprocess.run(
        [
            'ffmpeg', '-i', video_path.name, '-c:v', 'libx264', '-c:a', 'aac',
            str(video_path_converted)
        ],
        cwd=fr"{video_path.parent}",
    )
    if result.returncode == 0:
        return video_path_converted


def convert_sfx(video_path: Path) -> Path:
    # declare save file location, name, & extension
    video_path_converted = SFX_SAVE_DIR / f"{video_path.stem}.mp3"

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


def delete_temp_files():
    for item in temp_dir.rglob('*'):
        if item.is_file():
            try:
                item.unlink()
                print(f"Deleted temp item: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")


def guess_project_path():
    try:
        timeline_track_list = current_timeline.GetItemListInTrack("audio",
                                                                  1)[:10]
        filepaths = []

        # get all none empty file paths in first 10 timeline audio tracks
        for track in timeline_track_list:
            try:
                track_path = track.GetMediaPoolItem().GetClipProperty(
                    f'File Path')
                if track_path != '':
                    filepaths.append(track_path)
            except AttributeError:
                print('AttributeError found, skipping timeline item')
                continue
    except IndexError:
        print('no timeline active')
        pass
    if not filepaths:
        return None
    else:
        most_common_file = Counter(filepaths).most_common(1)[0][0]
        return Path(most_common_file).parent


def import_to_resolve(video_path: Path, is_sfx: bool) -> bool:
    media_pool.SetCurrentFolder(root_folder)
    sfx_or_youtube = 'sfx' if is_sfx else 'youtube'

    # search for proper import folder
    for folder in folders:
        folder_name = folder.GetName()
        if folder_name.lower() == sfx_or_youtube:
            media_pool.SetCurrentFolder(folder)
            break
    # if folder doesn't exist make one
    else:  # no if statement. leave outside of for loop
        media_pool.AddSubFolder(root_folder, sfx_or_youtube)

    # import file
    media_pool.ImportMedia([str(video_path)])


# Legacy code. moved temp to Downloads/Youtube/Temp
# set/make temp dir for download
'''
try:
    temp_dir = Path(tempfile.gettempdir(), 'youtube_to_davinci_resolve')
    temp_dir.mkdir(exist_ok=True)
except FileNotFoundError:
    print(
        f"Your temp folder ({temp_dir.parent}) was not found. For caution, the script will not create it. please double check your temp dir and try again.\nExiting script..."
    )
    exit()
'''

download_dir = Path().home() / "Downloads" / "Youtube"
download_dir.mkdir(exist_ok=True)

# set/make temp dir for download
temp_dir = download_dir / "Temp"
temp_dir.mkdir(exist_ok=True)

# input video and trimmed video will have same name so put it into diff dir
trimmed_dir = temp_dir / "trimmed"
trimmed_dir.mkdir(exist_ok=True)

# check if save path exists
SFX_SAVE_DIR = SFX_SAVE_DIR if SFX_SAVE_DIR.exists() else download_dir

is_resolve = False
try:
    # Attempt to get the DaVinci Resolve API object
    resolve = app.GetResolve()
    is_resolve = True
    if resolve:
        print("Script is running inside DaVinci Resolve.")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        media_pool = project.GetMediaPool()
        root_folder = media_pool.GetRootFolder()
        folders = root_folder.GetSubFolderList()
        clips = root_folder.GetClipList()
        current_timeline = project.GetCurrentTimeline()
        project_path = guess_project_path()

except NameError:
    print("Script not running inside DaVinci Resolve.")
    resolve = None

# url = get_clipboard()
url = TEST_LINK_SFX
try:
    video_title = get_video_title(url)
except:
    print(f"Invalid url")
    exit()

is_sfx_in_video_title = is_sfx(video_title)
video_title = sanitize_filename(video_title)

video_path_download = download_video(url, video_title, is_sfx_in_video_title)
if is_sfx_in_video_title:
    video_path_trimmed = trim_sfx(video_path_download)
    video_path_download = convert_sfx(video_path_trimmed)
else:
    # ran out of video_path_.... names :)
    video_path_download = convert_video(video_path_download)
if AUTO_DELETE_TEMP:
    delete_temp_files()

if is_resolve:
    import_to_resolve(video_path_download, is_sfx_in_video_title)

print("---")
print("Done")
