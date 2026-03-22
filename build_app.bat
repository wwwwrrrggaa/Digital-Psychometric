@echo off
rem Build the Digital Psychometric App with Nuitka
rem Requires Nuitka and dependencies installed
rem pip install nuitka zstandard

echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist

echo Building...
python -m nuitka ^
 --standalone ^
 --onefile ^
 --enable-plugin=pyside6 ^
 --include-data-dir="Exams=Exams" ^
 --include-data-dir="FullExams=FullExams" ^
 --include-data-dir="Saves=Saves" ^
 --output-filename=DigitalPsychometric ^
 --include-module=server.models ^
 --include-module=server.database ^
 --include-module=requests ^
 --include-module=local_store ^
 --include-module=network_manager ^
 --include-module=exam_manager ^
 --include-module=login_window ^
 start.py

echo Build complete. executable is in current directory or dist folder.
pause

