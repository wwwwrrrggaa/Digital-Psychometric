from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                               QMessageBox, QHBoxLayout, QWidget, QFrame, QSizePolicy) # Added QWidget and others
from PySide6.QtCore import Qt, Signal
import network_manager
import local_store

class LoginWindow(QDialog):
    login_successful = Signal(str) # Emits username on success

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Psychometric - Login")
        self.resize(400, 300)
        self.token = None
        self.username = None

        # Stylesheet similar to main app (Aptos font, clean look)
        self.setStyleSheet("""
            QDialog { background-color: #f0f0f0; }
            QLabel { font-family: 'Aptos'; font-size: 14px; }
            QLineEdit { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
            QPushButton { 
                background-color: #007bff; color: white; padding: 10px; 
                border-radius: 4px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header
        header = QLabel("Login to Access Your Exams")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)

        # Form
        layout.addWidget(QLabel("Username:"))
        self.txt_user = QLineEdit()
        layout.addWidget(self.txt_user)

        layout.addWidget(QLabel("Password:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.txt_pass)

        # Actions
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.do_login)
        btn_layout.addWidget(self.btn_login)

        self.btn_offline = QPushButton("Offline Mode")
        self.btn_offline.setStyleSheet("background-color: #6c757d;")
        self.btn_offline.clicked.connect(self.do_offline)
        btn_layout.addWidget(self.btn_offline)

        layout.addLayout(btn_layout)

        # API URL Configuration
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Server URL:"))
        self.txt_api = QLineEdit(network_manager.get_api_url())
        config_layout.addWidget(self.txt_api)
        btn_save_api = QPushButton("Update")
        btn_save_api.clicked.connect(self.update_api)
        config_layout.addWidget(btn_save_api)
        layout.addLayout(config_layout)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_status)

    def update_api(self):
        new_url = self.txt_api.text().strip()
        if new_url:
            network_manager.save_api_url(new_url)
            self.lbl_status.setText(f"API URL updated to {new_url}")

    def do_login(self):
        user = self.txt_user.text()
        pwd = self.txt_pass.text()

        if not user or not pwd:
            self.lbl_status.setText("Please enter username and password")
            return

        self.lbl_status.setText("Connecting...")
        QCoreApplication.processEvents()

        # Try online login
        token = network_manager.login(user, pwd)

        if token:
            self.token = token
            self.username = user
            self.lbl_status.setText("Login Successful! Syncing...")
            QCoreApplication.processEvents()

            # Sync analytics
            synced_count = network_manager.sync_analytics(token, user)
            if synced_count > 0:
                 self.lbl_status.setText(f"Login Successful! Synced {synced_count} records.")

            self.login_successful.emit(user)
            self.accept()
        else:
            # Fallback to offline check
            local_user = local_store.login_offline(user, pwd)
            if local_user:
                 self.username = user
                 self.lbl_status.setText("Server unreachable. Logged in OFFLINE.")
                 local_store.save_local_user(user, pwd) # Refresh last login
                 self.login_successful.emit(user)
                 self.accept()
            else:
                 self.lbl_status.setText("Login failed. Check internet or credentials.")

    def do_offline(self):
        # Guest mode or just proceed?
        # Requirement says "Offline-First". Usually implies cached credentials.
        # If they click Offline Mode explicitely without credentials, maybe just browse local files?
        self.username = "guest"
        self.login_successful.emit("guest")
        self.reject() # Start anyway, but maybe signal differently?
        # Actually reject closes the dialog with Rejected code.
        # We want to proceed.
        self.accept()

from PySide6.QtCore import QCoreApplication

