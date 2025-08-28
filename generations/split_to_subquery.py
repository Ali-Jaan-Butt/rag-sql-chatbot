import re


def split_into_subqueries(message):
    # Splits message into multiple parts if it has "and", "also", etc.
    separators = [" and ", " also ", " plus ", " as well as "]
    pattern = "|".join(map(re.escape, separators))
    parts = re.split(pattern, message)
    return [p.strip() for p in parts if p.strip()]