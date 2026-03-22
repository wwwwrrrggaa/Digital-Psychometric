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
        self.resize(400, 350)
        self.token = None
        self.username = None

        # Simplified stylesheet as it's now handled by the app-level dark theme
        self.setStyleSheet("""
            QPushButton#offlineBtn {
                background-color: #6c757d;
            }
            QPushButton#offlineBtn:hover {
                background-color: #5a6268;
            }
            QPushButton#updateBtn {
                background-color: #28a745;
                padding: 5px 10px;
            }
            QPushButton#updateBtn:hover {
                background-color: #218838;
            }
            QLabel#status {
                color: #d9534f;
                font-size: 12px;
                margin-top: 10px;
            }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header
        header = QLabel("Sign In")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #007bff;")
        layout.addWidget(header)

        # Form
        layout.addWidget(QLabel("Username"))
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Enter username")
        layout.addWidget(self.txt_user)

        layout.addWidget(QLabel("Password"))
        self.txt_pass = QLineEdit()
        # self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password) # Passwords are NOT hidden now
        self.txt_pass.setPlaceholderText("Enter password")
        layout.addWidget(self.txt_pass)

        layout.addSpacing(20)

        # Actions
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.do_login)
        btn_layout.addWidget(self.btn_login)

        self.btn_offline = QPushButton("Offline Mode")
        self.btn_offline.setObjectName("offlineBtn")
        self.btn_offline.clicked.connect(self.do_offline)
        btn_layout.addWidget(self.btn_offline)

        layout.addLayout(btn_layout)

        layout.addSpacing(10)

        # API URL Configuration
        config_frame = QFrame()
        config_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 5px; padding: 5px; border: 1px solid #ccc;")
        config_layout = QHBoxLayout(config_frame)
        config_layout.setContentsMargins(5, 5, 5, 5)

        url_label = QLabel("Server:")
        url_label.setStyleSheet("font-size: 12px; color: #555;")
        config_layout.addWidget(url_label)

        self.txt_api = QLineEdit(network_manager.get_api_url())
        self.txt_api.setStyleSheet("font-size: 12px; padding: 4px; background-color: #fff; border: 1px solid #ccc;")
        config_layout.addWidget(self.txt_api)

        btn_save_api = QPushButton("Set")
        btn_save_api.setObjectName("updateBtn")
        btn_save_api.clicked.connect(self.update_api)
        config_layout.addWidget(btn_save_api)

        layout.addWidget(config_frame)

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("status")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

    def update_api(self):
        new_url = self.txt_api.text().strip()
        if new_url:
            network_manager.save_api_url(new_url)
            self.lbl_status.setStyleSheet("color: #28a745; font-size: 12px; margin-top: 10px;")
            self.lbl_status.setText(f"API URL updated to {new_url}")

    def do_login(self):
        user = self.txt_user.text()
        pwd = self.txt_pass.text()

        if not user or not pwd:
            self.lbl_status.setStyleSheet("color: #d9534f; font-size: 12px; margin-top: 10px;")
            self.lbl_status.setText("Please enter username and password")
            return

        self.lbl_status.setStyleSheet("color: #d39e00; font-size: 12px; margin-top: 10px;") # Warning yellow/gold
        self.lbl_status.setText("Connecting...")
        QCoreApplication.processEvents()

        # Try online login - Now returns (token, error_message)
        token, error_msg = network_manager.login(user, pwd)

        if token:
            self.token = token
            self.username = user
            self.lbl_status.setStyleSheet("color: #28a745;")
            self.lbl_status.setText("Login Successful! Syncing...")
            QCoreApplication.processEvents()

            # Sync analytics
            synced_count = network_manager.sync_analytics(token, user)
            if synced_count > 0:
                 self.lbl_status.setText(f"Login Successful! Synced {synced_count} records.")

            self.login_successful.emit(user)
            self.accept()
        else:
            # Login failed. Check offline or show error.
            # Differentiate between "Connection Error" and "Invalid Credentials"

            # If server is unreachable, try offline login
            if "Connection" in error_msg:
                self.lbl_status.setText(f"{error_msg}. Trying offline...")
                QCoreApplication.processEvents()

                local_user = local_store.login_offline(user, pwd)
                if local_user:
                     self.username = user
                     self.lbl_status.setStyleSheet("color: #17a2b8;") # Blue for offline
                     self.lbl_status.setText("Logged in OFFLINE.")
                     local_store.save_local_user(user, pwd) # Refresh last login
                     self.login_successful.emit(user)
                     self.accept()
                else:
                     self.lbl_status.setStyleSheet("color: #d9534f;")
                     self.lbl_status.setText("Offline login failed. No cached credentials.")
            else:
                 # Likely invalid credentials or server error
                 self.lbl_status.setStyleSheet("color: #d9534f;")
                 self.lbl_status.setText(error_msg)

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
