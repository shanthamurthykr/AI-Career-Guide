from flask import Flask, render_template, request,redirect, jsonify
from google import genai
from career_data import (career_data, kcet_colleges,comedk_colleges, percentage_courses, scholarships,roadmaps,skills_data,free_courses)
from flask import send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "ai_career_guide_secret_2026"
app.config["THEME"] = "blue-black"

client = genai.Client(api_key="GEMINI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    college_recommendations = []
    comedk_recommendations = []
    roadmap = []
    scholarship_list = []
    skill_recommendations = []
    free_course_list = []
    bot_reply = ""
    user_message = ""
    student_name = ""
    percentage = None
    stream = ""
    rank = ""
    education = ""
    value = None
    career_goal = ""
    comedk_rank = ""
    comedk_value = None

    if request.method == "POST":
        student_name = request.form.get("name")
        stream = request.form.get("stream")
        career_goal = request.form.get("career_goal")
        rank = request.form.get("rank")
        comedk_rank = request.form.get("comedk_rank")
        education = request.form.get("education")
        user_message = request.form.get("message")
        
        
    recommendations = career_data.get(stream, [])

       
    # Roadmap
    if career_goal:
        roadmap = roadmaps.get(career_goal, [])
        skill_recommendations = skills_data.get(career_goal, [])
        free_course_list = free_courses.get(career_goal, [])

    # Gemini AI
    if user_message:
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=user_message
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"AI Error: {e}"

    # Scholarships
    if education:
        scholarship_list = scholarships.get(education, [])

    # KCET Rank / Percentage
    if rank:
        value = int(rank)

        if value <= 100:
            percentage = value

            if value >= 90:
                recommendations = percentage_courses["90-100"]
            elif value >= 80:
                recommendations = percentage_courses["80-89"]
            elif value >= 70:
                recommendations = percentage_courses["70-79"]
            elif value >= 50:
                recommendations = percentage_courses["50-69"]

        else:
            if value <= 1000:
                college_recommendations = kcet_colleges["1-1000"]
            elif value <= 5000:
                college_recommendations = kcet_colleges["1001-5000"]
            elif value <= 10000:
                college_recommendations = kcet_colleges["5001-10000"]
            else:
                college_recommendations = kcet_colleges["10001-300000"]

    # COMEDK Rank
    if comedk_rank:
        comedk_value = int(comedk_rank)

        if comedk_value <= 1000:
            comedk_recommendations = comedk_colleges["1-1000"]
        elif comedk_value <= 5000:
            comedk_recommendations = comedk_colleges["1001-5000"]
        elif comedk_value <= 10000:
            comedk_recommendations = comedk_colleges["5001-10000"]
        else:
            comedk_recommendations = comedk_colleges["10001-30000"]

    return render_template(
        "index.html",
        recommendations=recommendations,
        roadmap=roadmap,
        student_name=student_name,
        colleges=college_recommendations,
        comedk_colleges=comedk_recommendations,
        percentage=percentage,
        scholarships=scholarship_list,
        bot_reply=bot_reply,
        user_message=user_message,
        skill_recommendations=skill_recommendations,
        free_courses=free_course_list
    )

@app.route("/youngstars")
def youngstars():
    return render_template("youngstars/home.html")


@app.route("/youngstars/home")
def youngstars_home():
    return render_template("youngstars/home.html")


@app.route("/youngstars/learning-skills")
def learning_skills():
    return render_template("youngstars/learning_skills.html")


@app.route("/youngstars/learning-skills/memory-skills")
def memory_skills():
    return render_template(
        "youngstars/learning_skills/memory_skills/memory_skills.html"
    )


@app.route("/youngstars/learning-skills/communication")
def communication():
    return render_template(
        "youngstars/learning_skills/communication/communication.html"
    )


@app.route("/youngstars/learning-skills/creativity")
def creativity():
    return render_template(
        "youngstars/learning_skills/creativity/creativity.html"
    )


@app.route("/youngstars/learning-skills/critical-thinking")
def critical_thinking():
    return render_template(
        "youngstars/learning_skills/critical_thinking/critical_thinking.html"
    )

@app.route('/youngstars/future-skills')
def future_skills():
    return render_template(
        'youngstars/learning_skills/future_skills/future_skills.html'
    )
@app.route('/youngstars/future-careers')
def future_careers():
    return render_template(
        'youngstars/future_careers/future_careers.html'
    )

@app.route('/youngstars/future-careers/government')
def government():
    return render_template(
        'youngstars/future_careers/government/government.html'
    )
@app.route('/youngstars/future-careers/defence')
def defence():
    return render_template(
        'youngstars/future_careers/defence/defence.html'
    )
@app.route('/youngstars/future-careers/medicine')
def medicine():
    return render_template(
        'youngstars/future_careers/medicine/medicine.html'
    )
@app.route('/youngstars/future-careers/science')
def science():
    return render_template(
        'youngstars/future_careers/science/science.html'
    )
@app.route('/youngstars/future-careers/technology')
def technology():
    return render_template(
        'youngstars/future_careers/technology/technology.html'
    )
@app.route('/youngstars/future-careers/engineering')
def engineering():
    return render_template(
        'youngstars/future_careers/engineering/engineering.html'
    )
@app.route('/youngstars/future-careers/business')
def business():
    return render_template(
        'youngstars/future_careers/business/business.html'
    )
@app.route('/youngstars/future-careers/law')
def law():
    return render_template(
        'youngstars/future_careers/law/law.html'
    )
@app.route('/youngstars/future-careers/creative')
def creative():
    return render_template(
        'youngstars/future_careers/creative/creative.html'
    )
@app.route('/youngstars/future-careers/sports')
def future_career_sports():
    return render_template(
        'youngstars/future_careers/sports/sports.html'
    )
@app.route('/youngstars/daily-learning')
def daily_learning():
    return render_template(
        'youngstars/daily_learning/daily_learning.html'
    )
@app.route('/youngstars/daily-learning/daily-plan')
def daily_plan():
    return render_template(
        'youngstars/daily_learning/daily_plan/daily_plan.html'
    )
@app.route('/youngstars/daily-learning/today-topic')
def today_topic():
    return render_template(
        'youngstars/daily_learning/today_topic/today_topic.html'
    )
@app.route('/youngstars/daily-learning/learn-something-new')
def learn_something_new():
    return render_template(
        'youngstars/daily_learning/learn_something_new/learn_something_new.html'
    )
@app.route('/youngstars/daily-learning/practice-time')
def practice_time():
    return render_template(
        'youngstars/daily_learning/practice_time/practice_time.html'
    )
@app.route('/youngstars/daily-learning/daily-challenge')
def daily_challenge():
    return render_template(
        'youngstars/daily_learning/daily_challenge/daily_challenge.html'
    )
@app.route('/youngstars/daily-learning/daily-notes')
def daily_notes():
    return render_template(
        'youngstars/daily_learning/daily_notes/daily_notes.html'
    )
@app.route('/youngstars/daily-learning/general-knowledge')
def general_knowledge():
    return render_template(
        'youngstars/daily_learning/general_knowledge/general_knowledge.html'
    )
@app.route('/youngstars/daily-learning/technology-of-day')
def technology_of_day():
    return render_template(
        'youngstars/daily_learning/technology_of_day/technology_of_day.html'
    )
@app.route('/youngstars/daily-learning/think-solve')
def think_solve():
    return render_template(
        'youngstars/daily_learning/think_solve/think_solve.html'
    )
@app.route('/youngstars/daily-learning/english-communication')
def english_communication():
    return render_template(
        'youngstars/daily_learning/english_communication/english_communication.html'
    )
@app.route('/youngstars/daily-learning/todays-goal')
def todays_goal():
    return render_template(
        'youngstars/daily_learning/todays_goal/todays_goal.html'
    )
@app.route('/youngstars/competitions')
def competitions():
    return render_template(
        'youngstars/competitions/competitions.html'
    )
@app.route('/youngstars/competitions/olympiads')
def olympiads():
    return render_template(
        'youngstars/competitions/olympiads/olympiads.html'
    )
@app.route('/youngstars/competitions/quizzes')
def quizzes():
    return render_template(
        'youngstars/competitions/quizzes/quizzes.html'
    )
@app.route('/youngstars/competitions/science-fairs')
def science_fairs():
    return render_template(
        'youngstars/competitions/science_fairs/science_fairs.html'
    )
@app.route('/youngstars/competitions/coding')
def coding():
    return render_template(
        'youngstars/competitions/coding/coding.html'
    )
@app.route('/youngstars/competitions/debate')
def debate():
    return render_template(
        'youngstars/competitions/debate/debate.html'
    )
@app.route('/youngstars/competitions/sports')
def sports():
    return render_template(
        'youngstars/competitions/sports/sports.html'
    )
@app.route('/youngstars/competitions/art-creative')
def art_creative():
    return render_template(
        'youngstars/competitions/art_creative/art_creative.html'
)
@app.route('/youngstars/competitions/scholarships')
def scholarships():
    return render_template(
        'youngstars/competitions/scholarships/scholarships.html'
    )
@app.route('/youngstars/ai-quiz')
def ai_quiz():
    return render_template(
        'youngstars/ai_quiz/ai_quiz.html'
    )
@app.route("/youngstars/ai-story", methods=["GET", "POST"])
def ai_story():
    story = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        category = request.form.get("category", "General Knowledge")
        length = request.form.get("length", "Short")
        idea = request.form.get("idea", "").strip()

        if not topic:
            error = "Please enter a story topic."
        else:
            prompt = f"""
Write an educational story for young students.

Topic: {topic}
Learning category: {category}
Story length: {length}
Additional idea: {idea}

Requirements:
- Use simple, age-appropriate English.
- Make the story interesting and imaginative.
- Teach something useful related to the selected category.
- Include a clear lesson or moral at the end.
- Do not just repeat the topic or form values.
- Return only the story and its lesson.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                story = response.text

            except Exception as exc:
                error = f"Story generation failed: {exc}"

    return render_template(
        "youngstars/ai_story/ai_story.html",
        story=story,
        error=error
    )
@app.route("/youngstars/motivation", methods=["GET", "POST"])
def motivation():
    motivation_text = None

    if request.method == "POST":
        goal = request.form.get("goal", "").strip()
        area = request.form.get("area", "Studies")
        challenge = request.form.get("challenge", "").strip()

        if goal:
            prompt = f"""
Give a short, positive and age-appropriate motivation
for a young student.

Goal: {goal}
Area: {area}
Challenge: {challenge}

Include:
1. Encouraging message
2. One practical step
3. A positive ending

Use simple language.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                motivation_text = response.text

            except Exception as exc:
                motivation_text = f"AI Error: {exc}"

    return render_template(
        "youngstars/motivation/motivation.html",
        motivation=motivation_text
    )
@app.route("/youngstars/parent-guide")
def parent_guide():
    return render_template(
        "youngstars/parent_guide/parent_guide.html"
    )


@app.route("/tenth")
def tenth():
    return render_template("tenth/tenth.html")

@app.route("/tenth/academic/science")
def tenth_science():
    return render_template(
        "tenth/academic/science/science.html"
    )

@app.route("/tenth/ai-tutor", methods=["GET", "POST"])
def ai_tutor():

    # Open AI Tutor page
    if request.method == "GET":
        return render_template("tenth/ai-tutor/ai_tutor.html")

    try:
        # IMPORTANT:
        # Frontend uses FormData(), so use request.form
        # NOT request.get_json()
        question = request.form.get("question", "").strip()
        language = request.form.get("language", "English").strip()

        if not question:
            return jsonify({
                "answer": "Please enter a question."
            }), 400

        # Language mapping
        language_map = {
            "English": "English",
            "Kannada": "Kannada",
            "Telugu": "Telugu",
            "Marathi": "Marathi",
            "Hindi": "Hindi",
            "Tamil": "Tamil"
        }

        selected_language = language_map.get(
            language,
            "English"
        )

        # Prompt for Gemini
        prompt = f"""
You are an AI Career Tutor for school students.

Student question:
{question}

IMPORTANT LANGUAGE RULE:
Answer ONLY in {selected_language}.

Do not answer in English if the selected language is
Kannada, Telugu, Marathi, Hindi or Tamil.

Give a simple, clear and student-friendly answer.

The student may ask about:
- 10th standard
- Streams
- Science PCM
- Science PCB
- Commerce
- Arts
- Polytechnic
- ITI
- B.Tech
- B.Sc
- B.Arch
- Medicine
- Pharmacy
- Nursing
- Biotechnology
- Life Sciences
- Careers
- Courses
- Scholarships
- Skills
- Education

Keep the answer practical and easy to understand.
"""

        # Gemini API call
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        answer = response.text

        if not answer:
            answer = "Sorry, I could not generate an answer."

        return jsonify({
            "answer": answer,
            "language": selected_language
        })

    except Exception as e:

        print("AI TUTOR ERROR:", e)

        return jsonify({
            "answer": "Sorry, something went wrong. Please try again."
        }), 500


@app.route("/puc")
def puc():
    return render_template("puc.html")


@app.route("/degree")
def degree():
    return render_template("degree.html")


@app.route("/resume", methods=["GET", "POST"])
def resume():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        education = request.form.get("education")
        skills = request.form.get("skills")
        projects = request.form.get("projects")
        
        return render_template(
            "resume.html",
            fullname=fullname,
            email=email,
            phone=phone,
            education=education,
            skills=skills,
            projects=projects
        )

    return render_template("resume.html")
@app.route("/download_resume", methods=["POST"])
def download_resume():

    fullname = request.form.get("fullname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    education = request.form.get("education")
    skills = request.form.get("skills")
    projects = request.form.get("projects")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Resume")

    pdf.setFont("Helvetica-Bold",24)
    pdf.drawCentredString(300,810,"Professional Resume")

    pdf.setFont("Helvetica",11)
    pdf.drawCentredString(300,792,"Generated by AI Career Guide")

    pdf.line(50,780,550,780)

    pdf.setFont("Helvetica",12)

    y = 760

    pdf.drawString(50, y, f"Name: {fullname}")
    y -= 25

    pdf.drawString(50, y, f"Email: {email}")
    y -= 25

    pdf.drawString(50, y, f"Phone: {phone}")
    y -= 35

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50, y, "Education")
    y -= 20

    pdf.setFont("Helvetica",12)
    pdf.drawString(50, y, education)
    y -= 35

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50, y, "Skills")
    y -= 20

    pdf.setFont("Helvetica",12)
    pdf.drawString(50, y, skills)
    y -= 35

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50, y, "Projects")
    y -= 20

    pdf.setFont("Helvetica",12)
    pdf.drawString(50, y, projects)

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Resume.pdf",
        mimetype="application/pdf"
    )
if __name__ == "__main__":
    app.run(debug=True)

