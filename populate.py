from db import connect_db

conn = connect_db()
c = conn.cursor()

# Add sample questions
c.execute("INSERT INTO quiz (question, answer) VALUES (?, ?)", ("What is the capital of France?", "Paris"))
c.execute("INSERT INTO quiz (question, answer) VALUES (?, ?)", ("What is 2 + 2?", "4"))
c.execute("INSERT INTO quiz (question, answer) VALUES (?, ?)", ("Who wrote 'Hamlet'?", "Shakespeare"))

conn.commit()
conn.close()
print("Sample questions added successfully!")