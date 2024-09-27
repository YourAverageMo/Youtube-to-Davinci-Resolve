# from youtube_to_davinci_resolve import *

# auto-editor "https://www.youtube.com/watch?v=oaiQ5hYKHTE" --margin 0s -o "output" --extras "-c:a libmp3lame -b:a 320k"

# current working auto-editor:
# auto-editor "test.m4a" --margin 0s

# current working ffmpeg:
# ffmpeg -i "input.m4a" -c:a libmp3lame -b:a 320k "output.mp3"

# yt-dlp --remux-video mp4 --format "bv+ba[ext=m4a]/ba[ext=aac]" "https://www.youtube.com/watch?v=xxfl7NCzBAA&pp=ygUIc2Z4IG1lbWU%3D"


# create the UI
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# some element IDs
winID = "Youtube Downloader"  # should be unique for single instancing

# check for existing instance
win = ui.FindWindow(winID)
if win:
    win.Show()
    win.Raise()
    exit()

# otherwise, we set up a new window
# win = dispatcher.AddWindow(
#     {
#         'ID': winID,
#         'WindowTitle': winID,
#     },
#     ui.VGroup(
#         {
#             'ID': 'root',
#         },
#         [
#             ui.HGroup({'Weight': 1.0}, [
#                 ui.HGap(4),
#                 ui.Label({
#                     'Text': "YouTube Downloader by Muhammed Yilmaz",
#                     'Weight': 0,
#                     'Font': ui.Font({
#                         'PixelSize': 22,
#                         'Bold': True
#                     })
#                 }),
#             ])
#         ],
#     ),
# )

winLayout = ui.VGroup([
    ui.Label({
        'Text': "A 2x2 grid of buttons",
        'Weight': 1,
        'Font': ui.Font({
            'PixelSize': 22,
            'Bold': True,
        }),
        'Alignment': {
            'AlignCenter': True
        }
    }),
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


def OnClose(ev):
    dispatcher.ExitLoop()


win.On[winID].Close = OnClose

win.Show()
dispatcher.RunLoop()
