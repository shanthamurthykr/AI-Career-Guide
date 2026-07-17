from flask import Flask, render_template, request
import os
from google import genai
from career_data import career_data, kcet_colleges, percentage_courses, scholarships, chatbot_responses

app = Flask(__name__)
client = genai.Client(api_key="AQ.Ab8RN6KxAHAHIJgFMFCiQB6VhuGNrr-cG7k3cIMfu2MEwW4AJg")

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    college_recommendations = []
    scholarship_list = []
    bot_reply = ""
    user_message = ""
    student_name = ""
    percentage = None
    stream = ""
    rank = ""
    education = ""
    value = None

    if request.method == "POST":
        student_name = request.form.get("name")
        stream = request.form.get("stream")
        rank = request.form.get("rank")
        education = request.form.get("education")
        user_message = request.form.get("message")
    
    recommendations = career_data.get(stream, [])

    if user_message:
        try:
            response = client.models.generate_content(
               model="gemini-3.5-flash",
               contents=user_message
            )

            bot_reply = response.text
        except Exception as e:
            bot_reply = f"AI Error: {e}"


    if education:
        scholarship_list = scholarships.get(education, [])

    if rank:
        value = int(rank)

        # Percentage Logic
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

        # KCET Rank Logic
        else:
            if value <= 1000:
                college_recommendations = kcet_colleges["1-1000"]
            elif value <= 5000:
                college_recommendations = kcet_colleges["1001-5000"]
            elif value <= 10000:
                college_recommendations = kcet_colleges["5001-10000"]
            else:
                college_recommendations = kcet_colleges["10001-300000"]

    return render_template(
        "index.html",
        recommendations=recommendations,
        student_name=student_name,
        colleges=college_recommendations,
        percentage=percentage,
        scholarships=scholarship_list,
        bot_reply=bot_reply,
        user_message=user_message
    )

if __name__ == "__main__":
    app.run(debug=True)