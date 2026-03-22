from pathlib import Path

import uvicorn

if __name__ == "__main__":
    # Get the project root directory
    project_root = Path(__file__).resolve().parent

    print(f"Starting server from: {project_root}")

    # Run uvicorn programmatically
    # equivalent to: uvicorn server.main:app --host 0.0.0.0 --port 8000
    # Removed reload=True to avoid potential Windows process spawning issues in some environments
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=False)
