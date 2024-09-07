# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import os
import pickle
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtWidgets import QFormLayout, QComboBox

import end
import pdfbackend
from mainwindow import MainWindow

dir=os.path.realpath(__file__).replace("\main.py", "")

timelimit = "25:00"
counter = -1
limit=5
backendfuncs=[pdfbackend.main,pdfbackend.main]
backendresumefuncs=[pdfbackend.mainresume,pdfbackend.mainresume]
backend=[backendfuncs,backendresumefuncs]
filenames = []
answers = []
true_answers=[]
examnames = ""
boxofanswers = []
w = ""
filesavelist = []
chapternames = []
trueanswerlist = []
shuffle = [2, 0, 4, 1, 5, 3]
saveslot = "ada"


def updatesaveslot(value):
    global saveslot
    saveslot = dir+"\\Saves\\"+value


def getsaveslot():
    global saveslot
    return saveslot


def getshuffle():
    global shuffle
    return shuffle


def finishchapter():
    pass
    global w, boxofanswers, counter, filesavelist
    savelist = [boxofanswers[i].currentText() for i in range(len(boxofanswers))]
    filesavelist.append(pdfbackend.saveanswers(savelist, counter))
    w.close()
    # close chapter


def jumpnextchapter():
    global filenames, counter, answers, typeexam
    finishchapter()
    mainapp("asda", timelimit)

    # answer=answers[counter]
    # examname=filenames[counter]


def givetimelimit():
    global timelimit
    return timelimit


def createanswerwidget(answers):
    if "p" in answers:
        minus = 1
    else:
        minus = 0
    layout = QFormLayout()
    boxesofanswer = [0 for i in range(len(answers) - minus)]
    for index in range(len(answers) - minus):
        boxesofanswer[index] = QComboBox()
        boxesofanswer[index].addItems(["1", "2", "3", "4"])
        layout.addRow(str(index + 1), boxesofanswer[index])
    return layout, boxesofanswer


def mainapp(exam, timer, *args):
    global timelimit, counter, answers, examnames, w, boxofanswers, chapternames, trueanswerlist, typeexam, shuffle,limit,backend,limit,true_answers
    typeexam = 1
    if counter == limit:
        finishchapter()
        w = end.Window(getsaveslot())
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
        ###end()
        if counter == -1:
            if args[0][2]==0:
                limit=5
            else:
                 limit=7
            if(args[0][1]==0):
                updatesaveslot(args[0][0])
                examnames, answers, trueanswerlist,true_answers = backend[args[0][1]][args[0][2]](
                    exam, getsaveslot()
                )
                if(args[0][2]==0):
                    with open(getsaveslot() + "\Grade\Order.txt", "wb") as f:
                        pickle.dump([2, 0, 4, 1, 5, 3], f)
                        shuffle=[2, 0, 4, 1, 5, 3]
                else:
                    with open(getsaveslot() + "\Grade\Order.txt", "wb") as f:
                        pickle.dump([0,1,2,3,4,5,6,7], f)
                        shuffle=[0,1,2,3,4,5,6,7]
            elif (args[0][1] == 1):
                updatesaveslot(args[0][0])
                examnames, answers, true_answers,counter = backend[args[0][1]][args[0][2]](
                    getsaveslot()
                )
                if (counter == limit):
                    w = end.Window(getsaveslot())
                    w.showMaximized()
                if args[0][2] == 1:
                    shuffle = [0, 1, 2, 3, 4, 5, 6, 7]
                else:
                    shuffle = [2, 0, 4, 1, 5, 3]
    if(counter<limit):
        counter += 1
        layout, boxofanswers = createanswerwidget(true_answers[shuffle[counter]])
        w.open(QUrl.fromLocalFile(examnames[shuffle[counter]]))
        w.addanswers(layout)

    QCoreApplication.exec()




### bug happen because of existing not saving