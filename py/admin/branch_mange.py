import sys
from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QFormLayout,QDialog,QDialogButtonBox, QApplication,QLineEdit,QHeaderView,QComboBox, QLabel, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from dataBase.database import BranchDatabase ,BranchManagerDatabase, UserDatabase# استيراد موديول قاعدة البيانات
import sys
from datetime import datetime
from py.form import DynamicForm,DynamicTableButtons
from py.data import branchFormFields


class Branchs(QWidget):
    """
    Main widget for managing branches. 
    Provides functionality to add, edit, delete, and display branches.
    """

    def __init__(self, parent=None):
        """
        Initializes the Branch management widget.
        
        Args:
            parent: The parent widget (optional).
        """
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.db_manager = BranchDatabase()  # Initialize the database manager
        self.creatTableOrbuttons = DynamicTableButtons()
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface components including buttons and the table.
        """
        # Define button configurations
        buttons = [
            {"text": "Add Branch", "callback": lambda: self.open_add_branche_dialog(branchFormFields)},
            {"text": "Delete Branch", "callback": self.delete_branch},
            {"text": "Edit Branch", "callback": lambda: self.open_edit_branche_dialog(branchFormFields)},
        ]

        self.layout = QVBoxLayout()

        # Create buttons and add them to the layout
        button_layout = self.creatTableOrbuttons.creat_button(buttons)
        self.layout.addLayout(button_layout)

        # Create a table to display branch data
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.load_branches_table()  # Load branches into the table

    def load_branches_table(self):
        """
        Fetches and displays all branches in the table.
        Displays a message if no branches are found or an error occurs.
        """
        try:

            branches = self.db_manager.fetch_all_branches()  # Fetch branch data
            if not branches:
                QMessageBox.information(self, "No Data", "No branches found in the database.")
                return
            self.creatTableOrbuttons.populate_table(self.table, branches)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading branches: {str(e)}")

    def open_add_branche_dialog(self, fields):
        """
        Opens a dialog to add a new branch.

        Args:
            fields: A list of fields required for the branch form.
        """
        dialog = DynamicForm(fields, lambda data: self.add_branch(data, dialog), button_text="Add Branch")
        if dialog.exec_() == QDialog.Accepted:
            self.load_branches_table()  # Refresh table after adding the branch

    def add_branch(self, data, window):
        """
        Adds a new branch to the database after validation.

        Args:
            data: A dictionary containing branch details.
            window: The dialog window for adding the branch.
        """
        try:
            branch_name = data.get('branch_name', '').strip()
            branch_location = data.get('branch_location', '').strip()
            branch_phone = data.get('branch_phone', '').strip()
            status = data.get("status", {}).get("data", 0)

            if not (branch_name and branch_phone and branch_location):
                QMessageBox.warning(self, "Error", "Please fill in all required fields.")
                return

            if self.db_manager.fetch_branche_by_name(branch_name):
                QMessageBox.warning(self, "Error", "Branch already exists.")
                return

            is_added = self.db_manager.insert_branch(branch_name, branch_location, branch_phone, status)

            if is_added:
                QMessageBox.information(self, "Success", "Branch added successfully!")
                self.load_branches_table()
                window.close()
            else:
                QMessageBox.critical(self, "Error", "Failed to add branch. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def open_edit_branche_dialog(self, fields):
        """
        Opens a dialog to edit the selected branch.

        Args:
            fields: A list of fields required for the branch form.
        """
        try:
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Error", "Please select a branch to edit.")
                return

            branch_id = int(self.table.item(selected_row, 0).text())
            branch = self.db_manager.fetch_one_branche(branch_id)

            if not branch:
                QMessageBox.warning(self, "Error", "Branch not found.")
                return

            branch['status'] = "Active" if branch['status'] == 1 else "Inactive"

            dialog = DynamicForm(
                fields,
                lambda data: self.update_branch(data, dialog),
                branch,
                button_text="Update Branch"
            )

            if dialog.exec_() == QDialog.Accepted:
                self.load_branches_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def update_branch(self, data, window):
        """
        Updates an existing branch in the database.

        Args:
            data: A dictionary containing updated branch details.
            window: The dialog window for editing the branch.
        """
        try:
            selected_row = self.table.currentRow()
            branch_id = int(self.table.item(selected_row, 0).text())
            branch_name = data.get('branch_name', '').strip()
            branch_location = data.get('branch_location', '').strip()
            branch_phone = data.get('branch_phone', '').strip()
            status = data.get("status", {}).get("data", 0)

            if not (branch_name and branch_location and branch_phone):
                QMessageBox.warning(self, "Error", "Please fill in all required fields.")
                return

            is_update = self.db_manager.update_branch(branch_id, branch_name, branch_location, branch_phone, status)

            if is_update:
                QMessageBox.information(self, "Success", "Branch updated successfully.")
                self.load_branches_table()
                window.close()
            else:
                QMessageBox.critical(self, "Error", "Failed to update branch. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def delete_branch(self):
        """
        Deletes the selected branch from the database.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            branch_id = int(self.table.item(selected_row, 0).text())
            confirmation = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this branch?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.db_manager.delete_branch(branch_id)
                self.load_branches_table()
                QMessageBox.information(self, "Success", "Branch deleted successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please select a branch to delete.")




class BranchManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.db_manager = BranchManagerDatabase()  # إنشاء كائن من ManagerDatabase
        self.db_BranchDatabase = BranchDatabase()  # إنشاء كائن من DatabaseManager
        self.db_users = UserDatabase()
        self.creatTableOrbuttons=DynamicTableButtons()
        self.init_ui()
    def init_ui(self):
        
        branches = self.db_BranchDatabase.fetch_all_branches()
        users = self.db_users.get_all_users()

        branchMangerFormFields = [
                {"name": "branch", "label": "Branch Name:", "type": "combo", "options": [{"name": branch['branch_name'], "id": branch['id']} for branch in branches if branch['status'] == 1]},
                {"name": "user", "label": "Manger Name:", "type": "combo", "options": [{"name": user['username'], "id": user['id']} for user in users if user['status'] == 1]},
                {"name": "status", "label": "Manger Status:", "type": "combo", "options": [{"name": "Active", "id": 1}, {"name": "Inactive", "id": 0}]},
            ]
     
        buttons = [
            {"text": "Add Manager", "callback": lambda: self.show_add_dialog(branchMangerFormFields)},
            {"text": "Update Manager", "callback":lambda: self.show_update_dialog(branchMangerFormFields)},
            {"text": "Delete Manager", "callback":self.delete_manager},
        ]

        self.layout = QVBoxLayout()
        
        # Create buttons and add them to the layout
        button_layout = self.creatTableOrbuttons.creat_button(buttons)
        self.layout.addLayout(button_layout)

        # Create table to display users
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)
        

        self.setLayout(self.layout)
        self.load_managers_table_table()


    def load_managers_table_table(self):
        """ تحميل جميع مديري الفروع من قاعدة البيانات وعرضها في الجدول """
        # استدعاء بيانات المديرين من قاعدة البيانات
        try:
            self.managers = self.db_manager.fetch_all_managers_with_details()
            if not self.managers:
                QMessageBox.information(self, "No Data", "No Manger found in the database.")
                return
            
            self.creatTableOrbuttons.populate_table(self.table,self.managers)

        except Exception as e:
            # Handle potential errors, like database connection issues
            QMessageBox.critical(self, "Error", f"An error occurred while loading branch manger: {str(e)}")


    def show_add_dialog(self,fields):
        
        dialog = DynamicForm(fields, lambda data: self.add_branch_manger(data, dialog), button_text="Add Branch Manger")

        # Open Window
        if dialog.exec_() == QDialog.Accepted:
            # Validate fields before accepting the dialog
                self.load_managers_table_table()  # Refresh the table after adding a new user
    
    def add_branch_manger(self, data, window):
        try:

            branch = self.get_data_field(data, "branch")
            user = self.get_data_field(data, "user")
            status = self.get_data_field(data, "status")

            # Validate required fields
            if not (branch and user):
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return

        #     # Check if the username already exists
            if not self.db_users.get_user_by_id(user):
                QMessageBox.warning(self, "Error", f"This User ID{user} not exists.")
                return

            if not self.db_BranchDatabase.fetch_one_branche(branch):
                QMessageBox.warning(self, "Error", f"This branch ID: {branch} not exists.")
                return
            # conf=self.db_manager.fetch_manager_by_user(user)
            if self.db_manager.fetch_manager_by_user(user):
                QMessageBox.warning(self, "Error", f"This User ID: {user} alredy exists in onther branch.")
                return
            is_added = self.db_manager.insert_manager(branch,user,status)

            if is_added:
                self.load_managers_table_table()  # Reload the table after adding the user
                QMessageBox.information(self, "Success", "Branch manger registered successfully!")
                window.close()
            else:
                QMessageBox.critical(self, "Error", "Registration failed. Please try again.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


    def show_update_dialog(self,fields):
        try:
                        # Get the selected row
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Error", "Please select a manger to update.")
                return
            self.manager_id = int(self.table.item(selected_row, 0).text())
            manager_data = next((item for item in self.managers if item['id'] == self.manager_id), None)
            # manager_data = self.db_manager.fetch_manager(manager_id)

            default_values = {
                "branch": {"name": manager_data['branch_name'], "id": manager_data['branch']},
                "user": {"name": manager_data['user_name'], "id": manager_data['user']},
                "status": "Active" if manager_data['status'] == 1 else "Inactive"
 
                    # أو {"name": "Inactive", "id": 0} حسب الحالة

            }
                        # branch['status'] = "Active" if branch['status'] == 1 else "Inactive"

            # "status":branch['status'] = "Active" if branch['status'] == 1 else "Inactive"

            if not manager_data:
                QMessageBox.warning(self, "Error", "User not found!")
                return
            # print("manager_data",manager_data)
            if manager_data['status']==1:
                manager_data['status']= "Active"
               
            else:
                manager_data['status']= "Inactive"
                       
            # Open the dynamic form for editing user details
            print("manager_data",manager_data)
            dialog = DynamicForm(
                fields,
                lambda data: self.update_manager(data, dialog),
                default_values,
                button_text="Update Branch"
            )
                # Execute the dialog and refresh the table if the user clicks "Update"
            if dialog.exec_() == QDialog.Accepted:
                self.load_managers_table_table()

        except Exception as e:
            # Handle unexpected errors
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def update_manager(self,data,window):

        """
        Update the branch MAmanger data after editing.

        Args:
            data (dict): A dictionary containing the updated user data.
            window (QWidget): The window dialog to be closed after updating the user.
        """
        try:
            branch = self.get_data_field(data, "branch")
            user = self.get_data_field(data, "user")
            status = self.get_data_field(data, "status")

            # Validate required fields
            if not (branch and user):
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return

        #     # Check if the username already exists
            if not self.db_users.get_user_by_id(user):
                QMessageBox.warning(self, "Error", f"This User ID{user} not exists.")
                return

            if not self.db_BranchDatabase.fetch_one_branche(branch):
                QMessageBox.warning(self, "Error", f"This branch ID: {branch} not exists.")
                return
            # # conf=self.db_manager.fetch_manager_by_user(user)
            # if self.db_manager.fetch_manager_by_user(user):
            #     QMessageBox.warning(self, "Error", f"This User ID: {user} alredy exists in onther branch.")
            #     return
            if not self.verify_user_not_connent_onther_branch(self.manager_id, user):
                QMessageBox.warning(self, "Error", f"This User ID: {user} alredy exists in onther branch. .")
                return

            is_update=self.db_manager.update_manager(branch,user,status,self.manager_id)
            if is_update:
            # Reload the user table and show success message
                self.load_managers_table_table()
                QMessageBox.information(self, "Success", "Branch Manger updated successfully!")
                window.close()
            else:
                QMessageBox.critical(self, "Error", "update failed. Please try again.")

        except Exception as e:
            # Handle unexpected errors and display them to the user
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
 

    def delete_manager(self):
        """ حذف مدير الفرع """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            
            manager_id = int(self.table.item(selected_row, 0).text())
            confirmation = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this Branch Manger?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.db_manager.delete_manager(manager_id)
                self.load_managers_table_table()  # إعادة تحميل البيانات في الجدول
                QMessageBox.information(self, "Success", "User deleted successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please select a Branch Manger to delete.")
            

    def get_data_field(self,data, field_name, default=0):
                field = data.get(field_name)
                if isinstance(field, dict):
                    return field.get("data", default)
                return default

    
    def verify_user_not_connent_onther_branch(self, id, user_id):
        managers = self.db_manager.fetch_all_managers()

        record = next((item for item in managers if item['user'] == user_id), None)
        if record ==None:
            return True

        elif record and record.get('id') == id:
                return True
        else:
            return False