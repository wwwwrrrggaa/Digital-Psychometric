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


def get_answer_from_save(filename):
    with open(filename, "rb") as fp:
        return pickle.load(fp)


def save_grades(grades):
    filename = main.getsaveslot() + "\Grade\Grade.txt"
    with open(filename, "wb") as fp:
        pickle.dump(grades, fp)


def get_chapter_score(a, b):
    errorFormat = '<span style="color:red;">{}</span>'
    correctFormat = '<span style="color:green;">{}</span>'
    total = 0
    wronguser = []
    wrongcorrect = []
    for i in range(len(a)):
        if a[i] == b[i]:
            total += 1
            wronguser.append(str(a[i]))
            wrongcorrect.append(str(a[i]))

        else:
            wronguser.append(errorFormat.format(str(a[i])))
            wrongcorrect.append(correctFormat.format(str(b[i])))
    return total, wronguser, wrongcorrect


def fix_list(true_answers: list):
    # original implementation returned the list directly; preserve behavior
    return true_answers


def give_chapters(saveslot):
    shuffle = main.get_save_slot()
    shuffle = pickle.load(open(shuffle + "\Grade\Order.txt", "rb"))
    user_answers_file_names = [saveslot + "\\Answers\\" + file_name for file_name in os.listdir(saveslot + "\\Answers\\")]
    true_answers_file_names = [saveslot + "\\TrueAnswers\\" + file_name for file_name in os.listdir(saveslot + "\\TrueAnswers\\")]
    finalanswerlist = [0 for i in range(len(user_answers_file_names))]
    finaltruelist = [0 for i in range(len(user_answers_file_names))]
    for k in range(len(user_answers_file_names)):
        i = shuffle[k]
        nowlist = fix_list(get_answer_from_save(user_answers_file_names[k]))
        truelist = fix_list(get_answer_from_save(true_answers_file_names[i]))
        finalanswerlist[int(true_answers_file_names[k][-7])] = nowlist
        finaltruelist[int(true_answers_file_names[k][-7])] = truelist
    return finalanswerlist, finaltruelist


def get_img(saveslot):
    pass


class Window(PySide6.QtWidgets.QDialog):
    @staticmethod
    def _on_destroyed(self):
        sys.exit(0)

    def __init__(self,saveslot):
        super().__init__(parent=None)
        self.setWindowTitle("End-screen")
        height = self.height()
        width = self.width()

        dialogLayout = PySide6.QtWidgets.QHBoxLayout()
        formLayout = PySide6.QtWidgets.QFormLayout()
        answerLayout = PySide6.QtWidgets.QFormLayout()

        pic = PySide6.QtWidgets.QLabel()

        self.Box1 = PySide6.QtWidgets.QLabel()
        self.Box2 = PySide6.QtWidgets.QLabel()
        self.Box3 = PySide6.QtWidgets.QLabel()
        self.Box4 = PySide6.QtWidgets.QLabel()
        self.Box5 = PySide6.QtWidgets.QLabel()
        self.Box6 = PySide6.QtWidgets.QLabel()

        self.Box1.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box2.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box3.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box4.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box5.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        self.Box6.setFont(PySide6.QtGui.QFont("Aptos", font_size))

        a = PySide6.QtWidgets.QLabel()
        b = PySide6.QtWidgets.QLabel()
        c = PySide6.QtWidgets.QLabel()
        d = PySide6.QtWidgets.QLabel()
        e = PySide6.QtWidgets.QLabel()
        f = PySide6.QtWidgets.QLabel()

        a.setText("\u05E6\u05D9\u05D5\u05DF \u05DE\u05D9\u05DC\u05D5\u05DC\u05D9-\u05E2\u05D1\u05E8\u05D9\u05EA:")
        b.setText("\u05E6\u05D9\u05D5\u05DF \u05DB\u05DE\u05D5\u05EA\u05D9-\u05DE\u05EA\u05DE\u05D8\u05D9\u05E7\u05D4:")
        c.setText("\u05D0\u05E0\u05D2\u05DC\u05D9\u05EA-\u05E6\u05D9\u05D5\u05DF:")
        d.setText("\u05E6\u05D9\u05D5\u05DF \u05E8\u05D1 \u05EA\u05D7\u05D5\u05DE\u05D9:")
        e.setText("\u05E6\u05D9\u05D5\u05DF \u05E4\u05E1\u05D9\u05DB\u05D5\u05DE\u05D8\u05E8\u05D9:")
        f.setText("\u05E6\u05D9\u05D5\u05DF \u05DE\u05E9\u05D5\u05E7\u05DC\u05DC:")

        a.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        b.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        c.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        d.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        e.setFont(PySide6.QtGui.QFont("Aptos", font_size))
        f.setFont(PySide6.QtGui.QFont("Aptos", font_size))

        alist, tlist = give_chapters(saveslot)
        formLayout.addRow(self.Box1, a)
        formLayout.addRow(self.Box2, b)
        formLayout.addRow(self.Box3, c)
        formLayout.addRow(self.Box4, d)
        formLayout.addRow(self.Box5, e)
        formLayout.addRow(self.Box6, f)

        mathrawscore = 0
        hebrawscore = 0
        engrawscore = 0
        answerLayout.setSpacing(1)
        for i in range(len(alist)):
            alist[i] = alist[i][::-1]
            if "p" in tlist[i]:
                tlist[i].remove("p")
                grade, wronguser, wrongcorrect = get_chapter_score(alist[i], tlist[i])
                long = PySide6.QtWidgets.QLabel(str(wrongcorrect))
            else:
                grade, wronguser, wrongcorrect = get_chapter_score(alist[i], tlist[i])
                lenchapter = len(alist[i])
                if lenchapter == 20:
                    mathrawscore += grade
                elif lenchapter == 22:
                    engrawscore += grade
                elif lenchapter == 23:
                    hebrawscore += grade
                long = PySide6.QtWidgets.QLabel(str(wrongcorrect))
            short = PySide6.QtWidgets.QLabel(str(wronguser))

            shortbox = PySide6.QtWidgets.QLabel()
            longbox = PySide6.QtWidgets.QLabel()
            difbox = PySide6.QtWidgets.QLabel()
            shortbox.setText("\u05E4\u05E8\u05E7 {} \u05EA\u05E9\u05D5\u05D1\u05D5\u05EA:".format(str(i + 1)))
            longbox.setText(
                "\u05E4\u05E8\u05E7 {} \u05EA\u05E9\u05D5\u05D1\u05D5\u05EA \u05E0\u05DB\u05D5\u05DF\u05D5\u05EA:".format(
                    str(i + 1)))
            difbox.setText(
                "\u05E4\u05E8\u05E7 {} \u05E9\u05D2\u05D9\u05D0\u05D5\u05EA: {}".format(
                    str(i + 1), str(len(alist[i]) - grade)
                )
            )
            dif = PySide6.QtWidgets.QLabel()

            short.setFont(PySide6.QtGui.QFont("Aptos", font_size))
            dif.setFont(PySide6.QtGui.QFont("Aptos", font_size))
            long.setFont(PySide6.QtGui.QFont("Aptos", font_size))
            shortbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))
            difbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))
            longbox.setFont(PySide6.QtGui.QFont("Aptos", font_size))

            answerLayout.addRow(short, shortbox)
            answerLayout.addRow(dif, difbox)
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
        self.Box4.setText(str(a))
        self.Box5.setText(str(b))
        self.Box6.setText(str(c))

        dialogLayout.setSpacing(50)
        dialogLayout.addLayout(answerLayout)
        dialogLayout.addWidget(pic)
        dialogLayout.addLayout(formLayout)
        pic.setPixmap(
            PySide6.QtGui.QPixmap(
                main.get_save_slot() + r"\images\answer.png"
            ).scaledToHeight(self.window().height() * int(1.8))
        )
        pic.setAlignment(PySide6.QtGui.Qt.AlignmentFlag.AlignTop)

        self.setLayout(dialogLayout)
