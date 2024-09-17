import re
import os

# TODO move global vars to a json file

UNWANTED_WORDS = [
    'Sound', 'effect', 'for editing', 'editing', '(dl in desc)', '-', '()',
    "''"
]
TEST_TITLES = [
    "Ryūjin no ken wo kurae (Overwatch Genji Ultimate Meme) - Sound Effect for editing ''",
    "VALORANT FAKE DEFUSE - SOUND EFFECT",
    "CSGO HIT AND DEATH SOUNDS (DL IN DESC)"
]


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


for title in TEST_TITLES:
    sanitized = sanitize_filename(title)
    print(f"Original: {title}")
    print(f"Sanitized: {sanitized}")
    print()
