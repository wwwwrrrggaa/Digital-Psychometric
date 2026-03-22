import os
import subprocess
import shutil
import sys

def build_for_platform(target_platform):
    """
    Simulates a cross-platform build command generation for instructions.
    """
    python_exe = "python" # Generic for instructions

    cmd = [
        python_exe, "-m", "nuitka",
        "--standalone",
    ]

    # Shared Nuitka options across all platforms to prevent bloat
    shared_options = [
        "--enable-plugin=pyside6",
        "--nofollow-import-to=scipy,pandas,numpy,matplotlib", # Prevent memory crashes
        "start.py"
    ]

    if target_platform == "windows":
        cmd.extend([
            "--onefile",
            "--windows-console-mode=disable", # Hides the black terminal window on launch
            "--output-filename=DigitalPsychometric.exe"
        ])
    elif target_platform == "macos":
        cmd.extend([
            "--macos-create-app-bundle",
            "--macos-app-mode=gui", # Ensures it runs as a standard Mac app
            "--output-filename=DigitalPsychometric"
        ])
    elif target_platform == "linux":
        cmd.extend([
            "--onefile",
            "--output-filename=DigitalPsychometric.bin"
        ])
    else:
        return

    cmd.extend(shared_options)
    return " ".join(cmd)

def build_all_instructions():
    print("="*60)
    print("CROSS-PLATFORM BUILD INSTRUCTIONS (NUITKA)")
    print("="*60)
    print("Note: Nuitka requires the target operating system to build the binary.")
    print("To generate all 3 versions, run these commands on the respective machines:\n")

    for plt in ["windows", "macos", "linux"]:
        print(f"--- {plt.upper()} ---")
        print(build_for_platform(plt))
        print()

def build():
    # Ensure current working directory is the script's directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    print(f"Working directory set to: {project_root}")

    # Clean previous build artifacts that Nuitka creates
    for folder in ["start.build", "start.dist", "start.onefile-build"]:
        if os.path.exists(folder):
            print(f"Cleaning old Nuitka artifact folder: {folder}...")
            shutil.rmtree(folder, ignore_errors=True)

    # Base Nuitka command using the current Python executable
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
    ]

    # Shared optimization and anti-bloat options
    shared_options = [
        "--enable-plugin=pyside6",
        "--nofollow-import-to=scipy,pandas,numpy,matplotlib", # Crucial for Windows memory limits
        "start.py"
    ]

    # Platform specific options
    if sys.platform == "win32":
        cmd.extend([
            "--onefile",
            "--windows-console-mode=disable", # Hides the terminal window
            "--output-filename=DigitalPsychometric.exe"
        ])
        output_name = "DigitalPsychometric.exe"

    elif sys.platform == "darwin": # macOS
        cmd.extend([
            "--macos-create-app-bundle",
            "--macos-app-mode=gui",
            "--output-filename=DigitalPsychometric"
        ])
        output_name = "DigitalPsychometric.app"

    else: # Linux/other
        cmd.extend([
            "--onefile",
            "--output-filename=DigitalPsychometric.bin"
        ])
        output_name = "DigitalPsychometric.bin"

    cmd.extend(shared_options)

    print("\nBuilding with Nuitka...")
    print("Command:", " ".join(cmd))
    print("-" * 40)

    try:
        # We use subprocess.call instead of check_call so we can handle the stream better
        result = subprocess.call(cmd)
        if result == 0:
            print(f"\n[SUCCESS] Build complete! Executable generated: {output_name}")
        else:
            print(f"\n[ERROR] Build failed with Nuitka exit code {result}")

    except FileNotFoundError:
        print("\n[ERROR] Python executable or Nuitka module not found.")
        print("Please ensure you are in an activated virtual environment and have run: pip install nuitka zstandard pyside6 pymupdf requests")

if __name__ == "__main__":
    if "--all-cmds" in sys.argv:
        build_all_instructions()
    else:
        build()