import subprocess
import re
from pathlib import Path
import yt_dlp
from collections import Counter
import json

# NOTE auto-editor doesnt seem to play nice with audio files unless you use your own ffmpeg path. so to keep this script user friendly workflow for sfx will be: download video with only audio as a video file > run auto-editor on it returning a video file > ffmpeg convert to mp3

# TODO emojis in video_title may cause issues. keep an eye on it

# yes im using an asmongold clip... bite me
TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"
TEST_LINK_SFX = "https://www.youtube.com/watch?v=X_-_AMdA4eE&list=PL41KByPmtbD7Jdoe7bH8gqobDCMin4x4H&index=2"
TEST_LINK_SFX2 = "https://www.youtube.com/watch?v=_98eA_BZZB0&list=PLGJIkLnskxQNfvMPkaRmb8KQLF3qb9Qoz&index=10"
TEST_LINK_SFX3 = "https://www.youtube.com/watch?v=Rk74KCkSCnM&list=PLGJIkLnskxQNfvMPkaRmb8KQLF3qb9Qoz&index=8"
TEST_LINK2 = "https://www.youtube.com/watch?v=qLGxQBEd948"


def load_settings():
    settings_file = download_dir / "settings.json"
    # use settings file if it exists
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        # abort if syntax error to preserve user settings
        except json.decoder.JSONDecodeError:
            print(
                "error loading user settings (syntax error), please correct settings.json or delete the file and rerun to use default settings"
            )
            print("aborting script...")
            exit()

    # save default settings to file
    else:
        settings = {
            # TODO add 👇🏽 hd and variants, popular, meme, free, free to use
            "UNWANTED_WORDS": [
                "sound", "effect", "for editing", "editing", "(dl in desc)",
                "-", "()", "''", "."
            ],
            "SFX_KEYWORDS": ["sfx", "sound effect", "sound effects"],
            # 0 "loose": "0.5s,0.5s"
            # 1 "standard": "0s,0s",
            # 2 "aggressive": "-0.05s,0s",
            "SFX_TRIM_MARGIN":
            2,
            "SFX_SAVE_DIR":
            "D:/Editing Stuff/SFX/Meme sound Clips, Mario, Cartoon Sounds, Funny Etc/Recent",
            "AUTO_DELETE_TEMP":
            True,
            "SAVE_TO_PROJECT_FOLDER":
            True,
            "SKIP_GUI":
            False,
        }
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    # set global settings
    # i think its neater to use globals here than to have these in the main loop
    global UNWANTED_WORDS
    global SFX_KEYWORDS
    global SFX_TRIM_MARGIN
    global SFX_SAVE_DIR
    global AUTO_DELETE_TEMP
    global SAVE_TO_PROJECT_FOLDER
    global SKIP_GUI

    try:
        UNWANTED_WORDS = settings["UNWANTED_WORDS"]
        SFX_KEYWORDS = settings["SFX_KEYWORDS"]
        SFX_TRIM_MARGIN = settings["SFX_TRIM_MARGIN"]
        SFX_SAVE_DIR = Path(settings["SFX_SAVE_DIR"])
        AUTO_DELETE_TEMP = settings["AUTO_DELETE_TEMP"]
        SAVE_TO_PROJECT_FOLDER = settings["SAVE_TO_PROJECT_FOLDER"]
        SKIP_GUI = settings["SKIP_GUI"]
    except KeyError:
        print(
            "error loading user settings (missing setting), please correct settings.json or delete the file and rerun to use default settings"
        )
        print("aborting script...")
        exit()

    # cleaning memory
    del settings

    return True


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
    filename = re.sub(r'[^a-zA-Z0-9\s]', '', filename)

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
        download_format = 'bv*[ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=aac]/b[ext=mp4]'  # best video + m4a or aac
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
    if SAVE_TO_PROJECT_FOLDER and is_resolve and project_path is not None:
        video_path_converted = project_path / f"{video_path.stem}.mp4"
    else:
        video_path_converted = download_dir / f"{video_path.stem}.mp4"

    # run ffmpeg in cmd
    result = subprocess.run(
        [
            'ffmpeg', '-i', video_path.name, '-c:v', 'libx264', '-preset',
            'fast', '-c:a', 'aac',
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
        return None
    except AttributeError:
        print('no timeline active')
        return None
    if not filepaths:
        return None
    else:
        most_common_file = Counter(filepaths).most_common(1)[0][0]
        return Path(most_common_file).parent


def import_to_resolve(video_path: Path, is_sfx: bool) -> bool:
    media_pool.SetCurrentFolder(root_folder)
    sfx_or_youtube = 'sfx' if is_sfx else 'youtube'

    # search for proper bin in davinci resolve
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

# --
# -- GUI building starts here
# --


def open_user_interface():

    # element IDs
    win_id = 'main_window'
    coffee_button = 'coffee_button'
    start_button = 'start_button'
    url_input = 'url_box'
    sfx_dir_input = 'sfx_dir_input'
    sfx_browse_button = 'sfx_browse_button'
    auto_delete_check = 'auto_delete_check'
    save_to_project_check = 'save_to_project_check'
    trim_margin_dropdown = 'trim_margin_dropdown'
    skip_gui_check = 'skip_ui'
    unwanted_words_input = 'unwanted_words_input'
    sfx_keywords_input = 'sfx_keywords'

    # check for existing instance
    win = ui.FindWindow(win_id)
    if win:
        win.Show()
        win.Raise()
        exit()

    # window layout
    winLayout = ui.VGroup([
        # shameless plug section
        ui.Label({
            'ID':
            'DialogBox',
            'Text':
            "YouTube Importer\nby Muhammed Yilmaz",
            'Weight':
            0,
            'Font':
            ui.Font({
                'PixelSize': 24,
                'Italic': True,
                'Bold': True,
            }),
            'Alignment': {
                'AlignHCenter': True
            },
            'StyleSheet':
            'QLabel { color: white; }',
        }),
        ui.Button({
            'ID': coffee_button,
            'Text':
            'If this plugin is useful and want to support me, consider buying me a coffee :)',
            'Weight': 0,
            'StyleSheet': 'QPushButton { color: #f1f17b; }'
        }),
        ui.VGap(5),

        # Video URL Section
        ui.Label({
            'Text': "Video URL:",
            'Font': ui.Font({
                'PixelSize': 16,
                'Bold': True,
            }),
            'Weight': 0,
        }),
        ui.Label({
            'Text':
            "Enter the full YouTube video URL. (This field is auto populated with your clipboard on launch)",
            'Font': ui.Font({'PixelSize': 9}),
            'Weight': 0,
        }),
        ui.LineEdit({
            'ID': url_input,
            'PlaceholderText': 'Enter YouTube URL',
            'Weight': 0,
        }),

        # start button
        ui.Button({
            'ID': start_button,
            'Text': 'START',
            'Font': ui.Font({
                'PixelSize': 16,
                'Bold': True
            }),
            'Weight': 0
        }),
        ui.VGap(5),

        # Advanced Settings Header
        ui.Label({
            'Text': "Advanced Settings",
            'Font': ui.Font({
                'PixelSize': 16,
                'Bold': True,
            }),
            'Weight': 0,
        }),
        ui.VGap(2),

        # SFX Save Directory Section
        ui.Label({
            'Text': "SFX Save Directory:",
            'Weight': 0,
        }),
        ui.Label({
            'Text':
            "Directory to save downloaded sound effects (Bypasses `Save To Project folder`)",
            'Font': ui.Font({'PixelSize': 9}),
            'Weight': 0,
        }),
        ui.HGroup({'Weight': 0}, [
            ui.LineEdit({
                'ID': sfx_dir_input,
                'PlaceholderText': 'Choose save directory',
                'Weight': 0.9,
                'Enabled': False
            }),
            ui.Button({
                'ID': sfx_browse_button,
                'Text': 'Browse',
                'Weight': 0.1
            })
        ]),
        ui.VGap(2),

        # Checkboxes Section
        ui.HGroup({'Weight': 0}, [
            ui.CheckBox({
                'ID': auto_delete_check,
                'Text': 'Auto Delete Temp Files?',
                'Weight': 0.1
            }),
            ui.HGap(50),
            ui.Label({
                'Text': "SFX Trim Margin:",
                'Weight': 0.1
            }),
            ui.ComboBox({
                'ID': trim_margin_dropdown,
                'Weight': 0.8
            })
        ]),
        ui.CheckBox({
            'ID': save_to_project_check,
            'Text':
            'Save to Project Folder? (Most common location of the first 10 timeline clips).',
            'Weight': 0
        }),
        ui.CheckBox({
            'ID': skip_gui_check,
            'Text':
            "Skip this window? (Warning to undo this you will have to change the settings file.)",
            'Weight': 0
        }),
        ui.VGap(2),

        # Unwanted Words and SFX Keywords Section
        ui.HGroup([
            ui.VGroup([
                ui.Label({
                    'Text': "Unwanted Words:",
                    'Weight': 0,
                }),
                ui.Label({
                    'Text':
                    "Comma-separated words to remove from final filename",
                    'Font': ui.Font({'PixelSize': 9}),
                    'Weight': 0,
                }),
                ui.TextEdit({
                    'ID': unwanted_words_input,
                    'PlaceholderText': 'Enter words to exclude',
                    'Weight': 1,
                }),
            ],
                      Weight=1),
            ui.VGroup([
                ui.Label({
                    'Text': "SFX Keywords:",
                    'Weight': 0,
                }),
                ui.Label({
                    'Text':
                    "Comma-separated keywords in video title to identify as SFX",
                    'Font': ui.Font({'PixelSize': 9}),
                    'Weight': 0,
                }),
                ui.TextEdit({
                    'ID': sfx_keywords_input,
                    'PlaceholderText': 'Enter SFX keywords',
                    'Weight': 1,
                }),
            ], )
        ]),
    ])

    #  create window and get items
    win = dispatcher.AddWindow(
        {
            'ID': win_id,
            'WindowTitle': "YouTube Importer by Muhammed Yilmaz",
            'Geometry': [20, 50, 550, 550],
        }, winLayout)
    itm = win.GetItems()

    # populate fields
    itm[trim_margin_dropdown].AddItem("Loose")
    itm[trim_margin_dropdown].AddItem("Standard")
    itm[trim_margin_dropdown].AddItem("Aggressive")
    itm[trim_margin_dropdown].CurrentIndex = SFX_TRIM_MARGIN
    itm[unwanted_words_input].SetPlainText(', '.join(UNWANTED_WORDS))
    itm[sfx_keywords_input].SetPlainText(', '.join(SFX_KEYWORDS))
    itm[sfx_dir_input].Text = str(SFX_SAVE_DIR)
    itm[auto_delete_check].Checked = AUTO_DELETE_TEMP
    itm[save_to_project_check].Checked = SAVE_TO_PROJECT_FOLDER
    itm[skip_gui_check].Checked = SKIP_GUI
    itm[url_input].Text = url

    # window events
    def save_settings():
        # save settings
        settings_file = download_dir / "settings.json"
        settings = {
            "UNWANTED_WORDS": [],
            "SFX_KEYWORDS": [],
            "SFX_TRIM_MARGIN": itm[trim_margin_dropdown].CurrentIndex,
            "SFX_SAVE_DIR": itm[sfx_dir_input].Text,
            "AUTO_DELETE_TEMP": itm[auto_delete_check].Checked,
            "SAVE_TO_PROJECT_FOLDER": itm[save_to_project_check].Checked,
            "SKIP_GUI": itm[skip_gui_check].Checked,
        }

        # if text is not empty
        if itm[sfx_keywords_input].PlainText:
            # sorry hard to read. split() text by ',' then strip() then list
            settings["SFX_KEYWORDS"] = [
                word.strip()
                for word in itm[sfx_keywords_input].PlainText.split(',')
            ]

        # if text is not empty
        if itm[unwanted_words_input].PlainText:
            # sorry hard to read. split() text by ',' then strip() then list
            settings["UNWANTED_WORDS"] = [
                word.strip()
                for word in itm[unwanted_words_input].PlainText.split(',')
            ]

        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

        return True

    def on_close(ev):
        save_settings()
        dispatcher.ExitLoop()
        exit()

    def on_browse_sfx(ev):
        selectedPath = fusion.RequestDir()
        if selectedPath:
            itm[sfx_dir_input].Text = str(selectedPath)

    def on_start(ev):
        # i no global url... deal with it.
        global url
        url = itm[url_input].Text
        save_settings()
        load_settings()
        dispatcher.ExitLoop()

    def on_coffee_button(ev):
        import webbrowser
        webbrowser.open("https://www.youtube.com")

    # event handlers
    win.On[win_id].Close = on_close
    win.On[sfx_browse_button].Clicked = on_browse_sfx
    win.On[start_button].Clicked = on_start
    win.On[coffee_button].Clicked = on_coffee_button

    # Show window
    win.Show()
    dispatcher.RunLoop()


# --
# -- Main loop starts here
# --

download_dir = Path().home() / "Downloads" / "Youtube"
download_dir.mkdir(exist_ok=True)

# set/make temp dir for download
temp_dir = download_dir / "Temp"
temp_dir.mkdir(exist_ok=True)

# input video and trimmed video will have same name so put it into diff dir
trimmed_dir = temp_dir / "trimmed"
trimmed_dir.mkdir(exist_ok=True)

load_settings()

# check if save path exists
# TODO i might have to change below to create SFX_SAVE_DIR instead
SFX_SAVE_DIR = SFX_SAVE_DIR if SFX_SAVE_DIR.exists() else download_dir

url = get_clipboard()

is_resolve = False
try:
    # Attempt to get the DaVinci Resolve API object
    resolve = app.GetResolve()
    is_resolve = True
    if resolve:
        print("Script is running inside DaVinci Resolve.")
        if SKIP_GUI:
            # i no nested if statement... bite me.
            print(
                f'Skipping user interface, to re-enable set SKIP_GUI to false in settings.json at {download_dir}'
            )
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        media_pool = project.GetMediaPool()
        root_folder = media_pool.GetRootFolder()
        folders = root_folder.GetSubFolderList()
        clips = root_folder.GetClipList()
        current_timeline = project.GetCurrentTimeline()
        project_path = guess_project_path()
        ui = fusion.UIManager
        dispatcher = bmd.UIDispatcher(ui)

except NameError:
    print("Script not running inside DaVinci Resolve.")
    resolve = None

if resolve and not SKIP_GUI:
    # open_user_interface is just a way of loading and saving settings. ezpz
    open_user_interface()

print('Fetching video title...')
try:
    video_title = get_video_title(url)
except:
    print(f"Invalid url")
    exit()

print('Checking for SFX keywords in title...')
is_sfx_in_video_title = is_sfx(video_title)
video_title = sanitize_filename(video_title)

video_path_download = download_video(url, video_title, is_sfx_in_video_title)
if is_sfx_in_video_title:
    print('SFX Keyword found in title, processing to trim and convert...')
    video_path_trimmed = trim_sfx(video_path_download)
    video_path_download = convert_sfx(video_path_trimmed)
else:
    print('No SFX Keyword found in title, processing to convert...')
    # ran out of video_path_.... names :)
    video_path_download = convert_video(video_path_download)
if AUTO_DELETE_TEMP:
    print('`Auto Delete Temp Files` enabled, deleting temp files')
    delete_temp_files()

if is_resolve:
    print('Importing file...')
    import_to_resolve(video_path_download, is_sfx_in_video_title)

print("---")
print(
    "Aaaannnd thats that! Hopefully it worked, happy editing. Remember if you wanna support me I love coffee!"
)
