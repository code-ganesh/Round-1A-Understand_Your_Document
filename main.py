import os
from extractor.processor import extract_headings
import json

print("📄 Running PDF outline extractor...")

input_dir = "input"
output_dir = "output"

pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
print("Found PDFs:", pdf_files)

for pdf in pdf_files:
    input_path = os.path.join(input_dir, pdf)
    output_path = os.path.join(output_dir, pdf.replace(".pdf", ".json"))

    print(f"🔍 Processing: {input_path}")
    outline = extract_headings(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": pdf,
            "outline": outline
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ Writing output to {output_path}")
