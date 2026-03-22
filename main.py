"""Main application glue for the PDF viewer/exam app.

This module holds the main application functions and shared global
state. Only a small module docstring and cosmetic import grouping are
added to improve readability; no logic is changed.
"""

import os
import pickle
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtWidgets import QFormLayout, QComboBox

import end
import pdfbackend
import local_store # New import
from mainwindow import MainWindow
from typing import Any, List

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
dir = BASE_DIR

timelimit: str = "25:00"
counter: int = -1
limit: int = 5
backendfuncs = [pdfbackend.main, pdfbackend.main]
backendresumefuncs = [pdfbackend.main_resume, pdfbackend.main_resume]
backend = [backendfuncs, backendresumefuncs]
filenames: List[str] = []
answers: List[Any] = []
true_answers: List[Any] = []
examnames: Any = ""
boxofanswers: List[Any] = []
w: Any = None
filesavelist: List[str] = []
chapternames: List[Any] = []
trueanswerlist: List[Any] = []
shuffle: List[int] = [2, 0, 4, 1, 5, 3]
saveslot: str = "ada"


class TimeTracker:
    def __init__(self):
        self.current_question = -1
        self.start_time = None
        self.total_times = {} # question_index -> total_seconds

    def start_tracking(self, index):
        if self.current_question != -1:
            self.stop_tracking(self.current_question)
        self.current_question = index
        self.start_time = datetime.now()

    def stop_tracking(self, index):
        if self.current_question == index and self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.total_times[index] = self.total_times.get(index, 0) + elapsed
            self.start_time = None
            self.current_question = -1

    def get_avg_time(self):
        if not self.total_times:
            return 0
        return int(sum(self.total_times.values()) / len(self.total_times))

tracker = TimeTracker()

class TrackedComboBox(QComboBox):
    def __init__(self, index):
        super().__init__()
        self.index = index

    def focusInEvent(self, e):
        tracker.start_tracking(self.index)
        super().focusInEvent(e)

    def focusOutEvent(self, e):
        tracker.stop_tracking(self.index)
        super().focusOutEvent(e)


def update_save_slot(value: str) -> None:
    global saveslot
    saveslot = os.path.join(BASE_DIR, "Saves", value)


def get_save_slot() -> str:
    global saveslot
    return saveslot


def get_shuffle() -> List[int]:
    global shuffle
    return shuffle


def finish_chapter() -> None:
    global w, boxofanswers, counter, filesavelist, examnames, shuffle, saveslot

    # Calculate score for this chapter (simple version, assuming single correct answer)
    # We need the true answers to calculate score now, but main_app logic uses pdfbackend helper later?
    # Actually finish_chapter saves answers to a file. It doesn't grade yet. Grading happens at the end.
    # However, Requirement Phase 3 says: "Save this data into the local SQLite database when the user saves or finishes the exam"
    # To save per-chapter stats now, I need the true answers for this chapter.

    # Extract current answers
    current_answers = [boxofanswers[i].currentText() for i in range(len(boxofanswers))]

    # Save standard file based resume info
    filesavelist.append(pdfbackend.save_answers(current_answers, counter))

    # NEW: Save to SQLite
    try:
        # We need the exam ID and chapter name.
        # examnames is a list of file paths. examnames[shuffle[counter]] is current file path.
        current_exam_path = examnames[shuffle[counter]]
        chapter_name = os.path.basename(current_exam_path)

        # Calculate approximate score for this chapter immediately for analytics
        # Note: We need true_answers for this specific chapter.
        # true_answers is a list of lists. true_answers[shuffle[counter]] is for this chapter.
        current_true_answers = true_answers[shuffle[counter]]

        correct_count = 0
        total_questions = len(current_true_answers)
        # Adjust for 'p' if present in true_answers? Logic in pdfbackend.create_answer_widget suggests 'p' handling.
        # Let's align with boxofanswers length.

        # Fix: boxofanswers might be shorter if 'p' is involved.
        for i in range(min(len(current_answers), len(current_true_answers))):
            # pdfbackend uses '1', '2', '3', '4'.
             if current_answers[i] == str(current_true_answers[i]):
                 correct_count += 1

        score_pct = int((correct_count / len(current_answers)) * 100) if len(current_answers) > 0 else 0

        # We need a proper exam_id. Currently we don't have one passed from start.py easily.
        # We can use a hash of the directory path or just 0 for now if unknown.
        # Or better, try to find it in downloaded_exams via path.
        # For this refactor, let's use a placeholder or try to look it up.
        exam_id = 0

        # Get user from local_store if logged in?
        # We can default to a "guest" or the last logged in user.
        # For now, let's assume 'default' or grab from local_store generic getter if we had one.
        username = "offline_user"

        local_store.save_analytics(
            username=username,
            exam_id=exam_id,
            chapter_name=chapter_name,
            score=score_pct,
            time_per_question_avg=tracker.get_avg_time()
        )

        # Also save progress state
        import json
        local_store.save_exam_progress(
            username=username,
            exam_id=exam_id,
            current_chapter=counter,
            answers_json=json.dumps(current_answers),
            time_elapsed=int(sum(tracker.total_times.values()))
        )

    except Exception as e:
        print(f"Failed to save analytics: {e}")

    tracker.total_times = {} # Reset for next chapter

    if hasattr(w, "close"):
        w.close()


def jump_next_chapter() -> None:
    global filenames, counter, answers, typeexam
    finish_chapter()
    mainapp("asda", timelimit)


def get_time_limit() -> str:
    global timelimit
    return timelimit


def create_answer_widget(answers):
    minus = 1 if "p" in answers else 0
    layout = QFormLayout()
    # Use TrackedComboBox instead of QComboBox
    boxesofanswer = [TrackedComboBox(i) for i in range(len(answers) - minus)]
    for index, box in enumerate(boxesofanswer):
        box.addItems(["1", "2", "3", "4"])
        layout.addRow(str(index + 1), box)
    return layout, boxesofanswer


def main_app(exam, timer, *args):
    global timelimit, counter, answers, examnames, w, boxofanswers, chapternames, trueanswerlist, typeexam, shuffle, limit, backend, limit, true_answers
    typeexam = 1
    if counter == limit:
        finish_chapter()
        w = end.Window(get_save_slot())
        w.showMaximized()
    else:
        timelimit = timer
        argument_parser = ArgumentParser(
            description="PDF Viewer", formatter_class=RawTextHelpFormatter
        )
        argument_parser.add_argument(
            "file", help="The file to open", nargs="?", type=str
        )
        w = MainWindow()
        w.showMaximized()
        if counter == -1:
            if args[0][2] == 0:
                limit = 5
            else:
                limit = 7
            if (args[0][1] == 0):
                update_save_slot(args[0][0])
                examnames, answers, trueanswerlist, true_answers = backend[args[0][1]][args[0][2]](
                    exam, get_save_slot()
                )
                if (args[0][2] == 0):
                    order_file = os.path.join(get_save_slot(), "Grade", "Order.txt")
                    with open(order_file, "wb") as f:
                        pickle.dump([2, 0, 4, 1, 5, 3], f)
                        shuffle = [2, 0, 4, 1, 5, 3]
                else:
                    order_file = os.path.join(get_save_slot(), "Grade", "Order.txt")
                    with open(order_file, "wb") as f:
                        pickle.dump([0, 1, 2, 3, 4, 5, 6, 7], f)
                        shuffle = [0, 1, 2, 3, 4, 5, 6, 7]
            elif (args[0][1] == 1):
                update_save_slot(args[0][0])
                examnames, answers, true_answers, counter = backend[args[0][1]][args[0][2]](
                    get_save_slot()
                )
                if (counter == limit):
                    w = end.Window(get_save_slot())
                    w.showMaximized()
                if args[0][2] == 1:
                    shuffle = [0, 1, 2, 3, 4, 5, 6, 7]
                else:
                    shuffle = [2, 0, 4, 1, 5, 3]
    if counter < limit:
        counter += 1
        layout, boxofanswers = create_answer_widget(true_answers[shuffle[counter]])
        w.open(QUrl.fromLocalFile(examnames[shuffle[counter]]))
        w.addanswers(layout)

    QCoreApplication.exec()


mainapp = main_app
