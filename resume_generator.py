import random
import re

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

print("🔥 NEW BULLET GENERATOR ACTIVE 🔥")
def generate_bullet(text):
    sentences = text.split(".")
    bullets = []

    for sentence in sentences:
        sentence = clean_text(sentence)
        if not sentence:
            continue

        # Remove leading verb only (not all verbs)
        words = sentence.split()
        if words:
            first_word = words[0].lower()
            if first_word in [
                "developed", "built", "implemented", "designed",
                "optimized", "engineered", "created",
                "automated", "performed", "architected",
                "deployed"
            ]:
                words = words[1:]

        cleaned = " ".join(words)

        if not cleaned:
            continue

        action = random.choice(ACTION_VERBS)
        impact = random.choice(IMPACT_METRICS)

        # Preserve acronyms like REST, ML
        cleaned = cleaned[0].upper() + cleaned[1:]

        bullet = f"• {action} {cleaned}, {impact}."
        bullets.append(bullet)

    return "\n".join(bullets)
def format_resume(data):
    print("🔥 ULTRA FAANG GENERATOR ACTIVE 🔥")

    bullet_section = generate_bullet(data["experience_description"])

    formatted_name = data["name"].strip().title()

    contact_line1 = f"🔗 LinkedIn: {data['linkedin']}   |   🐙 GitHub: {data['github']}"
    contact_line2 = f"📧 {data['email']}   |   📞 {data['phone']}"

    resume_text = (
        f"{formatted_name}\n"
        f"{contact_line1}\n"
        f"{contact_line2}\n\n"
        f"PROFESSIONAL SUMMARY\n"
        f"Results-driven AI & Backend Engineer with expertise in scalable system architecture, machine learning deployment, and high-performance REST API design. Proven ability to architect production-ready ML systems and optimize backend infrastructures.\n\n"
        f"TECHNICAL SKILLS\n"
        f"Languages: Python\n"
        f"Frameworks: Flask\n"
        f"Machine Learning: Scikit-learn, Pandas, NumPy\n"
        f"Core Concepts: REST APIs, Feature Engineering, Model Deployment\n\n"
        f"PROFESSIONAL EXPERIENCE\n"
        f"{bullet_section}\n\n"
        f"PROJECTS\n"
        f"{data['projects']}\n\n"
        f"EDUCATION\n"
        f"{data['education']}\n\n"
        f"CERTIFICATIONS\n"
        f"{data['certifications']}"
    )

    return resume_text