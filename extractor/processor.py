import fitz  # PyMuPDF
import re
from .utils import clean_text

def detect_heading_level(text, font_size):
    """Heuristic based on font size and patterns"""
    if re.match(r'(Section|Chapter)\s+\d+(\.\d+)*', text):
        depth = text.count('.')
        return f"H{depth + 1}" if depth else "H1"
    elif font_size >= 16:
        return "H1"
    elif font_size >= 14:
        return "H2"
    else:
        return "H3"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    # Collect text items from all pages
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                max_font_size = 0
                is_bold = False

                for span in line["spans"]:
                    if not span["text"].strip():
                        continue
                    line_text += span["text"].strip() + " "
                    max_font_size = max(max_font_size, span["size"])
                    if "Bold" in span["font"]:
                        is_bold = True

                cleaned = clean_text(line_text.strip())
                if not cleaned:
                    continue

                # Filter likely headings
                if len(cleaned.split()) > 12 or cleaned.endswith("."):
                    continue
                if not is_bold and max_font_size < 13:
                    continue

                heading_level = detect_heading_level(cleaned, max_font_size)

                outline.append({
                    "level": heading_level,
                    "text": cleaned,
                    "page": page_number  # ✅ 0-based
                })

    return outline
