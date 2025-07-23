import fitz
import re
import numpy as np
from collections import Counter

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF, page by page."""
    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        pages.append({"page": page_num + 1, "text": text})
    return pages

def keyword_score(text, keywords):
    """Score a text block based on keyword frequency."""
    text_tokens = re.findall(r'\w+', text.lower())
    keyword_tokens = re.findall(r'\w+', keywords.lower())
    text_counter = Counter(text_tokens)
    score = sum(text_counter.get(word, 0) for word in keyword_tokens)
    return score

def cosine_similarity(a, b):
    """Compute cosine similarity between two texts."""
    words = list(set(a + b))
    vec_a = np.array([a.count(w) for w in words])
    vec_b = np.array([b.count(w) for w in words])
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot / (norm_a * norm_b + 1e-10)

def score_sections(pages, persona_job_keywords):
    """Rank sections based on keyword matching and similarity."""
    ranked = []
    for page in pages:
        k_score = keyword_score(page["text"], persona_job_keywords)
        sim = cosine_similarity(
            re.findall(r'\w+', page["text"].lower()),
            re.findall(r'\w+', persona_job_keywords.lower())
        )
        combined_score = k_score + sim
        ranked.append((page, combined_score))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

def extract_relevant_sections(pdf_path, persona_job_keywords):
    pages = extract_text_from_pdf(pdf_path)
    ranked_sections = score_sections(pages, persona_job_keywords)

    extracted = []
    rank = 1
    for section, score in ranked_sections[:5]:  # Top 5 sections
        sub_sections = [{
            "refined_text": section["text"][:500],  # Trim long text
            "page": section["page"]
        }]
        extracted.append({
            "document": pdf_path.split("/")[-1],
            "page": section["page"],
            "section_title": f"Page {section['page']} Section",
            "importance_rank": rank,
            "sub_sections": sub_sections
        })
        rank += 1
    return extracted
