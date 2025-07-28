import os
import json
from extractor.processor import extract_document_structure

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    print("📄 Running Final 'Ground Truth' Engine...")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"   -> Processing {filename}")
            
            result = extract_document_structure(pdf_path)

            output_filename = filename.rsplit(".", 1)[0] + ".json"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

    print("✅ Analysis complete.")

if __name__ == "__main__":
    main()