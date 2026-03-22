import sqlite3
import os
import shutil
from datetime import datetime
from passlib.context import CryptContext

DB_NAME = "local_store.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # LocalUsers table
    c.execute('''CREATE TABLE IF NOT EXISTS local_users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  hashed_password TEXT,
                  last_login TIMESTAMP)''')

    # DownloadedExams table
    c.execute('''CREATE TABLE IF NOT EXISTS downloaded_exams
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  exam_id INTEGER UNIQUE, -- ID from server
                  title TEXT,
                  filename TEXT,
                  local_path TEXT,
                  downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # LocalAnalytics table
    # Stores un-synced test runs
    c.execute('''CREATE TABLE IF NOT EXISTS local_analytics
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER, -- Local user ID (or server ID if we sync that?)
                  username TEXT, -- storing username is safer for offline mapping
                  exam_id INTEGER,
                  chapter_name TEXT,
                  score INTEGER,
                  time_per_question_avg INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  synced BOOLEAN DEFAULT 0)''')

    # ExamInProgress table
    c.execute('''CREATE TABLE IF NOT EXISTS exam_inprogress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  exam_id INTEGER,
                  current_chapter INTEGER,
                  answers_json TEXT,
                  time_elapsed INTEGER,
                  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  UNIQUE(username, exam_id))''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def save_local_user(username, password):
    """
    Saves or updates a user's credentials locally.
    Hashes the password before storing.
    """
    conn = get_connection()
    c = conn.cursor()
    hashed = get_password_hash(password)

    # Check if user exists
    c.execute("SELECT id FROM local_users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE local_users SET hashed_password = ?, last_login = ? WHERE id = ?",
                  (hashed, datetime.now(), result[0]))
    else:
        c.execute("INSERT INTO local_users (username, hashed_password, last_login) VALUES (?, ?, ?)",
                  (username, hashed, datetime.now()))

    conn.commit()
    conn.close()

def get_local_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, hashed_password FROM local_users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "hashed_password": row[2]}
    return None

def login_offline(username, password):
    user = get_local_user(username)
    if user and verify_password(password, user['hashed_password']):
        return user
    return None

def save_downloaded_exam(exam_id, title, filename, local_path):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO downloaded_exams (exam_id, title, filename, local_path, downloaded_at) VALUES (?, ?, ?, ?, ?)",
                  (exam_id, title, filename, local_path, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error saving exam: {e}")
    finally:
        conn.close()

def get_downloaded_exams():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM downloaded_exams ORDER BY downloaded_at DESC")
    rows = c.fetchall()
    conn.close()
    exams = []
    for row in rows:
        exams.append({
            "id": row[0],
            "exam_id": row[1],
            "title": row[2],
            "filename": row[3],
            "local_path": row[4],
            "downloaded_at": row[5]
        })
    return exams

def save_analytics(username, exam_id, chapter_name, score, time_per_question_avg):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO local_analytics 
                 (username, exam_id, chapter_name, score, time_per_question_avg) 
                 VALUES (?, ?, ?, ?, ?)''',
              (username, exam_id, chapter_name, score, time_per_question_avg))
    conn.commit()
    conn.close()

def get_unsynced_analytics(username=None):
    conn = get_connection()
    c = conn.cursor()
    if username:
        c.execute("SELECT * FROM local_analytics WHERE synced = 0 AND username = ?", (username,))
    else:
        c.execute("SELECT * FROM local_analytics WHERE synced = 0")

    rows = c.fetchall()
    conn.close()
    analytics = []
    for row in rows:
        analytics.append({
            "id": row[0],
            "user_id": row[1],
            "username": row[2],
            "exam_id": row[3],
            "chapter_name": row[4],
            "score": row[5],
            "time_per_question_avg": row[6],
            "created_at": row[7]
        })
    return analytics

def mark_analytics_synced(analytics_ids):
    conn = get_connection()
    c = conn.cursor()
    # Safely building query for list of IDs
    placeholders = ','.join('?' for _ in analytics_ids)
    sql = f"UPDATE local_analytics SET synced = 1 WHERE id IN ({placeholders})"
    c.execute(sql, tuple(analytics_ids))
    conn.commit()
    conn.close()

def save_exam_progress(username, exam_id, current_chapter, answers_json, time_elapsed):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO exam_inprogress (username, exam_id, current_chapter, answers_json, time_elapsed, last_updated)
                     VALUES (?, ?, ?, ?, ?, ?)
                     ON CONFLICT(username, exam_id) DO UPDATE SET
                     current_chapter=excluded.current_chapter,
                     answers_json=excluded.answers_json,
                     time_elapsed=excluded.time_elapsed,
                     last_updated=excluded.last_updated''',
                  (username, exam_id, current_chapter, answers_json, time_elapsed, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error saving progress: {e}")
    finally:
        conn.close()

def load_exam_progress(username, exam_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT current_chapter, answers_json, time_elapsed FROM exam_inprogress WHERE username = ? AND exam_id = ?", (username, exam_id))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "current_chapter": row[0],
            "answers_json": row[1],
            "time_elapsed": row[2]
        }
    return None

def delete_exam_progress(username, exam_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM exam_inprogress WHERE username = ? AND exam_id = ?", (username, exam_id))
    conn.commit()
    conn.close()

def reset_all_data():
    """
    Deletes all local data including the database, exams, and saves.
    """
    # 1. Close any DB connections (handled by context managers usually, but make sure)
    # Since we use connect() inside methods, existing connections should be closed unless main app holds one.

    # 2. Delete DB file
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
        except Exception as e:
            print(f"Failed to remove DB: {e}")
            raise e

    # 3. Delete folders: Exams, FullExams, Saves
    folders = ["Exams", "FullExams", "Saves"]
    for folder in folders:
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                 print(f"Failed to remove {folder}: {e}")

    # 4. Re-init DB
    init_db()

init_db()
