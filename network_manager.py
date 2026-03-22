import requests
import local_store
import json
import os
import zipfile
import shutil

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
    Returns (token, error_message).
    """
    try:
        response = requests.post(f"{API_URL}/login", data={"username": username, "password": password}, timeout=5)
        if response.status_code == 200:
            token_data = response.json()
            # Save user locally for offline access
            local_store.save_local_user(username, password)
            return token_data["access_token"], None
        elif response.status_code == 401:
            return None, "Invalid username or password"
        else:
            return None, f"Server error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "Connection failed: Server unreachable"
    except requests.exceptions.Timeout:
         return None, "Connection timed out"
    except Exception as e:
        return None, f"Error: {str(e)}"

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
    Downloads an exam directory from the server and prepares it for the app.
    Returns the local path if successful, None otherwise.
    """
    global API_URL
    API_URL = get_api_url()

    exam_id = exam.get('id', exam.get('exam_id'))
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "exam_id": exam_id,
        "password": password
    }

    try:
        response = requests.post(f"{API_URL}/exams/download", json=data, headers=headers)
        if response.status_code == 200:
            # Sanitize paths and metadata
            def sanitize(val, default):
                if val is None or val == "N/A" or val == "None":
                    return default
                return str(val)

            language = sanitize(exam.get('language'), 'Unknown')
            year = sanitize(exam.get('year'), 'Unknown')
            # Fix quarter fallback logic
            quarter_val = exam.get('quarter')
            if not quarter_val or quarter_val == "N/A":
                 # Try to extract from name if possible, e.g. "Hebrew-2024-2"
                 name = exam.get('name', '')
                 if '-' in name:
                      parts = name.split('-')
                      if len(parts) >= 3 and parts[-1].isdigit():
                           quarter_val = parts[-1]
                      else:
                           quarter_val = str(exam_id)
                 else:
                      quarter_val = str(exam_id)

            quarter = sanitize(quarter_val, str(exam_id))

            version_folder = sanitize(exam.get('version'), 'Exams')
            # Build path relative to current working directory like start.py expects
            extract_path = os.path.join(version_folder, language, year, quarter)
            # Make it absolute for reliability
            extract_path = os.path.abspath(extract_path)

            # Ensure extraction path exists and is clean
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)
            os.makedirs(extract_path, exist_ok=True)

            content_type = response.headers.get('Content-Type', '')

            if 'zip' in content_type or response.content.startswith(b'PK\x03\x04'):
                # Handle Zip files
                zip_filename = f"exam_{exam_id}.zip"
                zip_temp_path = os.path.join("Exams", "temp", zip_filename)
                os.makedirs(os.path.dirname(zip_temp_path), exist_ok=True)

                with open(zip_temp_path, "wb") as f:
                    f.write(response.content)

                try:
                    with zipfile.ZipFile(zip_temp_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    print(f"Successfully extracted exam to {extract_path}")
                except Exception as e:
                    print(f"Failed to extract ZIP: {e}")
                    return None

                try:
                    os.remove(zip_temp_path)
                except:
                    pass

                # Verify all required files exist
                required_files = ['exam.pdf', 'answers.txt', 'pagelist.txt', 'gradingkey.txt']
                missing_files = [f for f in required_files if not os.path.exists(os.path.join(extract_path, f))]
                if missing_files:
                    print(f"WARNING: Downloaded exam is missing required metadata files: {missing_files}")
                    return None

            elif 'pdf' in content_type or response.content.startswith(b'%PDF'):
                # Handle single PDF files
                # The app expects answers.txt, pagelist.txt, gradingkey.txt, which must be in the ZIP
                # A PDF-only response indicates the server is misconfigured
                pdf_path = os.path.join(extract_path, "exam.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(response.content)

                print(f"ERROR: Downloaded PDF only to {extract_path}.")
                print(f"The app requires metadata files (answers.txt, pagelist.txt, gradingkey.txt)")
                print(f"This usually means the exam on the server is improperly configured.")
                print(f"Please ensure the server has the complete exam ZIP with all metadata files.")
                return None
            else:
                # Unknown content type
                print(f"Unknown content type received: {content_type}")
                return None

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
