from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                               QMessageBox, QListWidget, QHBoxLayout, QProgressBar)
from PySide6.QtCore import Qt
import network_manager
import local_store
import os

class ExamManager(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Exam Manager")
        self.resize(600, 400)
        self.token = token
        self.exams = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.lbl_title = QLabel("Available Exams")
        self.layout.addWidget(self.lbl_title)

        self.list_exams = QListWidget()
        self.layout.addWidget(self.list_exams)

        self.btn_refresh = QPushButton("Refresh List")
        self.btn_refresh.clicked.connect(self.refresh_exams)
        self.layout.addWidget(self.btn_refresh)

        self.layout_download = QHBoxLayout()
        self.lbl_pass = QLabel("Password:")
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_download = QPushButton("Download Selected")
        self.btn_download.clicked.connect(self.download_exam)

        self.layout_download.addWidget(self.lbl_pass)
        self.layout_download.addWidget(self.txt_pass)
        self.layout_download.addWidget(self.btn_download)
        self.layout.addLayout(self.layout_download)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress)

        self.refresh_exams()

    def refresh_exams(self):
        self.list_exams.clear()
        self.exams = network_manager.get_available_exams(self.token)
        downloaded = [e['exam_id'] for e in local_store.get_downloaded_exams()]

        for exam in self.exams:
            status = "[Downloaded]" if exam['id'] in downloaded else ""
            self.list_exams.addItem(f"{exam['title']} (ver: {exam['version']}) {status}")

    def download_exam(self):
        row = self.list_exams.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select an exam to download.")
            return

        exam = self.exams[row]
        password = self.txt_pass.text()

        if not password:
             QMessageBox.warning(self, "Error", "Please enter the password.")
             return

        self.progress.setVisible(True)
        self.progress.setRange(0, 0) # Indeterminate
        QCoreApplication.processEvents() # Force update

        # Pass the whole exam dict to network_manager
        path = network_manager.download_exam(exam, password, self.token)

        self.progress.setRange(0, 100)
        self.progress.setVisible(False)

        if path:
            QMessageBox.information(self, "Success", f"Exam downloaded to {path}")
            self.refresh_exams()
            # Also register with local DB if not already done in network_manager
        else:
             QMessageBox.critical(self, "Error", "Download failed. Check password or connection.")

from PySide6.QtCore import QCoreApplication
