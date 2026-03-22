# dialog.py

"""Dialog-style application."""
import os
import pickle
import sys

import PySide6.QtGui
import PySide6.QtWidgets

import main
import pdfbackend

font_size=12


def getanswerfromsave(filename):
    with open(filename, "rb") as fp:
        return pickle.load(fp)


def savegrades(grades):
    filename = main.get_save_slot() + r"\Grade\Grade.txt"
    with open(filename, "wb") as fp:
        pickle.dump(grades, fp)


def getchapterscore(a, b):
    errorFormat = '<span style="color:red;">{}</span>'
    correctFormat = '<span style="color:green;">{}</span>'
    total = 0
    sum=0
    wronguser = []
    wrongcorrect = []
    for i in range(len(a)):
        if a[i] == b[i]:
            sum += 1
            total += 1
            wronguser.append(str(a[i]))
            wrongcorrect.append(str(a[i]))

        else:
            wronguser.append(errorFormat.format(str(a[i])))
            wrongcorrect.append(correctFormat.format(str(b[i])))
    return sum, wronguser, wrongcorrect


def fixlist(true_answers:list):
    return [int(x) for x  in true_answers if x!="p"]

def givechapters(saveslot):
    shuffle = main.get_save_slot()
    shuffle = pickle.load(open(shuffle + r"\Grade\Order.txt", "rb"))
    user_answers_file_names = [saveslot+r"\Answers\\"+file_name for file_name in os.listdir(saveslot+r"\Answers\\")]
    true_answers_file_names = [saveslot+r"\TrueAnswers\\"+file_name for file_name in os.listdir(saveslot+r"\TrueAnswers\\")]
    finalanswerlist = [0 for i in range(len(user_answers_file_names))]
    finaltruelist = [0 for i in range(len(user_answers_file_names))]
    for k in range(len(user_answers_file_names)):
        i = shuffle[k]
        nowlist = fixlist(getanswerfromsave(user_answers_file_names[k]))
        truelist = fixlist(getanswerfromsave(true_answers_file_names[i]))
        finalanswerlist[int(true_answers_file_names[k][-7])] = nowlist
        finaltruelist[int(true_answers_file_names[k][-7])] = truelist
    return finalanswerlist, finaltruelist


def getimg(saveslot):
    pass


class Window(PySide6.QtWidgets.QDialog):
    def _on_destroyed(self):
        # sys.exit()
        pass

    def __init__(self,saveslot):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("End-screen")
        height = self.height()
        width = self.width()
        dialogLayout = PySide6.QtWidgets.QHBoxLayout()
        formLayout = PySide6.QtWidgets.QFormLayout()

        answerLayout = PySide6.QtWidgets.QFormLayout()

        # answerLayout.setVerticalSpacing(20)
        # answerLayout.setHorizontalSpacing(30)

        pic = PySide6.QtWidgets.QLabel()
        dialogLayout.addWidget(pic)

        scroll = PySide6.QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        # scroll.setFixedWidth(500)
        scroll.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollContent = PySide6.QtWidgets.QWidget()
        scrollContent.setLayout(formLayout)
        scroll.setWidget(scrollContent)

        dialogLayout.addWidget(scroll)
        dialogLayout.addLayout(answerLayout)

        self.Box1 = PySide6.QtWidgets.QLabel()
        self.Box2 = PySide6.QtWidgets.QLabel()
        self.Box3 = PySide6.QtWidgets.QLabel()
        self.Box4 = PySide6.QtWidgets.QLabel()
        self.Box5 = PySide6.QtWidgets.QLabel()
        self.Box6 = PySide6.QtWidgets.QLabel()

        a = PySide6.QtWidgets.QLabel("Hebrew Score:")
        b = PySide6.QtWidgets.QLabel("Math Score:")
        c = PySide6.QtWidgets.QLabel("English Score:")
        d = PySide6.QtWidgets.QLabel("Score without math:")
        e = PySide6.QtWidgets.QLabel("Score without hebrew:")
        f = PySide6.QtWidgets.QLabel("General Score:")

        self.Box1.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box2.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box3.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box4.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box5.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box6.setFont(PySide6.QtGui.QFont("Aptos", font_size))

        a.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        b.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        c.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        d.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        e.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        f.setFont(PySide6.QtGui.QFont("Aptos", font_size))

        alist, tlist = givechapters(saveslot)
        formLayout.addRow(self.Box1, a)
        formLayout.addRow(self.Box2, b)
        formLayout.addRow(self.Box3, c)
        formLayout.addRow(self.Box4, d)
        formLayout.addRow(self.Box5, e)
        formLayout.addRow(self.Box6, f)

        # self.boxes=[]
        mathrawscore = 0
        hebrawscore = 0
        engrawscore = 0

        for i in range(len(alist)):
            alist[i] = alist[i][::-1]
            if "p" in tlist[i]:
                tlist[i].remove("p")
            else:
                grade, wronguser, wrongcorrect = getchapterscore(alist[i], tlist[i])
                lenchapter = len(alist[i])
                if lenchapter == 20:
                    mathrawscore += grade
                elif lenchapter == 22:
                    engrawscore += grade
                elif lenchapter == 23:
                    hebrawscore += grade
                # hme
                long = PySide6.QtWidgets.QLabel(str(wrongcorrect))
                short = PySide6.QtWidgets.QLabel(str(wronguser))

                long.setWordWrap(True)
                short.setWordWrap(True)

                long.setFont(PySide6.QtGui.QFont("Aptos", font_size))
                short.setFont(PySide6.QtGui.QFont("Aptos", font_size))

                longbox = PySide6.QtWidgets.QLabel()
                shortbox = PySide6.QtWidgets.QLabel()
                difbox = PySide6.QtWidgets.QLabel()
                shortbox.setText("\u05E4\u05E8\u05E7 {} \u05EA\u05E9\u05D5\u05D1\u05D5\u05EA:".format(str(i + 1)))
                longbox.setText(
                    "\u05E4\u05E8\u05E7 {} \u05EA\u05E9\u05D5\u05D1\u05D5\u05EA \u05E0\u05DB\u05D5\u05DF\u05D5\u05EA:".format(
                        str(i + 1)))
                difbox.setText(
                    "\u05E4\u05E8\u05E7 {} \u05E9\u05D2\u05D9\u05D0\u05D5\u05EA: {}".format(
                        str(i + 1), str(lenchapter - grade)
                    )
                )

                longbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))
                shortbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))
                difbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))

                answerLayout.addRow(difbox, PySide6.QtWidgets.QLabel())
                answerLayout.addRow(short, shortbox)
                answerLayout.addRow(long, longbox)
                answerLayout.addRow(PySide6.QtWidgets.QLabel())
                answerLayout.addRow(PySide6.QtWidgets.QLabel())

        gradingkey = pickle.load(open(saveslot + r"\Grade\gradingkey.txt", 'rb'))
        a, b, c = pdfbackend.give_final_scores(
            [str(hebrawscore), str(mathrawscore), str(engrawscore)], gradingkey
        )

        self.Box1.setText(str(hebrawscore))
        self.Box2.setText(str(mathrawscore))
        self.Box3.setText(str(engrawscore))
        self.Box4.setText(str(b))
        self.Box5.setText(str(c))
        self.Box6.setText(str(a))
        savegrades([str(hebrawscore), str(mathrawscore), str(engrawscore), str(b), str(c), str(a)])
        self.setLayout(dialogLayout)
        pic.setPixmap(
            PySide6.QtGui.QPixmap(
                main.get_save_slot() + r"\images\answer.png"
            ).scaledToHeight(self.window().height() * int(1.8))
        )
        pic.setAlignment(PySide6.QtGui.Qt.AlignmentFlag.AlignTop)

        # self.ButtonExit = PySide6.QtWidgets.QPushButton(self.tr("Exit"))
        # dialogLayout.addWidget(self.ButtonExit)
        # self.ButtonExit.clicked.connect(self._on_destroyed)

    def closeEvent(self, event):
        # Override close event to exit the application properly
        self._on_destroyed()
        event.accept()

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)
    saveslot = "save1" # Default or passed arg
    dialog = Window(saveslot)
    dialog.showMaximized()
    sys.exit(app.exec())

