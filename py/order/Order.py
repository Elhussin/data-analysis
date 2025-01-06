from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QTableWidgetItem, QMessageBox, QHBoxLayout, QPushButton
from dataBase.database import UserDatabase, OrderModel, BranchManagerDatabase
from py.form import DynamicForm, DynamicTableButtons
from py.data import userFormFields
from py.functian import get_credentials_user_id_qsettings, show_auto_close_messagebox

from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class OrderManage(QWidget):
    """ 
    Main widget for managing order data. Allows adding, deleting, and editing orders records.
    """
    def __init__(self ,parent=None):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setup_database()
        self.init_ui()

    def setup_database(self):
        """Initialize database connections."""
        self.db_order = OrderModel()
        self.db_branch_manager = BranchManagerDatabase()
        self.dynamic_buttons_or_tables = DynamicTableButtons()
        self.db_users=UserDatabase()
   

    def init_ui(self):
        """Setup UI components and layout."""        
        buttons = [
            {"text": "Send Order To Lab", "callback": self.open_send_to_lab},
            {"text": "Get Order from Lab", "callback": self.open_get_from_lab},
            {"text": "OrderDilvered", "callback": self.open_dilvery_to_coutmer},
        ]

        self.layout = QVBoxLayout()     

        # Search and Filters   
        self.setup_search()
        self.user_id=get_credentials_user_id_qsettings()

        if self.user_id:
            self.userData=self.db_users.get_user_by_id(self.user_id)
            Branch_details=self.db_branch_manager.fetch_manager_by_user(self.user_id)
            if not Branch_details  :
                QMessageBox.critical(self, "Error", "You are not allowed to manage orders.")
            elif Branch_details['status']==0: 
                QMessageBox.critical(self, "Error", "Your account is not active.")
            else:
                self.branch_id=Branch_details['branch']
                
                # Create buttons and add them to the layout
                button_layout = self.dynamic_buttons_or_tables.creat_button(buttons)
                self.layout.addLayout(button_layout)
        
        # Order Table
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table) 

        self.load_order_table()  # Load users into the table

        self.table.setObjectName('OrderTable')
        self.setLayout(self.layout)


    def setup_search(self):
        """Add search box and status filter."""
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search by order number ...")
        self.search_box.textChanged.connect(self.perform_search)

        self.status_filter = QComboBox(self)
        self.status_filter.addItems(["All", "Send To Lab", "Delivery", "In Shop"])
        self.status_filter.currentTextChanged.connect(self.perform_search)

        filter_layout = QHBoxLayout() 
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)
        self.layout.addWidget(self.search_box)
        self.layout.addLayout(filter_layout)  

    def perform_search(self):
        """Handle search functionality."""
        input_text = self.search_box.text()
        selected_status = self.status_filter.currentText()
        # results = self.db_order.search_orders(input_text, selected_status)
        result =self.db_order.fetch_orders(filters=self.filter_data_per_user(), search_text=input_text, status_filter=selected_status)
        self.load_order_table(result,selected_status)

    def filter_data_per_user(self):
        if self.userData:
            user_type = self.userData.get('user_type')
            user_id = self.userData.get('id')

            if user_type in ['User', 'Staff']:
                filterData = {"Orders.user": user_id}
            else:
                filterData = {}
        else:
            filterData = {}

        return filterData
    



    def load_order_table(self,data=None,search_txt=None):

        """Load data into the table."""
        try:
             # Fetch  Order
            orders = data if search_txt else self.db_order.fetch_orders(filters=self.filter_data_per_user())

            self.dynamic_buttons_or_tables.populate_table(self.table,orders)
            self.add_buttons_to_table(self.table)

        except Exception as e:
            # Handle potential errors, like database connection issues
            QMessageBox.critical(self, "Error", f"An error occurred while loading users: {str(e)}")

    def validate_order_number(self, input_text):
        """Validate the order number input."""
        return input_text.isdigit() and len(input_text) in [4, 10, 11]

    def construct_order_number(self, branch_id, input_text):
        """Construct the full order number based on the branch ID and input."""
        if len(input_text) == 4:
            current_year = datetime.now().year
            return f"{branch_id}{current_year}{input_text}"
        return input_text

    def open_send_to_lab(self):
        # self.parent_window.stacked_widget.setCurrentIndex(5)
        add_input_with_button(self, "Send To Lap", "Send Order To Lap", self.send_order)

    def open_get_from_lab(self):

        add_input_with_button(self, "Get From Lap ", "Get Order From Lab", self.update_order_status,"In Shop")

    def open_dilvery_to_coutmer(self):
        add_input_with_button(self,"Delivery", "Submit Order To Coustmer", self.update_order_status,"Delivery" )
    
    def send_order(self, input_text,tergat):
        """
        Validate and send an order to the database.

        Parameters:
            input_text (str): The order number input by the user.

        Returns:
            None
        """
        try:
            # Validate the order number
            if not self.validate_order_number(input_text):
                QMessageBox.critical(self, "Error", "Invalid input. Must be 4, 10, or 11 digits.")
                return  # Ensure the function terminates for invalid input

            # Construct the full order number
            order_number = self.construct_order_number(self.branch_id, input_text)

            # Check if the order already exists
            order=self.db_order.getOrderBySerial(order_number)

            if order:
                if order['status'] == "Delivery" or  order['status'] == "In Shop":
                    confirmation = QMessageBox.question(
                        self,
                        "Confirm Update",
                        f"Order No: {order_number} is already {order['status']}. Do you want to revert it to 'Lap'?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )
                    if confirmation != QMessageBox.Yes:
                        return
                    else:
                        self.update_order_status( str(order['Serial']), "Send To Lab")
                        return

                else:
                    QMessageBox.critical(self, "Error", f"Order No: {order_number} already   : {order['status']}.")
                    return

            # Add the order to the database
            if self.db_order.add_order(order_number, self.branch_id, self.user_id):
                show_auto_close_messagebox(self, "Success", f"Order No: {order_number} added successfully!", timeout=3000)
                self.load_order_table()
                self.search_box.clear()  # Clear the search box after success
            else:
                QMessageBox.critical(self, "Error", "Failed to add the order. Please try again.")
        except Exception as e:
            logging.error(f"Failed to add order: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def update_order_by_index(self,row):
        if row is None or row < 0:
            return

        column_count = self.table.columnCount()
        row_data = [self.table.item(row, col).text() if self.table.item(row, col) else None for col in range(column_count)]
        order=self.db_order.getOrderBySerial(row_data[1])
        status= "In Shop" if order['status'] == 'Send To Lab' or order['status'] == 'In Lap' else "Delivery"
        if status == order['status'] :
            
            QMessageBox.critical(self, "Error", f"Order No: {order['Serial']} is already {order['status']}.")

            return
        confirmation = QMessageBox.question(
            self,
            "Confirm Update",
            f"Order No: {order['Serial']} is already {order['status']}. Do you want update it to '{status}' ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirmation != QMessageBox.Yes:
            return
        else:
            # self.update_order_status( str(order['Serial']), "Send To Lab")
            self.update_order_status(str(order['Serial']),status)
            return

        

    def delete_order_by_index(self, row):
        """Delete an order based on its table row index."""
        if row is None or row < 0:
            return

        column_count = self.table.columnCount()
        row_data = [self.table.item(row, col).text() if self.table.item(row, col) else None for col in range(column_count)]

        confirmation = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete this Order {row_data[1]}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            try:
                if self.db_order.delete_row(row_data[0]):
                    show_auto_close_messagebox(self, "Success", f"Order No {row_data[1]} deleted successfully!", timeout=3000)
                    self.load_order_table()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete this order.")
            except Exception as e:
                logging.error(f"Failed to delete order: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete this order: {e}")
                return

    def add_buttons_to_table(self, table):
        """Add update and delete buttons to each row in the table."""
        table.setColumnCount(table.columnCount() + 1)
        actions_column = table.columnCount() - 1
        table.setHorizontalHeaderItem(actions_column, QTableWidgetItem("Actions"))
        table.setColumnWidth(actions_column, 150)

        for row in range(table.rowCount()):
            update_button = QPushButton("Update")
            update_button.clicked.connect(lambda _, r=row: self.update_order_by_index(r))

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=row: self.delete_order_by_index(r))

            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(update_button)
            layout.addWidget(delete_button)
            table.setCellWidget(row, actions_column, cell_widget)
            table.setCellWidget(row,actions_column, cell_widget)
            table.setRowHeight(row,50)

    def update_order_status(self, input_text, target_status):
        """
        Update the status of an order based on the input text and target status.

        Parameters:
            input_text (str): The order number input by the user.
            target_status (str): The target status to update the order to.

        Returns:
            None
        """
        try:
            # Validate the input
            if not self.validate_order_number(input_text):
                QMessageBox.critical(self, "Error", "Invalid input. Must be 4, 10, or 11 digits.")
                return

            # Construct the order number
            order_number = self.construct_order_number(self.branch_id, input_text)

            # Fetch the order from the database
            order = self.db_order.getOrderBySerial(order_number)
            if not order:
                QMessageBox.critical(self, "Error", f"Order No: {order_number} does not exist.")
                return

            # Restrictions for status transitions
            if order['status'] == "In Lab" or order['status'] == "Send To Lab"  and target_status == "Delivery":
                # QMessageBox.critical(self, "Error", "Orders in 'In Lab' status cannot be updated to 'Delivery'.")
                # # return
                confirmation = QMessageBox.question(
                    self,
                    "Confirm Update",
                    f"Order No: {order_number} is in 'In Lab' . Do you want to  updated to 'Delivery'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if confirmation != QMessageBox.Yes:
                    return
            

            if order['status'] == "Delivery" and target_status == "In Shop":
                confirmation = QMessageBox.question(
                    self,
                    "Confirm Update",
                    f"Order No: {order_number} is already delivered. Do you want to revert it to 'In Shop'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if confirmation != QMessageBox.Yes:
                    return

            # Check if the status is already updated
            if order['status'] == target_status:
                QMessageBox.information(self, "Info", f"Order No: {order_number} is already {target_status}.")
                return
            

            # Perform the status update
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.db_order.update_order(order['id'], status=target_status, updated_at=current_time):
                show_auto_close_messagebox(self, "Success", f"Order No: {order_number} updated to {target_status} successfully!", timeout=3000)
                self.load_order_table()
            else:
                QMessageBox.critical(self, "Error", "Failed to update the order. Please try again.")
        except Exception as e:
            logging.error(f"Failed to update order: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

def add_input_with_button(self, button_text, placeholder_text, button_function, target_status=''):
        """
        Dynamically add or update an input field and button.

        :param button_text: Text to display on the button.
        :param placeholder_text: Placeholder text for the input field.
        :param button_function: Function to call when the button is pressed.
        :param target_status: Optional status to pass to the button function.
        """
        # Check if the layout already has input elements
        if hasattr(self, 'input_layout'):
            # Update placeholder text
            self.line_edit.setPlaceholderText(placeholder_text)

            # Disconnect any previous connections and reconnect with the new function
            try:
                self.line_edit.returnPressed.disconnect()
            except TypeError:
                pass

            self.line_edit.returnPressed.connect(lambda: button_function(self.line_edit.text(), target_status))

            # Update button text and connection
            self.button.setText(button_text)
            try:
                self.button.clicked.disconnect()
            except TypeError:
                pass

            self.button.clicked.connect(lambda: button_function(self.line_edit.text(), target_status))
        else:
            # Create a new layout if not already present
            self.input_layout = QHBoxLayout()

            # Create input field
            self.line_edit = QLineEdit()
            self.line_edit.setPlaceholderText(placeholder_text)
            self.line_edit.returnPressed.connect(lambda: button_function(self.line_edit.text(), target_status))

            # Create button
            self.button = QPushButton(button_text)
            self.button.clicked.connect(lambda: button_function(self.line_edit.text(), target_status))
            self.button.setDefault(True)

            # Add elements to the layout
            self.input_layout.addWidget(self.line_edit)
            self.input_layout.addWidget(self.button)

            # Add the layout to the main layout
            widget_to_move = self.layout.itemAt(3).widget()
            self.layout.addLayout(self.input_layout)
            self.layout.removeWidget(widget_to_move)
            self.layout.insertWidget(4, widget_to_move)

