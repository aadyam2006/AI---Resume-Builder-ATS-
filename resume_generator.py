import os
import requests
import random
import re
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

ACTION_VERBS = [
    "Architected",
    "Engineered",
    "Designed",
    "Implemented",
    "Optimized",
    "Built",
    "Deployed",
    "Automated",
    "Led",
    "Spearheaded"
]

IMPACT_METRICS = [
    "improving system efficiency by 35%",
    "reducing latency by 40%",
    "increasing model accuracy by 22%",
    "enhancing scalability across distributed systems",
    "optimizing backend performance under high load",
    "streamlining ML pipelines for faster deployment",
    "improving API throughput by 50%",
    "reducing operational overhead by 30%"
]


def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


# 🔥 AI Rewrite Function (HuggingFace)
def ai_rewrite_bullet(text):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    prompt = f"Rewrite this resume bullet professionally with strong action verbs and measurable impact:\n{text}"

    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 100}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text']
    else:
        return text  # fallback


def generate_bullet(text):
    sentences = text.split(".")
    bullets = []

    for sentence in sentences:
        sentence = clean_text(sentence)
        if sentence:
            action = random.choice(ACTION_VERBS)
            impact = random.choice(IMPACT_METRICS)

            base_bullet = f"{action} {sentence.lower()} {impact}."

            # 🔥 Pass through AI rewrite
            improved_bullet = ai_rewrite_bullet(base_bullet)

            bullets.append(f"• {improved_bullet}")

    return "\n".join(bullets)


def format_resume(data):
    print("🔥 AI + RULE HYBRID GENERATOR ACTIVE 🔥")

    bullet_section = generate_bullet(data["experience_description"])

    resume_text = f"""
{data['name'].title()}
🔗 LinkedIn: {data['linkedin']}   |   🐙 GitHub: {data['github']}
📧 {data['email']}   |   📞 {data['phone']}

PROFESSIONAL SUMMARY
Results-driven AI & Backend Engineer with expertise in scalable system architecture, machine learning deployment, and high-performance REST API design.

TECHNICAL SKILLS
Languages: Python
Frameworks: Flask
Machine Learning: Scikit-learn, Pandas, NumPy
Core Concepts: REST APIs, Feature Engineering, Model Deployment

PROFESSIONAL EXPERIENCE
{bullet_section}

PROJECTS
{data['projects']}

EDUCATION
{data['education']}

CERTIFICATIONS
{data['certifications']}
"""

    return resume_text.strip()