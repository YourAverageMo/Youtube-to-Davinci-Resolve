import subprocess
import re

# TODO move global vars to a json file

UNWANTED_WORDS = [
    'Sound', 'effect', 'for editing', 'editing', '(dl in desc)', '-', '()',
    "''"
]
# yes im using asmongold clip... bite me
TEST_LINK = "https://www.youtube.com/watch?v=Xgf8UBxKii0"


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

    if not filename:
        filename = 'Untitled'

    return filename


def get_link() -> str:
    """gets last item in users clipboard."""
    link = subprocess.getoutput("powershell.exe -Command Get-Clipboard")
    return link
