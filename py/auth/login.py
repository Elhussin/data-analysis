from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt
from py.functian import load_stylesheet, clear_credentials_qsettings, save_credentials_qsettings, check_saved_credentials, save_credentials_user_id
from dataBase.database import UserDatabase
from py.layOut.icon import IconManager ,set_default_title
from PyQt5.QtGui import QIcon

import os
import sys
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # استخدام هذه الطريقة للوصول إلى ملفات QSS والصور
        qss_path = self.resource_path("py/static/style/auth.qss")
        icon_path = self.resource_path("py/static/media/icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("LOG IN")
        self.setWindowFlags(Qt.Window)
        load_stylesheet(self, qss_path)


        # Initialize the database connection
        self.db = UserDatabase()

        # Set default window size for the login dialog
        self.resize(400, 300)

        # Setup UI elements
        self.init_ui()

        # Check if credentials are saved after UI setup Add user login datiles to form 
        check_saved_credentials(self)

    def init_ui(self):
        """ Initialize the UI elements for the login dialog """
        layout = QVBoxLayout()

        # Add title label
        self.label = QLabel("Login")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Add username input field
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")

        # Add password input field with hidden characters
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        # Add "Remember me" checkbox
        self.remember_me_checkbox = QCheckBox("Remember me", self)
        layout.addWidget(self.remember_me_checkbox)

        # Add login button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)

        # Add register button
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_register_dialog)

        # Add buttons to the layout
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        """ Handle login logic when the login button is clicked """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in both fields")
            return

        # Check user credentials in the database
        get_user = self.db.check_user(username, password)

        if get_user:

            # Check if the user is active
            if get_user['status'] == 0:
                QMessageBox.warning(self, "Error", "Invalid username - not active")
                return

            # Save user ID for session management
            self.user_id = get_user['id']
            save_credentials_user_id(self.user_id)

            # Save credentials if "Remember me" is checked
            if self.remember_me_checkbox.isChecked():
                save_credentials_qsettings(username, password)
            else:
                clear_credentials_qsettings()

            # Create a new user session
            self.db.create_user_session(self.user_id)

            # Retrieve the active session for the user
            active_session = self.db.get_active_session(self.user_id)
            if active_session:
                session_id, login_time = active_session
                print(f"Session ID: {session_id}, Login Time: {login_time}")

            QMessageBox.information(self, "Login Successful", "Welcome back!")
            self.accept()  # Close the login dialog on successful login

        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def open_register_dialog(self):
        """ Open the registration dialog """
        # Close the current login dialog before opening the registration dialog
        self.close()

        # Import registration dialog dynamically
        from py.auth.register import RegisterDialog

        register_dialog = RegisterDialog(self)
        if register_dialog.exec_() == QDialog.Accepted:
            self.accept()  # Close the login dialog on successful registration

    def resource_path(self,relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def closeEvent(self, event):
        """ Handle cleanup when the dialog is closed """
        # Save credentials if "Remember me" is checked
        if self.remember_me_checkbox.isChecked():
            save_credentials_qsettings(self.username_input.text(), self.password_input.text())
        else:
            clear_credentials_qsettings()

        # Close database connection
        self.db.close()
