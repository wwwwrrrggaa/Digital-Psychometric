import requests
import local_store
import json
import os

CONFIG_FILE = "client_config.json"

def get_api_url():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("api_url", "http://localhost:8000")
        except:
            pass
    return "http://localhost:8000"

def save_api_url(url):
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except:
            pass
    config["api_url"] = url
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

API_URL = get_api_url()

def login(username, password):
    global API_URL
    API_URL = get_api_url() # Refresh in case it changed
    """
    Attempts to login to the server.
    Returns token if successful, None otherwise.
    Also saves user locally if successful.
    """
    try:
        response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
        if response.status_code == 200:
            token_data = response.json()
            # Save user locally for offline access
            local_store.save_local_user(username, password)
            return token_data["access_token"]
        return None
    except requests.exceptions.ConnectionError:
        return None

def sync_analytics(token, username):
    """
    Syncs unsynced analytics for the given user.
    """
    unsynced = local_store.get_unsynced_analytics(username)
    if not unsynced:
        return 0

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "items": [
            {
                "exam_id": item['exam_id'],
                "chapter_name": item['chapter_name'],
                "score": item['score'],
                "time_per_question_avg": item['time_per_question_avg']
            }
            for item in unsynced
        ]
    }

    try:
        response = requests.post(f"{API_URL}/sync", json=payload, headers=headers)
        if response.status_code == 200:
            # Mark as synced locally
            ids = [item['id'] for item in unsynced]
            local_store.mark_analytics_synced(ids)
            return len(ids)
    except Exception as e:
        print(f"Sync failed: {e}")

    return 0

def download_exam(exam, password, token):
    """
    Downloads an exam PDF/Zip from the server.
    Expects 'exam' dict with metadata (id, language, year, quarter).
    Returns the local path if successful, None otherwise.
    """
    global API_URL
    API_URL = get_api_url()

    exam_id = exam['id']
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "exam_id": exam_id,
        "password": password
    }

    try:
        response = requests.post(f"{API_URL}/exams/download", json=data, headers=headers)
        if response.status_code == 200:
            # Save Zip temporarily
            zip_filename = f"exam_{exam_id}.zip"
            zip_path = os.path.join("Exams", "temp", zip_filename)

            # Ensure directory exists
            import os
            import zipfile
            import shutil

            os.makedirs(os.path.dirname(zip_path), exist_ok=True)

            with open(zip_path, "wb") as f:
                f.write(response.content)

            # Extract to Exams/{Language}/{Year}/{Quarter}/
            # This ensures start.py picks it up automatically
            # exam['quarter'] might be "1", "2" etc.

            # Sanitize paths
            language = exam.get('language', 'Unknown')
            year = exam.get('year', 'Unknown')
            quarter = exam.get('quarter', str(exam_id))

            # Handle "Exams" vs "FullExams" based on version?
            # start.py looks in dirlib/Exams or dirlib/FullExams
            # exam['version'] should be "Exams" or "FullExams"
            version_folder = exam.get('version', 'Exams')

            extract_path = os.path.join(version_folder, language, year, quarter)

            if os.path.exists(extract_path):
                # Backup or overwrite? Overwrite for now.
                try:
                    shutil.rmtree(extract_path)
                except Exception as e:
                    print(f"Could not remove existing dir: {e}")

            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # Cleanup zip
            try:
                os.remove(zip_path)
            except:
                pass

            # Save metadata
            local_store.save_downloaded_exam(exam_id, exam.get('title', f"Exam {exam_id}"), str(exam_id), extract_path)
            return extract_path
    except Exception as e:
        print(f"Download failed: {e}")

    return None

def get_available_exams(token):
    global API_URL
    API_URL = get_api_url()
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/exams/", headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []
