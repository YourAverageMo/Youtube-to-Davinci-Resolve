# create the UI
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# element IDs
win_id = 'youtube_importer'
coffee_button = 'coffee_button'
start_button = 'start_button'
url_input = 'url_box'
sfx_dir_input = 'sfx_dir_input'
sfx_browse_button = 'sfx_browse_button'
auto_delete_check = 'auto_delete_check'
save_to_project_check = 'save_to_project_check'
trim_margin_dropdown = 'trim_margin_dropdown'
skip_ui = 'skip_ui'
unwanted_words_input = 'unwanted_words_input'
sfx_keywords = 'sfx_keywords'

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
        'ID': 'DialogBox',
        'Text': "YouTube Importer\nby Muhammed Yilmaz",
        'Weight': 0,
        'Font': ui.Font({
            'PixelSize': 24,
            'Italic': True,
            'Bold': True,
        }),
        'Alignment': {
            'AlignHCenter': True
        }
    }),
    ui.Button({
        'ID': coffee_button,
        'Text':
        'If this plugin is useful and want to support me, consider buying me a coffee :)',
        'Weight': 0,
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
        'Text': "Enter the full YouTube video URL",
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
        'Text': "Directory to save downloaded sound effects",
        'Font': ui.Font({'PixelSize': 9}),
        'Weight': 0,
    }),
    ui.HGroup({'Weight': 0}, [
        ui.LineEdit({
            'ID': sfx_dir_input,
            'PlaceholderText': 'Choose save directory',
            'Weight': 0.9
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
            'Text': 'Auto Delete Temp Files'
        }),
        ui.CheckBox({
            'ID': save_to_project_check,
            'Text': 'Save to Project Folder'
        }),
        ui.Label({
            'Text': "SFX Trim Margin:",
            'Weight': 0.1
        }),
        ui.ComboBox({
            'ID': trim_margin_dropdown,
            'Items': ['No Trim', '0.5 seconds', '1 second'],
            'Weight': 0.9
        })
    ]),
    ui.CheckBox({
        'ID': skip_ui,
        'Text':
        "Skip this window? Warning to undo this you will have to change it in the settings file.",
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
                'Text': "Comma-separated words to exclude",
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
                'Text': "Enter keywords to search for sound effects",
                'Font': ui.Font({'PixelSize': 9}),
                'Weight': 0,
            }),
            ui.TextEdit({
                'ID': sfx_keywords,
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
        'Geometry': [20, 50, 600, 550],
    }, winLayout)
itm = win.GetItems()


# window events
def OnClose(ev):
    dispatcher.ExitLoop()


def OnBrowseSFX(ev):
    selectedPath = fusion.RequestDir()
    if selectedPath:
        itm[sfx_dir_input].Text = str(selectedPath)


# event handlers
win.On[win_id].Close = OnClose
win.On[sfx_browse_button].Clicked = OnBrowseSFX

# Show window
win.Show()
dispatcher.RunLoop()
