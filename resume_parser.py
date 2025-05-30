import re
from pdfminer.high_level import extract_text
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(uploaded_file):
    """Extract plain text from a PDF or .txt file."""
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf"):
        try:
            return extract_text(uploaded_file)
        except Exception as e:
            return ""

    return ""


def extract_contact_info(text):
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"(\+?\d{1,3})?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3}[\s.-]?\d{3,4}", text)
    
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
    }


def extract_skills(text):
    """Keyword-based simple skills extractor."""
    common_skills = [
        "python", "java", "c++", "machine learning", "deep learning", "tensorflow", "pytorch",
        "opencv", "nlp", "sql", "html", "css", "linux", "git", "docker", "azure", "aws"
    ]
    found_skills = []
    for skill in common_skills:
        if skill.lower() in text.lower():
            found_skills.append(skill.capitalize())
    return list(set(found_skills))


def extract_sections(text):
    """Rough section extraction by headers (simple heuristic)."""
    headers = ["education", "experience", "skills", "projects", "certifications"]
    lines = text.lower().splitlines()
    sections = {h: [] for h in headers}
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        for h in headers:
            if h in line:
                current = h
        if current:
            sections[current].append(line)

    return {k: v for k, v in sections.items() if v}


def extract_resume_data(text):
    sections = extract_sections(text)
    return {
        "contact": extract_contact_info(text),
        "skills": extract_skills(text),
        "education": sections.get("education", []),
        "experience": sections.get("experience", []),
        "structure_warnings": evaluate_structure(sections)
    }


def evaluate_structure(sections):
    required = ["education", "experience", "skills"]
    warnings = []
    for r in required:
        if r not in sections:
            warnings.append(f"Missing section: {r.capitalize()}")
    if len(sections.keys()) < 3:
        warnings.append("Résumé may be poorly structured or incomplete.")
    return warnings
