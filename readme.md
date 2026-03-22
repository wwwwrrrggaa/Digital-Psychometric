# Digital-Psychometric (Offline-First Client-Server Architecture)

**Digital-Psychometric** is a comprehensive platform designed for digitizing, solving, and analyzing psychometric exams with a focus on robust offline capabilities. It transforms traditional paper-based exams into an interactive digital experience that remains fully functional without an internet connection.

This project implements a modern **Client-Server Architecture** where a central FastAPI server manages users, exams, and aggregated analytics, while a PySide6 desktop client handles local exam simulation, storage, and synchronization.

---

## 🏗️ Project Architecture & Design

### 1. Offline-First Desktop Client
The desktop application is built with **PySide6 (Qt for Python)** to ensure a responsive, native experience. 
- **Local Data Persistence**: Uses **SQLite** (`local_store.db`) to store user credentials, downloaded exam content, and performance analytics. This allows users to log in and take exams completely offline.
- **Smart Synchronization**: A dedicated `NetworkManager` queues analytics data (scores, timing) locally and automatically pushes it to the server when an internet connection is restored.
- **Exam Engine**: Renders PDF exams using **PyMuPDF**, manages timing per question, and calculates scores in real-time.

### 2. High-Performance Backend Server
The server is powered by **FastAPI**, a modern, high-performance web framework.
- **Centralized Data**: Uses **SQLAlchemy** (targeting PostgreSQL in production) to store all users, exam metadata, and global analytics.
- **Secure Distribution**: Endpoints for authentication (JWT) and secure exam file delivery.
- **Analytics Aggregation**: Receives synced data from clients to provide instructors with insights into student performance.

---

## 🛠️ Main Technologies

### Backend
- **FastAPI**: For high-performance API endpoints.
- **SQLAlchemy & Pydantic**: For ORM and data validation.
- **PostgreSQL / SQLite**: Database backend (SQLite used for local development).
- **Python-Multipart & Passlib**: For file uploads and secure password hashing.
- **JWT (JSON Web Tokens)**: Stateless authentication.

### Frontend
- **PySide6 (Qt6)**: Cross-platform GUI framework.
- **SQLite**: Embedded database for offline storage.
- **Requests**: HTTP client for API communication.
- **PyMuPDF**: Parsing and rendering PDF documents.
- **Nuitka**: Compilation of the Python application into standalone executables.

---

## ⚙️ How It Works

1.  **Authentication**: Users log in via the client. If online, the server validates credentials and issues a token. If offline, the client validates against a locally cached password hash from a previous successful login.
2.  **Exam Management**: Users browse available exams from the server via the **Exam Manager**. Exams are downloaded as encrypted packages, extracted locally, and registered in the local database.
3.  **Simulation & Tracking**:
    - Users take exams in a distracted-free GUI.
    - The app tracks **time spent per question** and **accuracy per chapter**.
    - All progress is saved locally to `local_store.db` to prevent data loss.
4.  **Synchronization**: Upon finishing an exam or reconnecting to the internet, the client pushes unsynced analytics records to the server's `POST /sync` endpoint.

---

## 📂 Repository Layout

- `server/`: Contains the FastAPI application, database models (`models.py`), and API routers (`routers/`).
- `start.py`: The entry point for the desktop client. Initializes the GUI and handles the login flow.
- `main.py`: The core logic for the exam simulation window and analytics tracking.
- `local_store.py`: Interface for the local SQLite database. Handles all offline data operations.
- `network_manager.py`: Handles all HTTP communication with the server and the sync logic.
- `exam_manager.py`: The GUI component for browsing and downloading exams.
- `login_window.py`: The initial login dialog with online/offline fallback logic.
- `operating.md`: Detailed guide on how to operate, host, and use the system.
- `build_app.py`: Script to compile the client into a standalone executable.

---

## 🔐 Default Credentials

The system comes pre-seeded with the following users for testing:

- **Student User**:
  - Username: `student`
  - Password: `password`

- **Alternative User**:
  - Username: `Yuval`
  - Password: `19-07`

- **Exam Download Password**:
  - Password: `1234`

---

## 📦 Building for Distribution

The project includes a `build_app.py` script that uses **Nuitka** to compile the client into a standalone executable (`.exe` on Windows, `.bin` on Linux, `.app` on macOS).

To build, run:
```bash
python build_app.py
```
*Note: You must build on the target operating system (e.g., build on Windows to get a Windows .exe).*

---

For detailed setup and running instructions, please refer to **[operating.md](operating.md)**.

