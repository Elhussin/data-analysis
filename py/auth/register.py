from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from dataBase.database import UserDatabase
from py.auth.login import LoginDialog

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize the database connection
        self.db = UserDatabase()

        # Set default window size for the registration dialog
        self.resize(400, 300)
        self.setWindowFlags(Qt.Window)
        
        # Setup UI elements
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI elements for the registration dialog """
        layout = QVBoxLayout()

        # Add title label
        self.label = QLabel("Register")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Add input fields for registration
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your full name")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask the password
        self.password_input.setPlaceholderText("Enter your password")

        layout.addWidget(self.name_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)

        # Add register button
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.handle_register)

        # Add back to login button
        self.back_button = QPushButton("Back to Login", self)
        self.back_button.clicked.connect(self.go_back_to_login)

        # Add buttons to the layout
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def handle_register(self):
        """ Handle the registration logic """
        full_name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Check if all fields are filled
        if not full_name or not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        # Check if the username already exists in the database
        if self.db.check_user(username, password):
            QMessageBox.warning(self, "Error", "Username already exists")
            return

        # Add the new user to the database
        if self.db.add_user(username, password, full_name, email):
            QMessageBox.information(self, "Registration Successful", "User registered successfully!")
            self.go_back_to_login()
            self.accept()  # Close the registration dialog on success

        else:
            QMessageBox.warning(self, "Error", "Registration failed, please try again.")

    def closeEvent(self, event):
        """ Close the database connection when the dialog is closed """
        self.db.close()

    def go_back_to_login(self):
        """ Return to the login dialog and close the registration dialog """
        self.close()
        login_dialog = LoginDialog(self)
        login_dialog.exec_()
