import re

def clean_text(text: str) -> str:
    """
    Lowercase the text, remove non-letter characters,
    and normalize spaces.
    """
    if not isinstance(text, str):
        text = str(text)  # ✅ ensure input is always a string
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)   # keep only letters and spaces
    text = re.sub(r"\s+", " ", text)           # collapse multiple spaces
    return text.strip()

def normalize(score: float) -> float:
    """
    Normalize a similarity score (0–1) into a percentage (0–100),
    rounded to two decimal places.
    """
    try:
        return round(float(score) * 100, 2)    # ✅ cast to float for safety
    except (TypeError, ValueError):
        return 0.0

