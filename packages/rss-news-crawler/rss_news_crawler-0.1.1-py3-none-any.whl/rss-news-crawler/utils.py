import re
from difflib import SequenceMatcher

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()