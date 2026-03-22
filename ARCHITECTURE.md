# Architecture & Technical Details

## 1. Data Path Logic (`.exe` vs `.py`)

In `start.py`, you will see a check for `sys.frozen`. This is critical for handling file paths correctly when the application is compiled into a standalone executable.

```python
if getattr(sys, 'frozen', False):
    # FROZEN MODE (Running as .exe)
    READ_DIR = os.path.dirname(sys.executable)
    WRITE_DIR = READ_DIR
else:
    # SCRIPT MODE (Running as .py)
    READ_DIR = os.path.dirname(os.path.realpath(__file__))
    WRITE_DIR = READ_DIR
```

### Why is this needed?
- **Script Mode**: When running `python start.py`, your user data (`Saves/`) and resources (`Exams/`) are in the same folder as the script. `__file__` reliably points to this location.
- **Frozen Mode (Nuitka/PyInstaller)**: When compiled to a single file, the executable unpacks its *internal* resources to a temporary folder (often `sys._MEIPASS`) that is deleted when the app closes. 
- **The Problem**: If we saved user progress (`Saves/`) to this temporary folder, **all data would be lost** every time you closed the app.
- **The Solution**: We explicitly set the `WRITE_DIR` to `os.path.dirname(sys.executable)`, which is the folder where the `.exe` file itself sits. This ensures that the `Saves/` and `Exams/` folders are created next to the application and persist between runs.

---

## 2. Application States (Finite State Machine)

The application moves through several distinct stages during its lifecycle.

### Stage 1: Initialization (`start.py`)
- **Action**: App launch.
- **Tasks**: 
  - Detect execution mode (Script vs Frozen).
  - Initialize the local SQLite database (`local_store.py`).
  - Create necessary directories (`Saves/`, `Exams/`) if missing.

### Stage 2: Authentication (`LoginWindow`)
- **Action**: User enters credentials.
- **Branch A: Online Login**
  - App contacts `POST /login`.
  - **Success**: Token received. Credentials cached locally. Unsynced analytics push to server. -> **To Stage 3**.
  - **Fail (Credentials)**: Show error. Stay in Stage 2.
  - **Fail (Network)**: Fallback to Branch B.
- **Branch B: Offline Login**
  - App hashes entered password and compares with local DB `local_users` table.
  - **Success**: Log in as local user. Sync is deferred. -> **To Stage 3**.
  - **Fail**: Show "No cached credentials" error. Stay in Stage 2.

### Stage 3: Main Menu (`Window` in `start.py`)
- **Action**: User selects an action.
- **Option A: Exam Manager**
  - Browse server exams. Download (decrypt & unzip) to local folder.
- **Option B: Start New Exam**
  - Select Exam/Year/Language.
  - Initialize `Exam State` (Timer set, Tracker reset). -> **To Stage 4**.
- **Option C: Load Save**
  - Read `Saves/saveX/` data. Restore state. -> **To Stage 4**.

### Stage 4: Exam Simulation (`main.py` & `mainwindow.py`)
- **Action**: The active test environment.
- **Mechanics**:
  - **PDF Viewer**: Renders exam pages.
  - **Focus Tracking**: `TimeTracker` records milliseconds spent on each question input.
  - **State Changes**: Next/Prev Chapter.
- **Exit Paths**:
  - **Save & Quit**: Serializes state to `Saves/` and SQLite `exam_inprogress`. -> **Exit**.
  - **Finish Exam**: Calculates scores. Saves final analytics record. -> **To Stage 5**.

### Stage 5: Results & Analytics (`end.py`)
- **Action**: Review performance.
- **Tasks**:
  - Display raw score, weighted psychometric score.
  - Show per-chapter breakdown (Correct/Incorrect).
  - List answer key vs user answers.
- **Exit**: Closes application.

---

## 3. Multi-User Handling

The application supports multiple users on a single machine via the `local_store.db`.

- **Data Isolation**: 
  - `local_users` table stores unique usernames and their hashed passwords.
  - `local_analytics` table includes a `username` column.
- **Session Handling**: 
  - When User A logs in, `start.py` sets `current_user_name = "UserA"`.
  - All analytics saved during the session are tagged with `"UserA"`.
  - When syncing, only records belonging to `"UserA"` (or the currently logged-in user) are sent to the server.
- **Resource Control**:
  - Downloaded exams are not globally visible. Access is strictly controlled via the user's entry in `local_store.db`.
  - The database maintains a mapping of `user_id` to specific file paths for downloaded exams.
  - **Security**: Exam files are encrypted using the user's password. This ensures that even if multiple users share a machine, one user cannot access or open another user's exam files without the correct login credentials.

