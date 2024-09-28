# create the UI
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# some element IDs
winID = "Youtube Downloader"  # should be unique for single instancing
browseFilesID = "BrowseButton"

# check for existing instance
win = ui.FindWindow(winID)
if win:
    win.Show()
    win.Raise()
    exit()

# window layout
winLayout = ui.VGroup([
    ui.Label({
        'Text': "YouTube Downloader\n by Muhammed Yilmaz",
        'Weight': 1,
        'MinimumSize': [400, 100],
        'Font': ui.Font({
            'PixelSize': 22,
            'Bold': True,
        }),
        'Alignment': {
            'AlignCenter': True
        }
    }),
    ui.HGroup({
        'Weight': 0.0,
        'MinimumSize': [200, 25]
    }, [
        ui.LineEdit({
            'ID': 'FileLineTxt',
            'Text': '',
            'PlaceholderText': 'Video URL',
            'Weight': 0.9
        }),
        ui.Button({
            'ID': 'BrowseButton',
            'Text': 'Browse',
            'Weight': 0.1
        }),
    ]),
    ui.HGroup({
        'Weight': 0.0,
        'MinimumSize': [200, 25]
    }, [
        ui.LineEdit({
            'ID': 'FileLineTxt',
            'Text': '',
            'PlaceholderText': 'Video Save Filepath',
            'Weight': 0.9
        }),
        ui.Button({
            'ID': 'BrowseButton',
            'Text': 'Browse',
            'Weight': 0.1
        }),
    ]),
    ui.HGroup({
        'Weight': 0.0,
        'MinimumSize': [200, 25]
    }, [
        ui.LineEdit({
            'ID': 'FileLineTxt',
            'Text': '',
            'PlaceholderText': 'SFX Save Filepath',
            'Weight': 0.9
        }),
        ui.Button({
            'ID': 'BrowseButton',
            'Text': 'Browse',
            'Weight': 0.1
        }),
    ]),
    ui.HGroup({'Weight': 5}, [
        ui.Button({
            'ID': "myButton1",
            'Text': "Go"
        }),
        ui.Button({
            'ID': "myButton2",
            'Text': "Stop"
        }),
    ]),
    ui.VGap(2),
    ui.HGroup({'Weight': 5}, [
        ui.Button({
            'ID': "myButtonA",
            'Text': "Begin"
        }),
        ui.Button({
            'ID': "myButtonB",
            'Text': "End"
        }),
    ]),
]),

win = dispatcher.AddWindow({'ID': winID}, winLayout)
itm = win.GetItems()


# window events
def OnClose(ev):
    dispatcher.ExitLoop()


def OnBrowseFiles(ev):
    selectedPath = fusion.RequestDir()
    if selectedPath:
        itm['FileLineTxt'].Text = str(selectedPath)


# event handlers
win.On[winID].Close = OnClose
win.On[browseFilesID].Clicked = OnBrowseFiles

win.Show()
dispatcher.RunLoop()
