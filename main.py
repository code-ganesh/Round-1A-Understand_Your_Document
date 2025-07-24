import os
import json
from extractor.processor import extract_outline

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    print("📄 Running PDF outline extractor...")  # Startup debug

    # List PDF files
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    print("Found PDFs:", pdf_files)  # Show which files are being processed

    for pdf_file in pdf_files:
        input_path = os.path.join(INPUT_DIR, pdf_file)
        output_path = os.path.join(OUTPUT_DIR, pdf_file.replace(".pdf", ".json"))

        print(f"🔍 Processing: {input_path}")  # Show current file being processed

        result = extract_outline(input_path)

        print(f"✅ Writing output to {output_path}")  # Confirm output path
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
