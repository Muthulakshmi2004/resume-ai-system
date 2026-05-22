import re
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    if hasattr(file, "stream"):
        doc = fitz.open(stream=file.stream.read(), filetype="pdf")
    elif isinstance(file, str):
        doc = fitz.open(file)
    else:
        raise TypeError("Unsupported file type")
    text = ""
    for page in doc:
        text += page.get_text()
    return text or ""

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text: str):
    doc = nlp(text)
    return list(set([
        token.lemma_ for token in doc
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.lemma_) > 2
    ]))

def parse_resume(file):
    text = extract_text_from_pdf(file)
    clean = clean_text(text)
    keys = extract_keywords(text)
    return {"raw_text": text, "cleaned_text": clean, "keywords": keys}
