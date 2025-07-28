import fitz
import re
from collections import Counter

def clean_text(text):
    """Removes extra whitespace and non-printable characters."""
    return re.sub(r'\s+', ' ', text.strip())

def get_font_statistics(pdf_path):
    """
    Analyzes the PDF to find the most common font sizes, which helps in
    differentiating headings from body text.
    """
    doc = fitz.open(pdf_path)
    font_sizes = Counter()
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    font_sizes[size] += 1
    
    # The most common font size is likely the body text
    most_common_size = font_sizes.most_common(1)[0][0] if font_sizes else 0
    
    # Heading sizes are typically larger than the body text
    heading_sizes = [size for size, _ in font_sizes.most_common() if size > most_common_size]
    
    # Sort heading sizes in descending order and take the top 3
    top_font_sizes = sorted(heading_sizes, reverse=True)[:3]
    
    # Ensure there are always 3 heading levels, even if fewer are found
    while len(top_font_sizes) < 3:
        top_font_sizes.append(top_font_sizes[-1] if top_font_sizes else most_common_size)

    return {
        "body_text_size": most_common_size,
        "top_font_sizes": top_font_sizes
    }

def is_heading_like(text, is_bold):
    """
    Determines if a line of text is likely a heading based on its content and style.
    """
    text = text.strip()

    if not text or len(text.split()) > 15 or len(text) > 150:
        return False
        
    # Headings are often in title case or all caps
    if not (text.istitle() or text.isupper()):
        return False

    # Headings usually don't end with a period
    if text.endswith('.') or text.endswith(','):
        return False

    # Numbered headings are a strong indicator (e.g., "1. Introduction", "2.1. Methodology")
    if re.match(r'^\d+(\.\d+)*\s+', text):
        return True

    # Check for keywords that often appear in headings
    heading_keywords = ['introduction', 'abstract', 'conclusion', 'references', 'methodology', 'results', 'discussion']
    if any(keyword in text.lower() for keyword in heading_keywords):
        return True
    
    # Bold text is a strong indicator
    if is_bold:
        return True

    return False