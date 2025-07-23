import os
import json
from datetime import datetime
from persona_extractor import extract_relevant_sections

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
PERSONA = "PhD Researcher in Computational Biology"
JOB = "Prepare a literature review on Graph Neural Networks for Drug Discovery"

def main():
    metadata = {
        "input_documents": [],
        "persona": PERSONA,
        "job_to_be_done": JOB,
        "processing_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    all_extracted_sections = []

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            metadata["input_documents"].append(filename)
            sections = extract_relevant_sections(input_path, PERSONA + " " + JOB)
            all_extracted_sections.extend(sections)

    result = {
        "metadata": metadata,
        "extracted_sections": all_extracted_sections
    }

    output_path = os.path.join(OUTPUT_DIR, "persona_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()
