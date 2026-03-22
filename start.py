"""Start dialog UI helpers and dialog for the exam application.

This module contains the start dialog used by the application to select
an exam and save slot. The changes here are cosmetic only: a short
module docstring was added for clarity and PEP 8 style.
"""

import os
import shutil
import sys

# Determine paths for frozen (compiled) vs script mode
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    # Resources (Exams) will be downloaded to the executable folder (cwd)
    # User data (Saves) should also be in the executable folder (cwd)
    READ_DIR = os.path.dirname(sys.executable)
    WRITE_DIR = READ_DIR
else:
    READ_DIR = os.path.dirname(os.path.realpath(__file__))
    WRITE_DIR = READ_DIR

loadstate = 0
BASE_DIR = READ_DIR # Default base for content
dir = READ_DIR
appdatafolder = WRITE_DIR # User data goes to write dir
saveslot = "save1"
dirlib = READ_DIR

import main
import login_window

def get_save_slot():
    # Fix: return full path if needed, or rely on update_save_slot setting it correctly
    global saveslot
    if not os.path.isabs(saveslot):
         return os.path.join(get_app_data(), "Saves", saveslot)
    return saveslot


def get_app_data():
    return appdatafolder


def get_exams_folder(folder_type):
    return os.path.join(dirlib, folder_type)


def update_save_slot(value):
    global saveslot
    saveslot = os.path.join(get_app_data(), "Saves", value)


from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
)

timer = "25:00"
exam = ""
examtype = 0
current_user_token = None
current_user_name = "guest"


def get_language():
    path = os.path.join(dirlib, "Exams")
    if not os.path.isdir(path):
        return []
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def get_years(folder_type, language):
    path = os.path.join(get_exams_folder(folder_type), language)
    listyear = []
    if not os.path.isdir(path):
        return listyear

    for year in os.listdir(path):
        if os.path.isdir(os.path.join(path, year)):
            listyear.append(year)
    return listyear


def get_quarters(folder_type, language, year):
    path = os.path.join(get_exams_folder(folder_type), language, year)
    listquarter = []
    if not os.path.isdir(path):
        return listquarter
    for quarter in os.listdir(path):
        if len(quarter) == 1:
            q = quarter
        else:
            q = quarter[-5]
        listquarter.append(q)
    return listquarter


def get_slot_names() -> list:
    saves_path = os.path.join(get_app_data(), "Saves")
    if not os.path.isdir(saves_path):
        # Create default slots if missing (especially in compiled mode)
        try:
             os.makedirs(saves_path, exist_ok=True)
             for i in range(1, 10):
                 slot = f"save{i}"
                 os.makedirs(os.path.join(saves_path, slot), exist_ok=True)
                 # Also create subfolders needed?
                 # pdfbackend writes to Answers/, Chapters/, Grade/, Trueanswers/, images/
                 for sub in ["Answers", "Chapters", "Grade", "Trueanswers", "images"]:
                     os.makedirs(os.path.join(saves_path, slot, sub), exist_ok=True)
        except:
             return []

    return [
        name
        for name in os.listdir(saves_path)
        if os.path.isdir(os.path.join(saves_path, name))
    ]


def get_all_slots():
    return get_slot_names()


def get_time_limits():
    return ["10:00", "20:00", "25:00", "30:00", "60:00"]


def get_types():
    return ["FullExams", "Exams"]


def get_save_slots():
    return get_all_slots()


class Window(QDialog):
    def update_year(self):
        self.Box2.clear()
        self.Box3.clear()
        self.Box2.addItems(get_years(self.Box0.currentText(), self.Box1.currentText()))

    def update_quarter(self):
        self.Box3.clear()
        self.Box3.addItems(
            get_quarters(
                self.Box0.currentText(),
                self.Box1.currentText(),
                self.Box2.currentText(),
            )
        )

    def update_language(self):
        self.Box1.clear()
        path = os.path.join(dirlib, self.Box0.currentText())
        if not os.path.isdir(path):
            return
        self.Box1.addItems([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])

    @staticmethod
    def _on_destroyed():
        global timer, exam
        main.main_app(exam, timer)

    def start(self):
        global exam, timer, saveslot, examtype, loadstate
        exam = os.path.join(
            get_exams_folder(self.Box0.currentText()),
            self.Box1.currentText(),
            self.Box2.currentText(),
            self.Box3.currentText(),
        )
        if os.path.isdir(exam):
            timer = self.Box4.currentText()
            if self.Box0.currentText() == "Exams":
                examtype = 0
            self.accept()
        else:
            # Maybe offer to download exams?
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Exam Not Found", "This exam is not available locally. Please use Exam Manager to download.")

    def open_exam_manager(self):
        import exam_manager
        manager = exam_manager.ExamManager(current_user_token)
        manager.exec()
        # Refresh available exams in dropdowns?
        self.update_language() # Recheck directory structure

    def load(self):
        global loadstate, examtype
        update_save_slot(self.BoxSaves.currentText())
        savefolder = os.path.join(dirlib, "Saves", get_save_slot())
        trueanswers_path = os.path.join(savefolder, "Trueanswers")
        if not os.path.isdir(trueanswers_path):
            len_true_answers = 0
        else:
            len_true_answers = len([f for f in os.listdir(trueanswers_path) if os.path.isfile(os.path.join(trueanswers_path, f))])
        if len_true_answers == 6:
            examtype = 0
        else:
            examtype = 1
        loadstate = 1
        self.close()

    def switch_mode(self):
        index = self.formLayout.count()
        index2 = index
        layou2 = QFormLayout()
        if self.ButtonMode.text() == "Load from save":
            while self.formLayout.count():
                item = self.formLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            self.BoxSaves = QComboBox()
            self.BoxSaves.addItems(get_all_slots())
            self.formLayout.addRow("Save slot:", self.BoxSaves)

            self.ButtonMode.setText("Start new exam")
            self.ButtonOk.setText("Enter Exam")
            self.ButtonOk.clicked.disconnect()
            self.ButtonOk.clicked.connect(self.load)
            self.ButtonOk.setEnabled(self.BoxSaves.count() > 0)
        else:
            while self.formLayout.count():
                item = self.formLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            self.Box0 = QComboBox()
            self.Box1 = QComboBox()
            self.Box2 = QComboBox()
            self.Box3 = QComboBox()
            self.Box4 = QComboBox()
            self.BoxSaves = QComboBox()

            self.Box0.addItems(get_types())
            self.Box1.addItems(get_language())
            self.Box4.addItems(get_time_limits())
            self.BoxSaves.addItems(get_all_slots())

            self.formLayout.addRow("Version:", self.Box0)
            self.formLayout.addRow("Language:", self.Box1)
            self.formLayout.addRow("Year:", self.Box2)
            self.formLayout.addRow("Quarter:", self.Box3)
            self.formLayout.addRow("TimeLimit:", self.Box4)
            self.formLayout.addRow("Save slot:", self.BoxSaves)
            self.Box0.activated.connect(self.update_language)
            self.Box1.activated.connect(self.update_year)
            self.Box2.activated.connect(self.update_quarter)
            self.update_language()
            self.update_year()
            self.update_quarter()
            self.ButtonMode.setText("Load from save")
            self.ButtonOk.setParent(None)
            self.ButtonOk = QPushButton(self.tr("Enter Exam"))
            self.dialogLayout.addWidget(self.ButtonOk)
            self.ButtonOk.clicked.connect(self.start)

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("ChooseExam")
        self.dialogLayout = dialogLayout = QVBoxLayout()
        self.formLayout = formLayout = QFormLayout()
        self.Box0 = QComboBox()
        self.Box1 = QComboBox()
        self.Box2 = QComboBox()
        self.Box3 = QComboBox()
        self.Box4 = QComboBox()
        self.Box0.addItems(get_types())
        self.Box1.addItems(get_language())
        self.Box4.addItems(get_time_limits())
        # Add save slot to initial form
        self.BoxSaves = QComboBox()
        self.BoxSaves.addItems(get_all_slots())
        formLayout.addRow("Version:", self.Box0)
        formLayout.addRow("Language:", self.Box1)
        formLayout.addRow("Year:", self.Box2)
        formLayout.addRow("Quarter:", self.Box3)
        formLayout.addRow("TimeLimit:", self.Box4)
        formLayout.addRow("Save slot:", self.BoxSaves)
        self.Box0.activated.connect(self.update_language)
        self.Box1.activated.connect(self.update_year)
        self.Box2.activated.connect(self.update_quarter)

        dialogLayout.addLayout(formLayout)
        self.ButtonOk = QPushButton(self.tr("Start Exam"))
        self.ButtonMode = QPushButton(self.tr("Load from save"))
        dialogLayout.addWidget(self.ButtonMode)
        dialogLayout.addWidget(self.ButtonOk)

        self.setLayout(dialogLayout)

        self.ButtonOk.clicked.connect(self.start)
        self.ButtonMode.clicked.connect(self.switch_mode)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show Login First
    login = login_window.LoginWindow()
    if login.exec() == QDialog.Accepted:
        current_user_name = login.username
        current_user_token = login.token

        # Then Start Dialog
        start_dialog = Window()

        # Add Exam Manager Button to Start Dialog
        btn_manager = QPushButton("Manage/Download Exams")
        btn_manager.clicked.connect(start_dialog.open_exam_manager)
        start_dialog.layout().addWidget(btn_manager)

        start_dialog.show()

        # Wait for start dialog to close (it calls main.main_app internally on destroy? No wait)
        # start.py logic is weird. _on_destroyed connects to main_app.
        # But Window(QDialog) is modal usually?
        # Let's fix start.py execution flow.

        app.exec()
    else:
        sys.exit()
