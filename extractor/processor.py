import fitz
import re
from .utils import clean_text, merge_adjacent_spans, is_heading_like

def extract_title(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]

    candidates = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["text"].strip():
                    candidates.append((span["text"], span["size"]))
    if not candidates:
        return "Untitled Document"

    title_text, _ = max(candidates, key=lambda x: x[1])
    return clean_text(title_text)

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = {}

    # Pass 1: collect font size stats
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = clean_text(span["text"])
                    if not text:
                        continue
                    size = round(span["size"], 1)
                    font_sizes[size] = font_sizes.get(size, 0) + 1

    if not font_sizes:
        return []

    # Top 3 font sizes
    sorted_sizes = sorted(font_sizes.items(), key=lambda x: (-x[0], -x[1]))
    size_to_level = {}
    for idx, (size, _) in enumerate(sorted_sizes[:3]):
        size_to_level[size] = f"H{idx+1}"

    # Pass 2: Extract with filters
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        spans = []
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = clean_text(span["text"])
                    if not text:
                        continue
                    spans.append({
                        "text": text,
                        "size": round(span["size"], 1),
                        "font": span["font"],
                        "flags": span["flags"]
                    })

        # Merge "1." and "Objective" if applicable
        merged_spans = merge_adjacent_spans(spans)

        for item in merged_spans:
            text = item["text"]
            size = item["size"]
            if size in size_to_level:
                if is_heading_like(text):
                    headings.append({
                        "text": text,
                        "level": size_to_level[size],
                        "page": page_num
                    })
    return headings
