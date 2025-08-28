import re


def is_english(text):
    # Count how many characters are A-Z or a-z
    english_chars = re.findall(r'[A-Za-z]', text)
    ratio = len(english_chars) / max(len(text), 1)
    return ratio > 0.6  # 60% of chars are English