import sqlite3

DB_NAME = "resume.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ User table ------------------

def init_user_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password_hash):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row

# ------------------ Candidates table ------------------

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def insert(user_id, filename, score):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO candidates (user_id, filename, score) VALUES (?, ?, ?)",
              (user_id, filename, score))
    conn.commit()
    conn.close()

def get_all_results(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT filename, score FROM candidates WHERE user_id = ? ORDER BY score DESC", (user_id,))
    results = [{"filename": row["filename"], "score": row["score"]} for row in c.fetchall()]
    conn.close()
    return results

def delete_score(user_id, filename):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM candidates WHERE user_id = ? AND filename = ?", (user_id, filename))
    conn.commit()
    conn.close()

def clear_all(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM candidates WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
