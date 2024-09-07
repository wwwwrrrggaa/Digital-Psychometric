# DigitalPsychometric

DigitalPsychometric is a tool for digitizing printed psychometric exams and making the simulation process easier.



## Getting Started:

### Dependencies
python 3.x

pyside 6

pymupdf

all the required data folders inside the same directory 

nuitka in order to compile

I used conda to build a virtual env for the project myself

### Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/yourusername/Digital-Psychometric.git
2. Navigate to the project directory:
    cd OnlinePsychometric
3. Install the required dependencies
4. Activate the virtual environment:
    conda activate OnlinePsychometric


### Usage
Run start.py to start into the gui


### Build
To build the project into a standalone exe, use the following commands on an existing conda env with the required dependencies:
``` bash
conda activate OnlinePsychometric
python -m nuitka --follow-imports --standalone --disable-console --onefile --enable-plugin=pyside6 --include-data-dir=C:\Users\yonat\PycharmProjects\OnlinePsychometric2\Data= C:\Users\yonat\pycharmprojects\OnlinePsychometric2\start.py
```

## About the project

### How this works

The project is structured around five key files, each serving a specific purpose:

1. **start.py**:
   - This file serves as the entry point for the application. It initializes the GUI and allows the user to choose from starting a new exam and loading from a save finally calling main.py .

2. **main.py**:
   - This file calls the gui and logic for processing an exam and displaying it to the user. the main logic function is called per each chapter in the exam until it calls end.py

3. **end.py**:
   - This file displays the end stats after a user finishes the exam and then calculates the required grades.
4. **pdfbackend.py**:
   - This file contains the basic pdf and backedn logic required to extract the required information from the data directories and transfer it accordingly, it is also contains logic to save the generated data.

5. **Exampreprocessing.py**:
   - This file contains preprocessing logic for the exams. It handles tasks such as extracting data from PDFs, organizing the data into a usable format, and preparing the exams for simulation, basically what's required to create all exam folders .

other files are basicly the pyside gui
]()
### Todo List

- [v] Work on any computer (bundle files with exe)
- [v] Give correct Hebrew score without essay
- [V] More save slots
- [v] Remove bad UI elements
- [v] Show actual grade
- [v] Shuffle chapters
- [ ] Resume from save (Now)
- [V] Campus IL version
- [x] Bug fixes
- [ ] Manual checks (After Now)
- [ ] Essay grader (future version)
- [v] End screen
- [ ] Refactor code and publish?


written with the help of chatgpt
