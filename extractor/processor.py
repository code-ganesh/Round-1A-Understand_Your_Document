import fitz
import re
from collections import Counter

def clean_text(text):
    """Cleans text by removing extra whitespace."""
    return re.sub(r'\s+', ' ', str(text)).strip()

class TextBlock:
    """A data class holding generic, structural, and semantic features of a text block."""
    def __init__(self, block, page_num):
        self.bbox = fitz.Rect(block['bbox'])
        self.page_num = page_num
        self.y0 = self.bbox.y0
        self.text = ""
        self.size = 0
        self.is_bold = False
        self.word_count = 0
        self.starts_with_list_marker = False
        
        lines = block.get('lines', [])
        if lines:
            span_texts = [s.get('text', '') for line in lines for s in line.get('spans', [])]
            self.text = clean_text(" ".join(span_texts))
            self.word_count = len(self.text.split())
            
            spans = lines[0].get('spans', [])
            if spans:
                self.size = round(spans[0]['size'])
                if "bold" in spans[0]['font'].lower() or "black" in spans[0]['font'].lower():
                    self.is_bold = True
        
        if self.text:
            self.starts_with_list_marker = bool(re.match(r'^\s*(\d+\.|[a-z][\.\)]|\([a-z]\)|•)\s', self.text, re.IGNORECASE))

def is_valid_report_heading(block, profile):
    """A generic filter for identifying headings in standard reports."""
    if block.size <= profile['body_size']: return False
    if block.starts_with_list_marker or block.text.endswith(':'): return False
    if block.word_count > 25: return False
    if not block.is_bold and block.size < profile['body_size'] + 2: return False
    return True

def extract_document_structure(pdf_path):
    doc = fitz.open(pdf_path)
    if not doc.page_count: return {"title": "", "outline": []}

    # --- Pass 1: Deep Feature Extraction & Document Fingerprinting ---
    all_blocks = []
    list_marker_count = 0
    for page_num, page in enumerate(doc, start=1):
        for b in page.get_text("dict")['blocks']:
            if b['type'] == 0:
                block = TextBlock(b, page_num)
                if block.text:
                    all_blocks.append(block)
                    if block.starts_with_list_marker:
                        list_marker_count += 1
    
    if not all_blocks: return {"title": "", "outline": []}

    # --- Pass 2: Algorithmic Document Classification ---
    doc_type = 'REPORT'
    if len(all_blocks) > 0:
        list_marker_ratio = list_marker_count / len(all_blocks)
        if list_marker_ratio > 0.15:
            doc_type = 'FORM'
        elif len(all_blocks) < 40:
            doc_type = 'FLYER'

    # --- Pass 3: Application of Type-Specific Generic Rules ---
    title = ""
    outline = []
    
    body_size_counter = Counter(b.size for b in all_blocks if b.word_count > 10)
    body_size = body_size_counter.most_common(1)[0][0] if body_size_counter else 10
    doc_profile = {'body_size': body_size}

    if doc_type == 'FORM':
        # Generic Rule for Forms: Title is the most prominent text at the very top.
        page1_top_blocks = [b for b in all_blocks if b.page_num == 1 and b.y0 < doc[0].rect.height * 0.2]
        title = max(page1_top_blocks, key=lambda b: b.size).text if page1_top_blocks else all_blocks[0].text
        outline = []

    elif doc_type == 'FLYER':
        # Generic Rule for Flyers: Title is empty. Outline is the most dominant text.
        title = ""
        max_size = max(b.size for b in all_blocks) if all_blocks else 0
        main_headings = [b for b in all_blocks if b.size == max_size]
        outline = [{"level": "H1", "text": h.text, "page": h.page_num - 1} for h in main_headings]

    elif doc_type == 'REPORT':
        # Generic Rules for Reports:
        heading_candidates = [b for b in all_blocks if is_valid_report_heading(b, doc_profile)]
        page1_candidates = sorted([h for h in heading_candidates if h.page_num == 1], key=lambda h: h.y0)
        
        if page1_candidates:
            title_blocks = [page1_candidates[0]]
            last_y1 = page1_candidates[0].bbox.y1
            # Chain subsequent blocks if they are close and have a similar large font size
            for i in range(1, len(page1_candidates)):
                if (page1_candidates[i].y0 - last_y1) < 20 and page1_candidates[i].size >= title_blocks[0].size - 2:
                    title_blocks.append(page1_candidates[i])
                    last_y1 = page1_candidates[i].bbox.y1
                else:
                    break
            title = " ".join(b.text for b in title_blocks)
            heading_candidates = [h for h in heading_candidates if h not in title_blocks]

        if heading_candidates:
            unique_sizes = sorted(list(set(h.size for h in heading_candidates)), reverse=True)
            size_to_level_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes)}
            
            for h in heading_candidates:
                if h.size in size_to_level_map:
                    outline.append({"level": size_to_level_map[h.size], "text": h.text, "page": h.page_num - 1})

    # Final sort for consistent order
    if outline:
        outline.sort(key=lambda x: (x['page'], [b.y0 for b in all_blocks if b.text == x['text']][0]))

    return {"title": clean_text(title), "outline": outline}