import sqlite3
import json
import os
from datetime import datetime

DB_NAME = "local_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table for sessions (replaces save slots)
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  last_accessed TIMESTAMP)''')

    # Table for exam answers
    c.execute('''CREATE TABLE IF NOT EXISTS exam_answers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id INTEGER,
                  exam_id TEXT, -- identifier for the exam (folder path or name)
                  chapter_index INTEGER,
                  answers TEXT, -- JSON string of answers
                  answer_type TEXT, -- type of the answer (e.g., 'user', 'ai')
                  FOREIGN KEY(session_id) REFERENCES sessions(id))''')

    # Table for user settings/state
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY, value TEXT)''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_or_create_session(session_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM sessions WHERE name = ?", (session_name,))
    result = c.fetchone()
    if result:
        session_id = result[0]
        c.execute("UPDATE sessions SET last_accessed = ? WHERE id = ?", (datetime.now(), session_id))
    else:
        c.execute("INSERT INTO sessions (name, created_at, last_accessed) VALUES (?, ?, ?)",
                  (session_name, datetime.now(), datetime.now()))
        session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id, session_name

def save_chapter_answers(session_id, exam_id, chapter_index, answers, answer_type='user'):
    conn = get_connection()
    c = conn.cursor()
    answers_json = json.dumps(answers)

    # Check if exists
    c.execute("SELECT id FROM exam_answers WHERE session_id = ? AND exam_id = ? AND chapter_index = ? AND answer_type = ?",
              (session_id, exam_id, chapter_index, answer_type))
    result = c.fetchone()

    if result:
        c.execute("UPDATE exam_answers SET answers = ? WHERE id = ?", (answers_json, result[0]))
    else:
        c.execute("INSERT INTO exam_answers (session_id, exam_id, chapter_index, answers, answer_type) VALUES (?, ?, ?, ?, ?)",
                  (session_id, exam_id, chapter_index, answers_json, answer_type))
    conn.commit()
    conn.close()

def load_chapter_answers(session_id, exam_id, chapter_index, answer_type='user'):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT answers FROM exam_answers WHERE session_id = ? AND exam_id = ? AND chapter_index = ? AND answer_type = ?",
              (session_id, exam_id, chapter_index, answer_type))
    result = c.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return None

def get_all_sessions():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sessions ORDER BY last_accessed DESC")
    sessions = [row[0] for row in c.fetchall()]
    conn.close()
    return sessions

def bind_exam_to_session(session_id, exam_id):
    """Associates an exam ID with a session if not already done."""
    conn = get_connection()
    c = conn.cursor()
    # We might want to store which exam this session is for in the sessions table
    # For now, we can check if we have a way to store metadata.
    # Let's add a column to sessions table if not exists? Or just use settings table.
    # Actually, sessions table needs exam_id.
    try:
        c.execute("ALTER TABLE sessions ADD COLUMN exam_id TEXT")
    except sqlite3.OperationalError:
        pass

    c.execute("UPDATE sessions SET exam_id = ? WHERE id = ?", (exam_id, session_id))
    conn.commit()
    conn.close()

def get_session_exam_id(session_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT exam_id FROM sessions WHERE id = ?", (session_id,))
        result = c.fetchone()
        return result[0] if result else None
    except sqlite3.OperationalError:
        return None
    finally:
        conn.close()

init_db()
