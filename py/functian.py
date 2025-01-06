from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox
import os
import shutil
import time
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
def load_stylesheet(app, file_path):
    """
    Load and apply a QSS stylesheet file to the QApplication.

    Args:
        app (QApplication): The PyQt5 application instance.
        file_path (str): Path to the QSS stylesheet file.
    """
    try:
        with open(file_path, "r") as file:
            app.setStyleSheet(file.read())
    except Exception as e:
        print(f"Error loading QSS file: {e}")

def hendel_register_user(self, full_name, username, email, password, db):
    """
    Handles the user registration process by validating inputs and checking database.

    Args:
        self (QWidget): The calling widget instance.
        full_name (str): Full name of the user.
        username (str): Username for registration.
        email (str): Email of the user.
        password (str): Password for the account.
        db (object): Database instance to validate and save user information.
    """
    if not full_name or not username or not email or not password:
        QMessageBox.warning(self, "Error", "Please fill in all fields")
        return

    # Check if the username already exists in the database
    if db.check_user(username, password):
        QMessageBox.warning(self, "Error", "Username already exists")
        return
    else:
        QMessageBox.warning(self, "Error", "Registration failed, please try again.")

def show_message(self, icon_type=QMessageBox.Information, title="Information", message=""):
    """
    Displays a message box to the user.

    Args:
        self (QWidget): The calling widget instance.
        icon_type (QMessageBox.Icon): The type of icon to display (e.g., Information, Warning).
        title (str): The title of the message box.
        message (str): The message content to display.
    """
    msg_box = QMessageBox(self)
    msg_box.setIcon(icon_type)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.adjustSize()  # Automatically adjusts the size based on content
    msg_box.exec_()
    # def show_message(self, title, message):
    #     """ إظهار رسالة للمستخدم """
    #     msg = QMessageBox()
    #     msg.setIcon(QMessageBox.Information)
    #     msg.setText(message)
    #     msg.setWindowTitle(title)
    #     msg.exec_()


def clean_all_caches(root_path=".", folder_name="__pycache__", age_limit_seconds=86400):
    """
    Deletes all folders with the specified name within the root_path if they are older than the age limit.

    Args:
        root_path (str): The root directory to start searching from. Defaults to the current directory.
        folder_name (str): The name of the folders to delete. Defaults to "__pycache__".
        age_limit_seconds (int): The age limit in seconds. Folders older than this will be deleted. Defaults to 86400 (1 day).

    Returns:
        int: The count of folders deleted.
    """
    deleted_count = 0

    for dirpath, dirnames, _ in os.walk(root_path):
        if folder_name in dirnames:
            folder_path = os.path.join(dirpath, folder_name)
            
            try:
                # Get the last modified time of the folder
                last_modified_time = os.path.getmtime(folder_path)
                current_time = time.time()
                folder_age = current_time - last_modified_time

                # Check if the folder is older than the age limit
                if folder_age > age_limit_seconds:
                    shutil.rmtree(folder_path)
                    logging.info(f"Deleted folder: {folder_path}, Age: {folder_age} seconds")
                    deleted_count += 1
                else:
                    logging.info(f"Folder {folder_path} is not old enough to delete. Age: {folder_age} seconds")
            except PermissionError:
                logging.error(f"Permission denied while deleting folder: {folder_path}")
            except Exception as e:
                logging.error(f"Error occurred while deleting folder {folder_path}: {e}")

    return deleted_count



# Initialize QSettings for saving and retrieving application settings
settings = QSettings("Hussain Dev", "Order")

def load_credentials_qsettings():
    """
    Loads saved credentials (username and password) from QSettings.

    Returns:
        tuple: A tuple containing the saved username and password.
    """
    username = settings.value("username", "")
    password = settings.value("password", "")
    return username, password

def save_credentials_qsettings(username, password):
    """
    Saves user credentials (username and password) to QSettings.

    Args:
        username (str): The username to save.
        password (str): The password to save.
    """
    settings.setValue("username", username)
    settings.setValue("password", password)

def clear_credentials_qsettings():
    """
    Clears saved credentials and user ID from QSettings.
    """
    settings.remove("username")
    settings.remove("password")
    settings.remove("user_id")

def save_credentials_user_id(user_id):
    """
    Saves the user ID to QSettings.

    Args:
        self (QWidget): The calling widget instance.
        user_id (int): The user ID to save.
    """
    settings.setValue("user_id", user_id)

def get_credentials_user_id_qsettings():
    if settings.contains("user_id"):
        return settings.value("user_id")
    else:
        
        return None

def check_saved_credentials(self):
    """
    Checks for saved credentials in QSettings and populates the login fields.

    Args:
        self (QWidget): The calling widget instance.
    """
    if settings.contains("username") and settings.contains("password"):
        saved_username = settings.value("username", "")
        saved_password = settings.value("password", "")
        self.username_input.setText(saved_username)
        self.password_input.setText(saved_password)
        self.remember_me_checkbox.setChecked(True)  # Mark the "Remember me" checkbox as checked

def result_as_dict(data, description):
    """
    Converts database query results into a dictionary or a list of dictionaries.

    Args:
        data (tuple or list): The data retrieved from the database query.
        description (list): Column descriptions for the database table.

    Returns:
        dict or list: A dictionary for a single row or a list of dictionaries for multiple rows.
    """
    # Extract column names from the description
    column_names = [description[0] for description in description]

    # If the data is a single row (tuple)
    if isinstance(data, tuple):
        return dict(zip(column_names, data))

    # If the data is multiple rows (list of tuples)
    elif isinstance(data, list):
        return [dict(zip(column_names, row)) for row in data]

    # If data is of an unknown type (e.g., None or non-iterable)
    return None

def confirm_exit(parent, message="Are you sure you want to exit?"):
    reply = QMessageBox.question(
        parent,
        "Exit Confirmation",
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    return reply == QMessageBox.Yes


# def toggle_buttun_Visible(self):
#     self.delete_button.setVisible(not self.delete_button.isVisible())
#     self.add_button.setVisible(not self.add_button.isVisible())
#     self.update_button.setVisible(not self.update_button.isVisible())
#     self.send_update_button.setVisible(not self.send_update_button.isVisible())
#     self.back_to_form_button.setVisible(not self.back_to_form_button.isVisible())



def show_auto_close_messagebox(self, title, message, timeout=1000):
    """
    عرض رسالة باستخدام QMessageBox يتم إغلاقها تلقائيًا.
    :param title: عنوان الرسالة.
    :param message: نص الرسالة.
    :param timeout: المدة الزمنية قبل الإغلاق (بالميلي ثانية).
    """
    # إنشاء الرسالة
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    # msg_box.setStandardButtons(QMessageBox.NoButton)  # إخفاء الأزرار

    # عرض الرسالة
    msg_box.show()

    # تعيين المؤقت لإغلاق الرسالة بعد الوقت المحدد
    timer = QTimer(self)
    timer.setSingleShot(True)
    timer.timeout.connect(msg_box.close)
    timer.start(timeout)
