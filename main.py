"""Main application glue for the PDF viewer/exam app.

This module holds the main application functions and shared global
state. Only a small module docstring and cosmetic import grouping are
added to improve readability; no logic is changed.
"""

import os
import pickle
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtWidgets import QFormLayout, QComboBox

import end
import pdfbackend
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
    global w, boxofanswers, counter, filesavelist
    savelist = [boxofanswers[i].currentText() for i in range(len(boxofanswers))]
    filesavelist.append(pdfbackend.save_answers(savelist, counter))
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
    boxesofanswer = [QComboBox() for _ in range(len(answers) - minus)]
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
