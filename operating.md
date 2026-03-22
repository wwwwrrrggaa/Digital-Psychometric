# Operating Instructions

This guide provides step-by-step instructions for setting up the environment, running the backend server, and operating the client application.

## 📋 1. Environment Setup

### Prerequisites
- Python 3.10+ installed and added to PATH.
- (Optional) A clean virtual environment to avoid dependency conflicts.

```powershell
# Create a virtual environment (Recommended)
python -m venv venv
.\venv\Scripts\activate

# Install Project Dependencies
pip install -r requirements.txt
pip install -r client_requirements.txt
```

---

## 🖥 2. Server Operations

### A. Database Initialization
Before starting the server, you must seed the database with initial users and exams.
```powershell
python server/seed_db.py
```
This script acts as an admin tool:
- Creates users: `student` (prop: `password`) and `Yuval` (prop: `19-07`).
- Scans the `Digital-Psychometric-Data` folder.
- Archives exam folders into zip files for distribution.
- Registers exams in the database with the download password `1234`.

### B. Starting the Server
Run the dedicated server script:
```powershell
python run_server.py
```
*The server will listen on `http://0.0.0.0:8000`.*

### C. Troubleshooting
- If the server crashes immediately or you see a "socket bind" error, ensure no other process is using port 8000.
- Check logs for "Application startup complete" to confirm it's running.

---

## 📱 3. Client Operations

### A. Launching the Client
Open a new terminal (keep the server terminal running) and start the client:
```powershell
python start.py
```

### B. Login
1.  **Server URL**: Enter `http://localhost:8000` (or your Ngrok URL if remote).
2.  **Username**: `student` (or `Yuval`).
3.  **Password**: `password` (or `19-07`).
4.  If the server is offline but you have logged in before, the app will log you in using cached credentials ("Offline Mode").

### C. Downloading Exams
1.  Click the **"Manage/Download Exams"** button on the start screen.
2.  The list will populate from the server.
3.  Select an exam and enter the password: `1234`.
4.  Click **Download**. The exam is extracted locally and ready for use.

### D. Taking an Exam (Offline Capable)
1.  Select the exam from the dropdown menus (Version, Language, Year).
2.  Pick a **Save Slot** (e.g., `save1`).
3.  Click **"Start Exam"**.
4.  The system tracks your timer and answers locally.
5.  If you close the app, your progress is saved in the SQLite database.

### E. Syncing Results
- When you finish an exam or restart the app with an internet connection, your analytics (scores, timing) are automatically sent to the server.

---

## 📦 4. Building Executables

To create a standalone file (`.exe`) that doesn't need Python installed:

1.  **Install Build Tools**:
    ```powershell
    pip install nuitka zstandard
    ```

2.  **Run Build Script**:
    ```powershell
    python build_app.py
    ```
    - This will generate `DigitalPsychometric.exe` (on Windows).
    - **Note**: Ensure you are in a clean environment. Conflicts between Conda and Pip packages can cause build failures.

3.  **Cross-Platform Builds**:
    To see the commands for building on macOS or Linux, run:
    ```powershell
    python build_app.py --all-cmds
    ```
    *You must run the specific command on the target OS to generate its binary.*

