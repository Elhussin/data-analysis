from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QDialog, QMessageBox
from dataBase.database import UserDatabase
from dataBase.encrypet import EncryptionManager
from py.form import DynamicForm,DynamicTableButtons
from py.data import userFormFields

class UserMange(QWidget):
    """ 
    Main widget for managing user data. Allows adding, deleting, and editing user records.
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.db = UserDatabase()  # Initialize database connection
        self.creatTableOrbuttons=DynamicTableButtons()
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface components: buttons, table, and layout.
        """
        buttons = [
            {"text": "Add User", "callback": lambda: self.open_add_user_dialog(userFormFields)},
            {"text": "Delete User", "callback": self.delete_user},
            {"text": "Edit User", "callback": lambda: self.open_edit_user_dialog(userFormFields)},
        ]

        self.layout = QVBoxLayout()

        # Create buttons and add them to the layout
        button_layout = self.creatTableOrbuttons.creat_button(buttons)
        self.layout.addLayout(button_layout)

        # Create table to display users
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.load_users_table()  # Load users into the table

    def load_users_table(self):
        """
        Load all users from the database and display them in the table.
        Excludes sensitive information like passwords.
        """
        try:
            users = self.db.get_all_users()  # Fetch all users from the database
            if not users:
                QMessageBox.information(self, "No Data", "No users found in the database.")
                return

            exclude_columns = ["password"]  # Exclude sensitive data like passwords
            self.creatTableOrbuttons.populate_table(self.table, users, exclude_columns)

        except Exception as e:
            # Handle potential errors, like database connection issues
            QMessageBox.critical(self, "Error", f"An error occurred while loading users: {str(e)}")

    def open_add_user_dialog(self, fields):
        """
        Open the Add User dialog window and add a user after validation.
        """
        dialog = DynamicForm(fields, lambda data: self.add_user(data, dialog), button_text="Add User")

        # Open Window
        if dialog.exec_() == QDialog.Accepted:
            # Validate fields before accepting the dialog
                self.load_users_table()  # Refresh the table after adding a new user

    def add_user(self, data, window):
        """
        Add a new user to the database.
        """
        try:
            # Extract user data from the input dictionary
            username = data.get('username', '').strip()
            full_name = data.get('full_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            status = data.get("status", {}).get("data", 0)
            user_type = data.get("user_type", {}).get("text", None)

            # Validate required fields
            if not (username and password and email):
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return

            # Check if the username already exists
            if self.db.check_user(username, password):
                QMessageBox.warning(self, "Error", "Username already exists.")
                return

            # Add user to the database
            is_added = self.db.add_user_by_admin(
                username,full_name,email,
                status,user_type,password,
            )

            if is_added:
                self.load_users_table()  # Reload the table after adding the user
                QMessageBox.information(self, "Success", "User registered successfully!")
                window.close()
            else:
                QMessageBox.critical(self, "Error", "Registration failed. Please try again.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def open_edit_user_dialog(self,fields):
        """
        Open the Edit User dialog window to modify the selected user's details.
        """
        try:
            # Get the selected row
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Error", "Please select a user to update.")
                return

            # Fetch user ID and details
            self.user_id = int(self.table.item(selected_row, 0).text())
            self.user = self.db.get_user_by_id(self.user_id)


            if not self.user:
                QMessageBox.warning(self, "Error", "User not found!")
                return
            
            if self.user['status']==1:
                self.user['status']="Active"
            else:
                self.user['status']="Inactive"
            # Decrypt the password for editing
            decrypt = EncryptionManager()
            try:
                self.user['password'] = decrypt.decrypt_password(self.user["password"])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to decrypt password: {str(e)}")
                return

            # Open the dynamic form for editing user details
            dialog = DynamicForm(
                fields,
                lambda data: self.update_user(data, dialog),
                self.user,
                button_text="Update User"
            )

            # Execute the dialog and refresh the table if the user clicks "Update"
            if dialog.exec_() == QDialog.Accepted:
                self.load_users_table()

        except Exception as e:
            # Handle unexpected errors
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def update_user(self, data, window):
        """
        Update the user data after editing.

        Args:
            data (dict): A dictionary containing the updated user data.
            window (QWidget): The window dialog to be closed after updating the user.
        """
        try:
            # Extract user data from the input dictionary
            username = data.get('username', '').strip()
            full_name = data.get('full_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            status = data.get("status", {}).get("data", 0)
            user_type = data.get("user_type", {}).get("text", None)

            # Validate required fields
            if not (username and password and email):
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return

            # Update user data based on whether the password is provided
            if password:
                self.db.update_user(self.user_id, username, full_name, email, status, user_type, password)
            else:
                self.db.update_user_without_password(self.user_id, username, full_name, email, status, user_type)

            # Reload the user table and show success message
            self.load_users_table()
            QMessageBox.information(self, "Success", "User updated successfully!")
            window.close()

        except Exception as e:
            # Handle unexpected errors and display them to the user
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_user(self):
        """
        Delete the selected user from the database after confirmation.
        """
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a user to delete.")
            return  # Exit early if no row is selected

        # Get user ID from the selected row
        user_id = int(self.table.item(selected_row, 0).text())

        # Confirm deletion
        confirmation = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            try:
                self.db.delete_user(user_id)  # Delete the user from the database
                self.load_users_table()  # Refresh the table
                QMessageBox.information(self, "Success", "User deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {e}")
