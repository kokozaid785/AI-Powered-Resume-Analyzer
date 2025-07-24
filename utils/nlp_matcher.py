import re

def normalize_skills(skills):
    # Normalize and title-case for consistent display
    return [skill.strip().lower() for skill in skills]

def extract_keywords_only(text):
    """Returns raw lowercase tokens from text (not used for matching)"""
    return normalize_skills(text.split())

def calculate_match(resume_text, job_keywords):
    resume_text_lower = resume_text.lower()
    job_keywords_normalized = normalize_skills(job_keywords)

    matched = set()
    for skill in job_keywords_normalized:
        # Word-boundary match for whole phrases
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text_lower):
            matched.add(skill.title())

    if len(job_keywords) == 0:
        return 0.0, set()

    score = round((len(matched) / len(job_keywords)) * 100, 2)
    return score, matched
