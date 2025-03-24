import sqlite3

DATABASE = "quiz.db"

def connect_db():
    """Connect to the database."""
    return sqlite3.connect(DATABASE)

def init_db():
    """Initialize the database and create necessary tables."""
    conn = connect_db()
    c = conn.cursor()

    # Create the users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Create the quiz table
    c.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    # Insert sample quiz questions if they do not exist
    c.execute("SELECT COUNT(*) FROM quiz")
    if c.fetchone()[0] == 0:
        questions = [
            ("What is the capital of France?", "Paris"),
            ("What is 2 + 2?", "4"),
            ("What color is the sky?", "blue")
        ]
        c.executemany("INSERT INTO quiz (question, answer) VALUES (?, ?)", questions)

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

def get_user(username):
    """Retrieve a user from the database."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"username": user[1], "password": user[2]}
    return None

def fetch_questions():
    """Fetch all quiz questions from the database."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT id, question, answer FROM quiz")
    questions = [{"id": row[0], "question": row[1], "answer": row[2]} for row in c.fetchall()]
    conn.close()
    return questions