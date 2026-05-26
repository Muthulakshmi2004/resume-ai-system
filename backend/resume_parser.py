import re
import fitz  # PyMuPDF
import spacy

# -----------------------------
# Load spaCy safely
# -----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = spacy.blank("en")


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file):
    try:
        if hasattr(file, "stream"):
            doc = fitz.open(stream=file.stream.read(), filetype="pdf")
        elif isinstance(file, str):
            doc = fitz.open(file)
        else:
            raise TypeError("Unsupported file type")

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()

    except Exception as e:
        print("PDF extraction error:", e)
        return ""


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Extract keywords
# -----------------------------
def extract_keywords(text: str):
    try:
        doc = nlp(text)

        keywords = [
            token.lemma_
            for token in doc
            if token.is_alpha
            and not token.is_stop
            and token.pos_ in ["NOUN", "PROPN"]
            and len(token.lemma_) > 2
        ]

        return list(set(keywords))

    except Exception as e:
        print("Keyword extraction error:", e)
        return []


# -----------------------------
# Main parser
# -----------------------------
def parse_resume(file):
    text = extract_text_from_pdf(file)

    cleaned = clean_text(text)
    keywords = extract_keywords(text)

    return {
        "raw_text": text,
        "cleaned_text": cleaned,
        "keywords": keywords
    }