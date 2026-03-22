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
import local_store

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
    # Check downloaded exams for this language and populate years
    # Keep directory scan for robustness but prioritize or merge?
    # Simple directory scan is fine if download puts them in right place.
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
        # Handle simple folder names first
        if os.path.isdir(os.path.join(path, quarter)) or os.path.exists(os.path.join(path, quarter)):
             # Previous logic had weird slicing: if len(quarter) == 1: q=quarter else q=quarter[-5]
             # This was likely for full filenames like "Hebrew-2024-2.pdf" -> '2'
             # If we use folders, we just use the folder name.
             if os.path.isdir(os.path.join(path, quarter)):
                  listquarter.append(quarter)
             else:
                  # Fallback for file-based
                  pass

    # If empty, maybe try scanned files?
    if not listquarter:
        for f in os.listdir(path):
             if f.endswith(".pdf"):
                  # Try to extract quarter from filename if standardization exists
                  # But our new download logic puts them in folders.
                  pass

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

DARK_THEME_SS = """"""

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
        if not os.path.isdir(exam):
            # Maybe offer to download exams?
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Exam Not Found", f"This exam is not available locally at {exam}. Please use Exam Manager to download.")
            return # Don't start

        # Check for required metadata files
        if self.Box0.currentText() == "FullExams" or self.Box0.currentText() == "Exams":
            required_files = ["answers.txt", "pagelist.txt"]
            missing = [f for f in required_files if not os.path.exists(os.path.join(exam, f))]
            if missing:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Invalid Exam", f"The exam files are incomplete (missing {', '.join(missing)}).\n\nIf you recently downloaded this exam, it might be corrupted or in raw format (PDF only).")
                return

        if os.path.isdir(exam):
            timer = self.Box4.currentText()
            if self.Box0.currentText() == "Exams":
                examtype = 0
            self.accept()
        else:
             # Should be covered above
             pass

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

            # Initial population of options based on default type
            self.update_language()
            self.update_year()
            self.update_quarter()

            self.dialogLayout.addLayout(self.formLayout)
            self.ButtonOk = QPushButton(self.tr("Enter Exam"))
            self.ButtonOk.setParent(None)
            self.dialogLayout.addWidget(self.ButtonOk)
            self.ButtonOk.clicked.connect(self.start)
            self.ButtonMode.setText("Load from save")

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("ChooseExam")

        # Apply Global Dark Theme Stylesheet
        self.setStyleSheet(DARK_THEME_SS)

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

        # Initial population of options based on default type
        self.update_language()
        self.update_year()
        self.update_quarter()

        dialogLayout.addLayout(formLayout)
        self.ButtonOk = QPushButton(self.tr("Start Exam"))
        self.ButtonMode = QPushButton(self.tr("Load from save"))
        dialogLayout.addWidget(self.ButtonMode)
        dialogLayout.addWidget(self.ButtonOk)

        self.setLayout(dialogLayout)

        self.ButtonOk.clicked.connect(self.start)
        self.ButtonMode.clicked.connect(self.switch_mode)

        # Reset Cache Button
        self.btn_reset = QPushButton("Reset Cache (Delete all data)")
        self.btn_reset.setStyleSheet("background-color: #dc3545; color: white; margin-top: 10px;")
        self.btn_reset.clicked.connect(self.do_reset_cache)
        dialogLayout.addWidget(self.btn_reset)

    def do_reset_cache(self):
        # We need password confirmation again? Or just warning since we are logged in?
        # User is already past login. But destructive action usually requires confirmation.
        # Since we don't store password in memory securely to reuse verify, prompt again?
        # Or just big warning.
        # Let's prompt for password to be safe, using a small dialog.

        from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox

        # Simple confirmation first
        reply = QMessageBox.question(self, 'Reset Local Cache',
                                     "Are you sure you want to delete all downloaded exams, saves, and progress? This cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
              # Since we are already logged in (possibly), should we require re-auth?
              # If guest, no password.
              # If logged in user, maybe yes.
              # But let's keep it simple: just reset if confirmed.
              # Unless user wants password check as previous implementation.
              # "reset local cache option(enter the password again and confirm to do so...)"

              if current_user_name != "guest":
                   pwd, ok = QInputDialog.getText(self, "Confirm Reset", "Enter your password to confirm:", QLineEdit.Password)
                   if ok and pwd:
                        local_user = local_store.get_local_user(current_user_name)
                        if local_user and local_store.verify_password(pwd, local_user['hashed_password']):
                             pass # Proceed
                        else:
                             QMessageBox.warning(self, "Error", "Invalid password.")
                             return
                   else:
                        return

              try:
                  local_store.reset_all_data()
                  QMessageBox.information(self, "Reset Complete", "Local cache has been reset. The application will close.")
                  sys.exit()
              except Exception as e:
                  QMessageBox.critical(self, "Error", f"Failed to reset cache: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_SS) # Apply to entire app

    # Show Login First
    login = login_window.LoginWindow()
    if login.exec() == QDialog.Accepted:
        current_user_name = login.username
        current_user_token = login.token

        # Then Start Dialog
        start_dialog = Window()

        # Add Exam Manager Button to Start Dialog
        btn_manager = QPushButton("Manage/Download Exams")
        btn_manager.setObjectName("updateBtn") # Re-use style if available or default to QPushButton
        btn_manager.clicked.connect(start_dialog.open_exam_manager)
        start_dialog.layout().addWidget(btn_manager)

        # start_dialog.show()
        # app.exec()
        # FIX: Use exec loop and check result to run main app

        if start_dialog.exec() == QDialog.Accepted:
             # Construct args for main.main_app
             # Arguments logic based on main.py analysis:
             # If loading from save (resume):
             # args = [[save_slot, 1, 0]] (assuming 1 is resume type, 0 is generic subtype)
             # If new exam:
             # args = [[save_slot, 0, 0]] (assuming 0 is new exam type, 0 is generic subtype)

             # loadstate is global set in load()
             # examtype is global set in start() / load()
             # saveslot is global set in start() / load()
             # saveslot path needs to be slot NAME?
             # update_save_slot in main.py takes value and joins with path.
             # so we pass slot name.

             slot_name = os.path.basename(saveslot) if os.path.isabs(saveslot) else saveslot

             args = [[slot_name, loadstate, examtype]] # Nested list as main.py does args[0][1]
             # exam path is global 'exam'

             # Run main app
             main.main_app(args, timer, exam)

    else:
        sys.exit()
