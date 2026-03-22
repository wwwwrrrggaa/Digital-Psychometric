import os
import subprocess
import shutil
import sys

def build_for_platform(target_platform):
    """
    Simulates a cross-platform build command generation.
    Note: Nuitka generally requires being on the target OS to build for it.
    However, we can generate the command strings for the user.
    """
    python_exe = "python" # Generic for instructions

    cmd = [
        python_exe, "-m", "nuitka",
        "--standalone",
    ]

    if target_platform == "windows":
        cmd.append("--onefile")
        output_name = "DigitalPsychometric.exe"
    elif target_platform == "macos":
        cmd.append("--macos-create-app-bundle")
        output_name = "DigitalPsychometric"
    elif target_platform == "linux":
        cmd.append("--onefile")
        output_name = "DigitalPsychometric.bin"
    else:
        return

    cmd.extend([
        "--enable-plugin=pyside6",
        f"--output-filename={output_name}",
        "--include-module=server.models",
        "--include-module=server.database",
        "--include-module=requests",
        "--include-module=local_store",
        "--include-module=network_manager",
        "--include-module=exam_manager",
        "--include-module=login_window",
        "start.py"
    ])

    return " ".join(cmd)

def build_all_instructions():
    print("="*60)
    print("CROSS-PLATFORM BUILD INSTRUCTIONS")
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

    # Clean previous builds
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"Cleaning {folder}...")
            shutil.rmtree(folder)

    # Nuitka command
    # Using sys.executable ensures we use the same python interpreter that ran this script
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
    ]

    # Platform specific options
    if sys.platform == "win32":
        cmd.append("--onefile")
        output_name = "DigitalPsychometric.exe"
    elif sys.platform == "darwin": # macOS
        cmd.append("--macos-create-app-bundle")
        output_name = "DigitalPsychometric"
    else: # Linux/other
        cmd.append("--onefile")
        output_name = "DigitalPsychometric.bin"

    cmd.extend([
        "--enable-plugin=pyside6",
        f"--output-filename={output_name}",
        "--include-module=server.models",
        "--include-module=server.database",
        "--include-module=requests",
        "--include-module=local_store",
        "--include-module=network_manager",
        "--include-module=exam_manager",
        "--include-module=login_window",
        "start.py"
    ])

    print("Building with Nuitka...")
    print("Command:", " ".join(cmd))

    try:
        subprocess.check_call(cmd)
        print(f"\nBuild complete. Executable is likely in DigitalPsychometric.dist/{output_name} or similar (depending on Nuitka version/platform).")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error code {e.returncode}")
    except FileNotFoundError:
        print("\nError: Python executable or Nuitka module not found. Make sure 'nuitka' is installed in your environment.")

if __name__ == "__main__":
    if "--all-cmds" in sys.argv:
        build_all_instructions()
    else:
        build()
