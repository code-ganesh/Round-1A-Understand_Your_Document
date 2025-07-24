import re

def clean_text(text):
    if text:
        return text.strip()
    return ""

def detect_heading_level(text):
    """
    Rule-based heading level detection based on patterns like:
    - Section 1       → H1
    - Section 1.1     → H2
    - Section 1.1.1   → H3
    """
    if not text:
        return "P"

    section_match = re.match(r'(Section|Chapter)\s+((\d+\.)*\d+)', text)
    if section_match:
        level_str = section_match.group(2)
        level_depth = level_str.count('.') + 1
        return f"H{level_depth}"
    return "P"
