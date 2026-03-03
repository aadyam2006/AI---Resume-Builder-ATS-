from flask import Flask, render_template, request, send_file, session
from resume_generator import format_resume
from ats_engine import calculate_ats

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from io import BytesIO


app = Flask(__name__)
app.secret_key = "resume_app_secret"


@app.route("/", methods=["GET", "POST"])
def index():
    resume_text = None
    ats_score = None
    matched_skills = []
    missing_skills = []

    if request.method == "POST":
        data = {
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "linkedin": request.form.get("linkedin", ""),
            "github": request.form.get("github", ""),
            "education": request.form.get("education", ""),
            "skills": request.form.get("skills", ""),
            "experience_description": request.form.get("experience_description", ""),
            "projects": request.form.get("projects", ""),
            "certifications": request.form.get("certifications", "")
        }

        job_description = request.form.get("job_description", "")

        resume_text = format_resume(data)
        session["resume_text"] = resume_text

        ats_score, matched_skills, missing_skills = calculate_ats(resume_text, job_description)

    return render_template(
        "index.html",
        resume_text=resume_text,
        ats_score=ats_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


@app.route("/download", methods=["POST"])
def download():
    resume_content = session.get("resume_text", "")

    if not resume_content:
        return "No resume found. Please generate resume first."

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=22,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1f4e79"),
        spaceAfter=6
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#1f4e79"),
        spaceBefore=10,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        leftIndent=18,
        spaceAfter=2
    )

    lines = resume_content.split("\n")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if i == 0:
            elements.append(Paragraph(f"<b>{line}</b>", name_style))
            elements.append(Spacer(1, 4))

        elif "LinkedIn" in line or "GitHub" in line or "@" in line:
            elements.append(Paragraph(line, contact_style))
            elements.append(Spacer(1, 2))

        elif line.startswith("•"):
            elements.append(Paragraph(line, bullet_style))

        elif line.isupper():
            elements.append(Paragraph(f"<b>{line}</b>", section_style))
            elements.append(
                HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#1f4e79"))
    )

        else:
            elements.append(Paragraph(line, body_style))

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Professional_Resume.pdf",
        mimetype="application/pdf"
    )


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))