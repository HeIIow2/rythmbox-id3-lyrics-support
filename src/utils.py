import random

MISSING_LYRICS_MESSAGES = [
    "Nobody here but us chickens! :3"
]


def get_missing_lyrics_message():
    return random.choice(MISSING_LYRICS_MESSAGES)
