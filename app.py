
from flask import Flask, render_template, request
from career_data import career_data, kcet_colleges, percentage_courses

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    college_recommendations = []
    student_name = ""

    if request.method == "POST":
        student_name = request.form.get("name")
        stream = request.form.get("stream")
        rank = request.form.get("rank")

        recommendations = career_data.get(stream, [])

        if rank:
            value = int(rank)
            print(value)

            # Percentage Logic
            if value <= 100:
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
        percentage=value if value <= 100
    else None
    )

if __name__ == "__main__":
    app.run(debug=True)