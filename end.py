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
    total_score = 0
    wronguser = []
    wrongcorrect = []

    # Iterate up to the length of the shorter list to avoid index error
    limit = min(len(a), len(b))

    for i in range(limit):
        # Comparison robust to types (str vs int)
        if str(a[i]) == str(b[i]):
            total_score += 1
            # For correct answers, just show the answer
            wronguser.append(str(a[i]))
            wrongcorrect.append(str(b[i]))
        else:
            # For wrong answers, show highlighted diff
            wronguser.append(errorFormat.format(str(a[i])))
            wrongcorrect.append(correctFormat.format(str(b[i])))

    return total_score, wronguser, wrongcorrect


def fixlist(true_answers: list):
    if not isinstance(true_answers, list):
        print(f"DEBUG: fixlist received non-list: {type(true_answers)}")
        return []
    result = []
    for x in true_answers:
        if x == "p":
            continue
        try:
            # Handle potential empty strings if user skipped question
            if isinstance(x, str) and not x.strip():
                # Treat empty answer as 0 or ignore?
                # Usually unanswered is 0 or -1. Let's use 0 to indicate valid slot but wrong answer.
                result.append(0)
            else:
                result.append(int(x))
        except (ValueError, TypeError):
            print(f"DEBUG: Skipping invalid answer value: {x}")
            # Append 0 so indices stay aligned?
            result.append(0)
    return result

def givechapters(saveslot):
    save_path = main.get_save_slot()
    order_path = os.path.join(save_path, r"Grade\Order.txt")
    with open(order_path, "rb") as f:
        shuffle = pickle.load(f)

    num_chapters = len(shuffle)
    finalanswerlist = [[] for _ in range(num_chapters)]
    finaltruelist = [[] for _ in range(num_chapters)]

    print(f"DEBUG: givechapters called for {saveslot}")
    answers_dir = os.path.join(save_path, "Answers")
    true_answers_dir = os.path.join(save_path, "Trueanswers")
    print(f"DEBUG: Using answers_dir={answers_dir}, true_answers_dir={true_answers_dir}")

    true_files_map = {}
    if os.path.exists(true_answers_dir):
        files = sorted(os.listdir(true_answers_dir), key=lambda f: int(f.split("-")[0]) if "-" in f and f.split("-")[0].isdigit() else f)
        print(f"DEBUG: Found {len(files)} files in Trueanswers: {files}")
        for fname in files:
            parts = fname.split('-')
            if parts and parts[0].isdigit():
                true_files_map[int(parts[0])] = os.path.join(true_answers_dir, fname)

    answer_files = sorted(os.listdir(answers_dir), key=lambda f: int(os.path.splitext(f)[0]) if os.path.splitext(f)[0].isdigit() else f) if os.path.exists(answers_dir) else []

    for k in range(num_chapters):
        user_file = os.path.join(answers_dir, f"{k}.txt")
        exam_chapter_idx = shuffle[k] if k < len(shuffle) else k
        true_file = true_files_map.get(exam_chapter_idx)

        if os.path.exists(user_file):
            try:
                raw_user = getanswerfromsave(user_file)
                nowlist = fixlist(raw_user)
                finalanswerlist[exam_chapter_idx] = nowlist
                print(f"DEBUG: Loaded user answers for ch {exam_chapter_idx} (k={k}): file={user_file} len={len(nowlist)}")
            except Exception as e:
                print(f"Error loading user answer {user_file}: {e}")
        elif k < len(answer_files):
            fallback_user_file = os.path.join(answers_dir, answer_files[k])
            try:
                raw_user = getanswerfromsave(fallback_user_file)
                nowlist = fixlist(raw_user)
                finalanswerlist[exam_chapter_idx] = nowlist
                print(f"DEBUG: Loaded fallback user answers for ch {exam_chapter_idx}: len={len(nowlist)}")
            except Exception as e:
                print(f"Error loading fallback user answer {fallback_user_file}: {e}")

        if true_file and os.path.exists(true_file):
            try:
                raw_true = getanswerfromsave(true_file)
                truelist = fixlist(raw_true)
                finaltruelist[exam_chapter_idx] = truelist
                print(f"DEBUG: Loaded true answers for ch {exam_chapter_idx}: len={len(truelist)}")
            except Exception as e:
                print(f"Error loading true answer {true_file}: {e}")
        else:
            print(f"DEBUG: True file missing for index {exam_chapter_idx}")

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
        self.formLayout = PySide6.QtWidgets.QFormLayout()
        # setLayoutDirection is not available on QFormLayout; set it on the widget that will host the layout instead
        # self.formLayout.setLayoutDirection(PySide6.QtCore.Qt.LayoutDirection.RightToLeft)
        self.formLayout.setLabelAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignRight)

        self.answerLayout = PySide6.QtWidgets.QFormLayout()
        # self.answerLayout.setLayoutDirection(PySide6.QtCore.Qt.LayoutDirection.RightToLeft)

        pic = PySide6.QtWidgets.QLabel()
        pic.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        pic.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Expanding)
        self.pic = pic

        scroll = PySide6.QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        # scroll.setFixedWidth(500)
        scroll.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollContent = PySide6.QtWidgets.QWidget()
        # set layout direction on the widget that hosts the form layout
        scrollContent.setLayoutDirection(PySide6.QtCore.Qt.LayoutDirection.RightToLeft)
        scrollContent.setLayout(self.formLayout)
        scroll.setWidget(scrollContent)

        # Create a scroll area for answers to ensure all are visible
        answerScroll = PySide6.QtWidgets.QScrollArea()
        answerScroll.setWidgetResizable(True)
        answerScroll.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        answerScrollContent = PySide6.QtWidgets.QWidget()
        # set layout direction on the widget that hosts the answer layout
        answerScrollContent.setLayoutDirection(PySide6.QtCore.Qt.LayoutDirection.RightToLeft)
        answerScrollContent.setLayout(self.answerLayout)
        answerScroll.setWidget(answerScrollContent)

        # Build layout: left=score panel, center=picture, right=answers
        dialogLayout.addWidget(scroll, 1)
        dialogLayout.addWidget(pic, 2)
        dialogLayout.addWidget(answerScroll, 1)

        self.Box1 = PySide6.QtWidgets.QLabel()
        self.Box2 = PySide6.QtWidgets.QLabel()
        self.Box3 = PySide6.QtWidgets.QLabel()
        self.Box4 = PySide6.QtWidgets.QLabel()
        self.Box5 = PySide6.QtWidgets.QLabel()
        self.Box6 = PySide6.QtWidgets.QLabel()

        # Save reference to saveslot
        self._saveslot = saveslot

        # Do initial render
        self.render()

        self.setLayout(dialogLayout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def render(self):
        # Rebuild both panels from disk
        save = self._saveslot
        alist, tlist = givechapters(save)

        # Clear existing
        self.clear_layout(self.formLayout)
        self.clear_layout(self.answerLayout)

        # Build score labels (Hebrew, values on left)
        label_hebrew = PySide6.QtWidgets.QLabel("ציון בעברית:")
        label_math = PySide6.QtWidgets.QLabel("ציון במתמטיקה:")
        label_english = PySide6.QtWidgets.QLabel("ציון באנגלית:")
        label_without_math = PySide6.QtWidgets.QLabel("ציון ללא מתמטיקה:")
        label_without_hebrew = PySide6.QtWidgets.QLabel("ציון ללא עברית:")
        label_general = PySide6.QtWidgets.QLabel("ציון כללי:")

        for lbl in (label_hebrew, label_math, label_english, label_without_math, label_without_hebrew, label_general):
            lbl.setFont(PySide6.QtGui.QFont("Aptos", font_size))

        # Add rows with (label, value) while layout direction is RTL so labels align right
        self.formLayout.addRow(label_hebrew, self.Box1)
        self.formLayout.addRow(label_math, self.Box2)
        self.formLayout.addRow(label_english, self.Box3)
        self.formLayout.addRow(label_without_math, self.Box4)
        self.formLayout.addRow(label_without_hebrew, self.Box5)
        self.formLayout.addRow(label_general, self.Box6)

        # Scores calculations
        mathrawscore = 0
        hebrawscore = 0
        engrawscore = 0

        for i in range(len(alist)):
            if not alist[i] and not tlist[i]:
                continue
            if "p" in tlist[i]:
                try:
                    tlist[i].remove("p")
                except ValueError:
                    pass
            if len(alist[i]) < len(tlist[i]):
                alist[i].extend([1] * (len(tlist[i]) - len(alist[i])))

            grade, wronguser, wrongcorrect = getchapterscore(alist[i], tlist[i])
            lenchapter = len(alist[i])
            if lenchapter == 20:
                mathrawscore += grade
            elif lenchapter == 22:
                engrawscore += grade
            elif lenchapter == 23:
                hebrawscore += grade

            long = PySide6.QtWidgets.QLabel("<div dir='rtl' style='text-align:right;'>" + " ".join(wrongcorrect) + "</div>")
            short = PySide6.QtWidgets.QLabel("<div dir='rtl' style='text-align:right;'>" + " ".join(wronguser) + "</div>")
            long.setTextFormat(PySide6.QtCore.Qt.TextFormat.RichText)
            short.setTextFormat(PySide6.QtCore.Qt.TextFormat.RichText)

            longbox = PySide6.QtWidgets.QLabel()
            shortbox = PySide6.QtWidgets.QLabel()
            difbox = PySide6.QtWidgets.QLabel()
            shortbox.setText(f"פרק {i+1} תשובות:")
            longbox.setText(f"פרק {i+1} תשובות נכונות:")
            difbox.setText(f"פרק {i+1} שגיאות: {str(lenchapter - grade)}")

            for lbl in (longbox, shortbox, difbox):
                lbl.setFont(PySide6.QtGui.QFont("Aptos", font_size))

            self.answerLayout.addRow(difbox, PySide6.QtWidgets.QLabel())
            self.answerLayout.addRow(short, shortbox)
            self.answerLayout.addRow(long, longbox)
            self.answerLayout.addRow(PySide6.QtWidgets.QLabel())
            self.answerLayout.addRow(PySide6.QtWidgets.QLabel())

        gradingkey = pickle.load(open(save + r"\Grade\gradingkey.txt", 'rb'))
        a, b, c = pdfbackend.give_final_scores([
            str(hebrawscore), str(mathrawscore), str(engrawscore)
        ], gradingkey)

        # Map totals correctly
        totalscore = a
        totalmathscore = b
        totalhebscore = c

        self.Box1.setText(str(hebrawscore))
        self.Box2.setText(str(mathrawscore))
        self.Box3.setText(str(engrawscore))
        self.Box4.setText(str(totalhebscore))
        self.Box5.setText(str(totalmathscore))
        self.Box6.setText(str(totalscore))

        savegrades([str(hebrawscore), str(mathrawscore), str(engrawscore), str(totalmathscore), str(totalhebscore), str(totalscore)])

        # Load and scale image for center column
        img_path = main.get_save_slot() + r"\images\answer.png"
        if os.path.exists(img_path):
            pix = PySide6.QtGui.QPixmap(img_path)
            target_h = int(self.screen().availableGeometry().height() * 0.9)
            target_w = int(self.screen().availableGeometry().width() * 0.45)
            scaled = pix.scaled(target_w, target_h, PySide6.QtCore.Qt.AspectRatioMode.KeepAspectRatio, PySide6.QtCore.Qt.TransformationMode.SmoothTransformation)
            self.pic.setPixmap(scaled)
        else:
            self.pic.setText("No answer image available")
        self.pic.setAlignment(PySide6.QtGui.Qt.AlignmentFlag.AlignCenter)
        self.setLayoutDirection(PySide6.QtCore.Qt.LayoutDirection.RightToLeft)

    def showEvent(self, event):
        # Refresh when the dialog is shown to reflect latest saved answers
        self.render()
        super().showEvent(event)

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
