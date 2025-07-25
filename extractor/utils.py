import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = text.strip()
    return text
