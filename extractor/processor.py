import fitz  # PyMuPDF
from extractor.utils import clean_text

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = {}
    blocks_by_page = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")['blocks']
        page_text_blocks = []
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                text = "".join(span['text'] for span in line['spans']).strip()
                if text:
                    size = line['spans'][0]['size']
                    font_sizes[size] = font_sizes.get(size, 0) + 1
                    page_text_blocks.append((clean_text(text), size, page_num))
        blocks_by_page.extend(page_text_blocks)

    # Pick top 3 most common font sizes
    common_sizes = sorted(font_sizes.items(), key=lambda x: -x[1])
    top_sizes = [item[0] for item in common_sizes[:3]]
    heading_levels = {size: f"H{i+1}" for i, size in enumerate(sorted(top_sizes, reverse=True))}

    outline = []
    title = ""
    title_found = False

    for text, size, page in blocks_by_page:
        if size in heading_levels:
            level = heading_levels[size]
            if not title_found:
                title = text
                title_found = True
                continue
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return {
        "title": title,
        "outline": outline
    }
