import sqlite3


DATABASE = "quiz.db"

def connect_db():
    """Connect to the database."""
    return sqlite3.connect(DATABASE)

def init_db():
    """Initialize the database and create necessary tables."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS quiz (
                question TEXT,
                answer TEXT)""")
    conn.commit()
    conn.close()

def insert_user(username, password):
    """Insert a new user into the database."""
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()
    return True

def get_user(username, password):
    """Retrieve a user from the database based on credentials."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def fetch_questions():
    """Fetch all quiz questions from the database."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz")
    questions = c.fetchall()
    conn.close()
    return questions
