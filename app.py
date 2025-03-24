"""

"""

from flask import Flask, render_template, request, redirect, url_for, session
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure random key

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256", salt_length=16)
        if db.insert_user(username, password):
            return redirect(url_for("login"))  # Redirect to login after successful registration
        else:
            return "Username already exists!"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = username  # Save username in the session
            return redirect(url_for("quiz"))  # Redirect to the quiz page after login
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Display and handle quiz logic."""
    if "username" not in session