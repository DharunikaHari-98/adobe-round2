# 📄 Adobe India Hackathon 2025 — Round 1B

## 🎯 Task
Extract and rank the **top 5 most relevant sections** from each PDF based on a **user persona** and **job to be done**.

---

## 🗂 Folder Structure

.
├── app/
│ ├── main.py # Entry point
│ └── persona_extractor.py # Section scoring and ranking logic
├── input/ # Input PDFs
│ ├── discover.pdf
│ └── file-sample_150kB.pdf
├── output/ # Extracted JSON will appear here
├── Dockerfile
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🧠 How It Works

1. Extracts text page by page using `PyMuPDF`
2. Scores relevance using:
   - Keyword frequency
   - Cosine similarity
3. Outputs top 5 sections per PDF with:
   - `importance_rank` (local to doc)
   - `score` (combined match + similarity)
   - `refined_text` preview (trimmed to 500 chars)

---

## 🚀 Run Instructions (Dockerized)

### 🔨 Build the image
```bash
docker build --platform linux/amd64 -t adobehack:round1b .
▶️ Run the container
bash
Copy
Edit
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none adobehack:round1b
🔍 Sample Output Schema
json
Copy
Edit
{
  "document": "file.pdf",
  "page": 3,
  "importance_rank": 1,
  "sub_sections": [
    {
      "refined_text": "...",
      "page": 3,
      "score": 42.65
    }
  ]
}
✅ Extras Implemented
 Included relevance scores in output

 Skipped empty pages

 Clarified importance ranking scope

 Works fully offline

 Adheres to schema expectations

 Supports multiple PDFs

🔐 Notes
importance_rank is local per document

Final structured_output.json will be in /output/

