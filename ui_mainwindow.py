# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QMenu,
    QMenuBar,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
)
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QListWidget,
    QGridLayout,
    QLabel,
    QProgressBar,
)

import main

starttime = ""
start = ""


class WinForm(QWidget):
    def __init__(self, timelimit, parent=None):
        global starttime, start
        super(WinForm, self).__init__(parent)
        self.listFile = QListWidget()
        self.label = QLabel("Label")
        self.startBtn = QPushButton("Pause")
        self.endBtn = QPushButton("Finish")
        layout = QGridLayout()
        self.timer = QTimer()
        self.timer.start(1000 * 60 * int(timelimit[0:-3]) + 5000)
        self.savedtime = self.timer.remainingTime()
        # self.timer.timeout.connect(s)
        self.refresh = QTimer()
        self.refresh.start(1000)
        self.refresh.timeout.connect(self.refreshr)
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.startBtn, 0, 3)
        layout.addWidget(self.endBtn, 0, 4)
        self.startBtn.clicked.connect(self.pauseunpause)
        self.endBtn.clicked.connect(self.endchapter)

        self.setLayout(layout)

    def refreshr(self):
        if self.timer.isActive():
            self.label.setText(
                str(self.timer.remainingTime() / 60000)[0:2]
                + ":"
                + str((self.timer.remainingTime() % 60000) / 1000)[0:2]
            )
            self.savedtime = self.timer.remainingTime()
        else:
            pass

    def pauseunpause(self):
        if self.timer.isActive():
            self.label.setText(
                str(self.timer.remainingTime() / 60000)[0:2]
                + ":"
                + str((self.timer.remainingTime() % 60000) / 1000)[0:2]
            )
            self.timer.stop()
            self.startBtn.setText("Unpause")
        else:
            self.timer = QTimer()
            self.timer.start(self.savedtime)
            self.savedtime = self.timer.remainingTime()
            self.startBtn.setText("Pause")

    def endchapter(self):
        main.jumpnextchapter()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        icon = QIcon()
        iconThemeName = "document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(
                ":/icons/images/document-open.svgz", QSize(), QIcon.Normal, QIcon.Off
            )
        self.actionOpen.setIcon(icon)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        icon1 = QIcon(QIcon.fromTheme("application-exit"))
        self.actionQuit.setIcon(icon1)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon2 = QIcon(QIcon.fromTheme("help-about"))
        self.actionAbout.setIcon(icon2)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionZoom_In = QAction(MainWindow)
        self.actionZoom_In.setObjectName("actionZoom_In")
        icon3 = QIcon()
        iconThemeName = "zoom-in"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(
                ":/icons/images/zoom-in.svgz", QSize(), QIcon.Normal, QIcon.Off
            )

        self.actionZoom_In.setIcon(icon3)
        self.actionZoom_Out = QAction(MainWindow)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        icon4 = QIcon()
        iconThemeName = "zoom-out"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(
                ":/icons/images/zoom-out.svgz", QSize(), QIcon.Normal, QIcon.Off
            )

        self.actionZoom_Out.setIcon(icon4)
        self.actionPrevious_Page = QAction(MainWindow)
        self.actionPrevious_Page.setObjectName("actionPrevious_Page")
        icon5 = QIcon()
        iconThemeName = "go-previous-view-page"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(
                ":/icons/images/go-previous-view-page.svgz",
                QSize(),
                QIcon.Normal,
                QIcon.Off,
            )

        self.actionPrevious_Page.setIcon(icon5)
        self.actionNext_Page = QAction(MainWindow)
        self.actionNext_Page.setObjectName("actionNext_Page")
        icon6 = QIcon()
        iconThemeName = "go-next-view-page"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(
                ":/icons/images/go-next-view-page.svgz",
                QSize(),
                QIcon.Normal,
                QIcon.Off,
            )

        self.actionNext_Page.setIcon(icon6)
        self.actionContinuous = QAction(MainWindow)
        self.actionContinuous.setObjectName("actionContinuous")
        self.actionContinuous.setCheckable(True)
        self.actionBack = QAction(MainWindow)
        self.actionBack.setObjectName("actionBack")
        self.actionBack.setEnabled(False)
        icon7 = QIcon()
        icon7.addFile(
            ":/icons/images/go-previous-view.svgz", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionBack.setIcon(icon7)
        self.actionForward = QAction(MainWindow)
        self.actionForward.setObjectName("actionForward")
        self.actionForward.setEnabled(False)
        icon8 = QIcon()
        icon8.addFile(
            ":/icons/images/go-next-view.svgz", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionForward.setIcon(icon8)
        self.progressbar = QProgressBar()
        self.progressbar.setObjectName("progressBar")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.widget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(0)
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.setDocumentMode(False)
        self.bookmarkTab = QWidget()
        self.bookmarkTab.setObjectName("answers")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        # self.bookmarkView = QTreeView(self.bookmarkTab)
        # self.bookmarkView.setObjectName(u"bookmarkView")
        # sizePolicy.setHeightForWidth(self.bookmarkView.sizePolicy().hasHeightForWidth())
        # self.bookmarkView.setSizePolicy(sizePolicy)
        # self.bookmarkView.setHeaderHidden(True)

        # self.verticalLayout_3.addWidget(self.bookmarkView)

        # self.tabWidget.addTab(self.bookmarkTab, "")
        self.pagesTab = QWidget()
        self.pagesTab.setObjectName("pagesTab")
        # self.tabWidget.addTab(self.pagesTab, "")
        # self.splitter.addWidget(self.tabWidget)
        self.pdfView = QPdfView(self.splitter)
        self.pdfView.setObjectName("pdfView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(10)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pdfView.sizePolicy().hasHeightForWidth())
        self.pdfView.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.pdfView)

        self.verticalLayout_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 700, 23))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuView.addAction(self.actionPrevious_Page)
        self.menuView.addAction(self.actionNext_Page)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionContinuous)
        # self.mainToolBar.addAction(self.actionOpen)
        # self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionZoom_Out)
        self.mainToolBar.addAction(self.actionZoom_In)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionBack)
        self.mainToolBar.addAction(self.actionForward)
        global timelimit
        self.mainToolBar.addWidget(WinForm(timelimit=main.givetimelimit()))

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "PDF Viewer", None)
        )
        # self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        # if QT_CONFIG(shortcut)
        # self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        # endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        # if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Q", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionAbout_Qt.setText(
            QCoreApplication.translate("MainWindow", "About Qt", None)
        )
        self.actionZoom_In.setText(
            QCoreApplication.translate("MainWindow", "Zoom In", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionZoom_In.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl++", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionZoom_Out.setText(
            QCoreApplication.translate("MainWindow", "Zoom Out", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionZoom_Out.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+-", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionPrevious_Page.setText(
            QCoreApplication.translate("MainWindow", "Previous Page", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionPrevious_Page.setShortcut(
            QCoreApplication.translate("MainWindow", "PgUp", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionNext_Page.setText(
            QCoreApplication.translate("MainWindow", "Next Page", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionNext_Page.setShortcut(
            QCoreApplication.translate("MainWindow", "PgDown", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionContinuous.setText(
            QCoreApplication.translate("MainWindow", "Continuous", None)
        )
        self.actionBack.setText(QCoreApplication.translate("MainWindow", "Back", None))
        # if QT_CONFIG(tooltip)
        self.actionBack.setToolTip(
            QCoreApplication.translate("MainWindow", "back to previous view", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionForward.setText(
            QCoreApplication.translate("MainWindow", "Forward", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionForward.setToolTip(
            QCoreApplication.translate("MainWindow", "forward to next view", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.bookmarkTab),
            QCoreApplication.translate("MainWindow", "answers", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.pagesTab),
            QCoreApplication.translate("MainWindow", "Pages", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", "View", None))

    # retranslateUi
