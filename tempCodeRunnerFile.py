from flask import Flask, render_template, request
from resume_generator import format_resume

app = Flask(__name__)
def generate_ai_bullets(text):
    sentences = text.split(".")
    bullets = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            improved = f"• Developed and implemented {sentence.lower()} using industry-standard tools."
            bullets.append(improved)
    
    return "\n".join(bullets)

@app.route("/", methods=["GET", "POST"])
def index():
    resume_text = None

    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "education": request.form["education"],
            "skills": request.form["skills"],
            "experience_description": request.form["experience_description"],
            "projects": request.form["projects"],
            "certifications": request.form["certifications"]
        }

        resume_text = format_resume(data)

    return render_template("index.html", resume_text=resume_text)

if __name__ == "__main__":
    app.run(debug=True)