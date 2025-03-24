import sqlite3

# Create a new database file (quiz.db) or connect if it already exists
conn = sqlite3.connect("quiz.db")
c = conn.cursor()

# Create the "users" table
c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT)""")

# Create the "quiz" table
c.execute("""CREATE TABLE IF NOT EXISTS quiz (
            question TEXT,
            answer TEXT)""")

# Insert sample questions into the "quiz" table
sample_questions = [
    ("What is 5 + 3?", "8"),
    ("What color is the sky on a clear day?", "Blue"),
    ("How many days are in a week?", "7"),
    ("What is the largest planet in our solar system?", "Jupiter"),
    ("What is the freezing point of water in Celsius?", "0")
]

c.executemany("INSERT INTO quiz (question, answer) VALUES (?, ?)", sample_questions)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully with sample questions!")