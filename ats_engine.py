from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Preprocess text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

# Master skill list (can expand later)
SKILL_LIST = [
    "python", "flask", "machine learning", "sql",
    "aws", "docker", "tensorflow", "pytorch",
    "data science", "rest api", "git"
]

def extract_skills(text):
    text = preprocess(text)
    found_skills = []
    for skill in SKILL_LIST:
        if skill in text:
            found_skills.append(skill)
    return found_skills

import re

def calculate_ats(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    # Extract keywords from JD (simple split)
    jd_words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description)

    # Remove common filler words
    stopwords = ["with", "and", "the", "for", "using", "should", "have", "knowledge", "looking", "candidate"]
    jd_keywords = [word for word in jd_words if word not in stopwords]

    matched_skills = []
    missing_skills = []

    for word in set(jd_keywords):
        if word in resume_text:
            matched_skills.append(word)
        else:
            missing_skills.append(word)

    if len(jd_keywords) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(set(jd_keywords))) * 100

    return round(score, 2), matched_skills, missing_skills