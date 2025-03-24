'''
INF601 - Programming in Python
Assignment# MiniProject 3
I, Cole Darling, affirm that the work submitted for this assignment is entirely my own. I have not engaged in any form of academic dishonesty, including but not limited to cheating, plagiarism, or the use of unauthorized materials. I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence to academic standards. I understand that failing to comply with this integrity statement may result in consequences, including disciplinary actions as determined by my course instructor and outlined in institutional policies. By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.
'''

from flask import Flask, render_template, request, redirect, url_for, session
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize Database
db.init_db()

# Home Page Route
@app.route("/")
def home():
    return render_template("home.html")

# Registration Page Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256", salt_length=16)
        if db.insert_user(username, password):
            return redirect(url_for("login"))
        else:
            return "Username already exists!"
    return render_template("register.html")

# Login Page Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("quiz"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

# Quiz Page Route
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "username" not in session:
        return redirect(url_for("login"))

    questions = db.fetch_questions()

    if request.method == "POST":
        score = 0
        for question in questions:
            answer = request.form.get(f"question_{question['id']}")
            if answer and answer.strip().lower() == question['answer'].lower():
                score += 1
        session["score"] = score  # Store score in session
        session["total"] = len(questions)  # Store total in session
        return redirect(url_for("results"))  # Redirect to the results page

    return render_template("quiz.html", questions=questions)

@app.route("/results")
def results():
    if "username" not in session:
        return redirect(url_for("login"))
    if "score" not in session or "total" not in session:
        return redirect(url_for("quiz"))

    score = session.get("score")  # Retrieve score
    total = session.get("total")  # Retrieve total
    return render_template("results.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)