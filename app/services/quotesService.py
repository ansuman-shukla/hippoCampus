from app.utils.quotes_dict import quotes
import random


def get_quotes():
    return random.choice(quotes)