# dialog.py
import os
import shutil

loadstate = 0
dir = os.path.realpath(__file__).replace("\start.py", "")
appdatafolder = dir
examsfolder = dir + "\Exams\\"
saveslot = dir + "\Saves\save1"
dirlib = dir + "\\"
import main


def getsaveslot():
    global saveslot
    return saveslot


def getappdata():
    return appdatafolder


def getexamsfolder(type):
    return dirlib + type + "\\"


def updatesaveslot(value):
    global saveslot
    saveslot = value


import os
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


def getlanguage():
    # path = getexamsfolder()
    # listlanguage = []
    # for language in os.listdir(path):
    # listlanguage.append(language)
    # return listlanguage
    return []


def getyears(type, language):
    path = getexamsfolder(type) + language
    listyear = []

    for year in os.listdir(path):
        listyear.append(year)
    return listyear


def getquarters(type, language, year):
    path = getexamsfolder(type) + language + "\\" + year
    listquarter = []
    for quarter in os.listdir(path):
        if len(quarter) == 1:
            quarter = quarter
        else:
            quarter = quarter[-5]
        listquarter.append(quarter)
    return listquarter


def getallslots():
    return os.listdir(getappdata() + "\Saves")


def gettimelimits():
    return ["10:00", "20:00", "25:00", "30:00", "60:00"]


def gettype():
    return ["FullExams", "Exams"]


def getsaveslots():
    return os.listdir(dir + "\Saves")


class Window(QDialog):
    def updateyear(self):
        self.Box2.clear()
        self.Box3.clear()
        self.Box2.addItems(getyears(self.Box0.currentText(), self.Box1.currentText()))

    def updatequarter(self):
        self.Box3.clear()
        self.Box3.addItems(
            getquarters(
                self.Box0.currentText(),
                self.Box1.currentText(),
                self.Box2.currentText(),
            )
        )

    def updatelanguage(self):
        self.Box1.clear()
        self.Box1.addItems(os.listdir(dirlib + self.Box0.currentText()))

    @staticmethod
    def _on_destroyed(self):
        global timer, exam
        main.mainapp(exam, timer)

    def Start(self):
        global exam, timer, saveslot, examtype, loadstate
        exam = (
            getexamsfolder(self.Box0.currentText())
            + self.Box1.currentText()
            + "\\"
            + self.Box2.currentText()
            + "\\"
            + self.Box3.currentText()
        )
        if os.path.isdir(exam):
            if self.Box0.currentText() == "Exams":
                updatesaveslot(self.Box5.currentText())
                timer = self.Box4.currentText()
                self.close()
                examtype = 0
            else:
                updatesaveslot(self.Box5.currentText())
                timer = self.Box4.currentText()
                self.close()
                examtype = 1
            imgpath = exam + r"\\answer.png"
            shutil.copy(
                imgpath,
                dirlib + r"Saves\\" + getsaveslot() + r"\images\answer.png",
            )
            loadstate = 0
        else:
            pass

    def load(self):
        global loadstate, examtype
        updatesaveslot(self.BoxSaves.currentText())
        savefolder = dirlib + r"Saves\\" + getsaveslot()
        len_true_answers = len(os.listdir(savefolder + "\\Trueanswers\\"))
        if len_true_answers == 6:
            examtype = 0
        else:
            examtype = 1
        loadstate = 1
        self.close()

    def SwitchMode(self):
        index = self.formLayout.count()
        index2 = index
        layou2 = QFormLayout()
        if self.ButtonMode.text() == "Load from save":
            while index >= 1:
                myWidget = self.formLayout.itemAt(0).widget()
                myWidget.setParent(None)
                index -= 1
            self.BoxSaves = QComboBox()
            self.BoxSaves.addItems(getallslots())
            self.formLayout.addRow("Save slot:", self.BoxSaves)
            self.ButtonMode.setText("Start new exam")
            self.ButtonOk.setParent(None)
            self.ButtonOk = QPushButton(self.tr("Enter Exam"))
            self.dialogLayout.addWidget(self.ButtonOk)
            self.ButtonOk.clicked.connect(self.load)
        else:
            while index >= 1:
                myWidget = self.formLayout.itemAt(0).widget()
                myWidget.setParent(None)
                index -= 1
            self.Box0 = QComboBox()
            self.Box1 = QComboBox()
            self.Box2 = QComboBox()
            self.Box3 = QComboBox()
            self.Box4 = QComboBox()
            self.Box5 = QComboBox()
            self.Box0.addItems(gettype())
            self.Box1.addItems(getlanguage())
            self.Box4.addItems(gettimelimits())
            self.Box5.addItems(getallslots())
            self.formLayout.addRow("Version:", self.Box0)
            self.formLayout.addRow("Language:", self.Box1)
            self.formLayout.addRow("Year:", self.Box2)
            self.formLayout.addRow("Quarter:", self.Box3)
            self.formLayout.addRow("TimeLimit:", self.Box4)
            self.formLayout.addRow("Choose save slot", self.Box5)
            self.Box0.activated.connect(self.updatelanguage)
            self.Box1.activated.connect(self.updateyear)
            self.Box2.activated.connect(self.updatequarter)
            self.updatelanguage()
            self.updateyear()
            self.updatequarter()
            self.ButtonMode.setText("Load from save")
            self.ButtonOk.setParent(None)
            self.ButtonOk = QPushButton(self.tr("Enter Exam"))
            self.dialogLayout.addWidget(self.ButtonOk)
            self.ButtonOk.clicked.connect(self.Start)

    def __init__(self):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("ChooseExam")
        self.dialogLayout = dialogLayout = QVBoxLayout()
        self.formLayout = formLayout = QFormLayout()
        self.Box0 = QComboBox()
        self.Box1 = QComboBox()
        self.Box2 = QComboBox()
        self.Box3 = QComboBox()
        self.Box4 = QComboBox()
        self.Box5 = QComboBox()
        self.Box0.addItems(gettype())
        self.Box1.addItems(getlanguage())
        self.Box4.addItems(gettimelimits())
        self.Box5.addItems(getallslots())
        formLayout.addRow("Version:", self.Box0)
        formLayout.addRow("Language:", self.Box1)
        formLayout.addRow("Year:", self.Box2)
        formLayout.addRow("Quarter:", self.Box3)
        formLayout.addRow("TimeLimit:", self.Box4)
        formLayout.addRow("Choose save slot", self.Box5)
        self.Box0.activated.connect(self.updatelanguage)
        self.Box1.activated.connect(self.updateyear)
        self.Box2.activated.connect(self.updatequarter)

        dialogLayout.addLayout(formLayout)
        self.ButtonOk = QPushButton(self.tr("Start Exam"))
        self.ButtonMode = QPushButton(self.tr("Load from save"))
        dialogLayout.addWidget(self.ButtonMode)
        dialogLayout.addWidget(self.ButtonOk)

        self.setLayout(dialogLayout)

        self.ButtonOk.clicked.connect(self.Start)
        self.ButtonMode.clicked.connect(self.SwitchMode)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
    main.mainapp(exam, timer, [saveslot, loadstate, examtype])
