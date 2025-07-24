from PyPDF2 import PdfReader
from .utils import clean_text, detect_heading_level
import re

def extract_headings(pdf_path):
    reader = PdfReader(pdf_path)
    outline = []

    for page_number, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
        except:
            continue

        if not text:
            continue

        lines = text.split('\n')
        for line in lines:
            cleaned = clean_text(line)
            if not cleaned:
                continue

            # Skip long body lines or sentences
            if cleaned.endswith('.') or len(cleaned.split()) > 12:
                continue

            # Match structured patterns first
            if re.match(r'(Section|Chapter)\s+\d+(\.\d+)*:?', cleaned):
                level = detect_heading_level(cleaned)
                outline.append({
                    "level": level,
                    "text": cleaned,
                    "page": page_number
                })

            # Fallback: detect generic headings like "Introduction", "Objectives", etc.
            elif (cleaned.istitle() or cleaned.isupper()) and len(cleaned.split()) <= 5:
                outline.append({
                    "level": "H1",  # default level
                    "text": cleaned,
                    "page": page_number
                })

    return outline
