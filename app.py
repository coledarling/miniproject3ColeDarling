from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.insert_user(username, password):
            return redirect(url_for("login"))
        else:
            return "Username already exists!"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user(username, password)
        if user:
            session["username"] = username
            return redirect(url_for("quiz"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Display and handle quiz logic."""
    questions = db.fetch_questions()  # Fetch questions from the database
    if not questions:  # Check if there are no questions
        return "No quiz questions available! Add some to the database."
    score = 0
    if request.method == "POST":
        for question in questions:
            user_answer = request.form.get(question[0])
            if user_answer and user_answer.lower() == question[1].lower():
                score += 1
        session['score'] = score
        return redirect(url_for("results"))
    return render_template("quiz.html", questions=questions)



@app.route("/results")
def results():
    """Show quiz results."""
    score = session.get('score', 0)
    total = len(db.fetch_questions())
    return render_template("results.html", score=score, total=total)

@app.route("/logout")
def logout():
    """Log the user out and clear the session."""
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
