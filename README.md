# 🧠 PDF Outline Extractor – Adobe Hackathon 2025 Round 1A

## 📘 Problem Statement
Extract a structured outline (title, H1, H2, H3 headings) from raw PDF documents. The output must be a valid JSON file identifying heading levels and page numbers. This solution is designed to run entirely offline in a Docker container and is compatible with amd64 architecture.

---

## 📂 Folder Structure

pdf-outline-extractor/
├── main.py # Entry point
├── Dockerfile # Docker setup
├── requirements.txt # Python dependencies
├── README.md # This file
├── extractor/
│ ├── init.py # Python package marker
│ ├── processor.py # PDF parser and heading extractor
│ ├── utils.py # Helper functions
├── input/ # Input PDFs (volume mounted)
├── output/ # Output JSON files (volume mounted)

yaml
Copy
Edit

---

## 🚀 How to Build and Run

### 🧱 Step 1: Build Docker Image

docker build --platform linux/amd64 -t mysolutionname:abc123 .
📥 Step 2: Place Your PDFs
Place one or more .pdf files inside the input/ folder.

🧪 Step 3: Run the Container

docker run --rm `
  -v "D:/your/path/pdf-outline-extractor/input:/app/input" `
  -v "D:/your/path/pdf-outline-extractor/output:/app/output" `
  --network none `
  mysolutionname:abc123
Replace the path with your actual local path if you're on Windows.
On Unix/macOS, use: $(pwd) instead of full paths.

🧾 Sample Output Format
json:
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
⚙️ Tech Stack
Python 3.10 (via python:3.10-slim)

PyMuPDF (fitz) for fast PDF parsing

No external dependencies, no internet access needed

CPU-only execution, model size: 0MB (lightweight logic-based solution)

🧠 Logic Summary
Extracts all text lines from each page

Records font sizes for every line

Selects top 3 most common font sizes → maps to H1, H2, H3

Picks the first heading as the document title

Outputs clean JSON with heading levels and page numbers