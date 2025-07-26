import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def merge_adjacent_spans(spans):
    merged = []
    skip = False
    for i in range(len(spans)):
        if skip:
            skip = False
            continue
        current = spans[i]
        if i < len(spans) - 1:
            next_span = spans[i + 1]
            if current["size"] == next_span["size"]:
                merged.append({
                    "text": f"{current['text']} {next_span['text']}",
                    "size": current["size"]
                })
                skip = True
            else:
                merged.append({
                    "text": current["text"],
                    "size": current["size"]
                })
        else:
            merged.append({
                "text": current["text"],
                "size": current["size"]
            })
    return merged

def is_heading_like(text):
    # Only allow short strings that look like headings
    if len(text.split()) > 15:
        return False
    # Disallow typical paragraph patterns
    if re.match(r'^[a-z]', text):
        return False
    # Allow numbered headings, Roman, etc.
    if re.match(r'^(\d+\.|\(?[ivxIVX]{1,4}\)?\.?)\s*\w+', text):
        return True
    # Allow capital or title-case phrases
    if re.match(r'^[A-Z][A-Za-z\s\-:\(\)]+$', text) and not text.endswith("."):
        return True
    return False
