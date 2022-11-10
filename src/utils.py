import random

from src import MISSING_LYRICS_MESSAGES


def get_missing_lyrics_message():
    return random.choice(MISSING_LYRICS_MESSAGES)
