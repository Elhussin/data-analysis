from PyQt5.QtWidgets import (
    QDialog,QMessageBox, QHeaderView,QTableWidgetItem,QHBoxLayout,QCheckBox,
    QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton,QSpinBox
)
from PyQt5.QtGui import QColor

color_map = {
    "Active": QColor("#4CAF50"),
    "Inactive": QColor("#9E9E9E"),
    "In Lap": QColor("#f8ffc0"),
    "In Shop": QColor("#d8fbd8"),
    "Delivery": QColor("#6a876840"),
    "Send To Lab": QColor("#f8ffc0"),
}


class DynamicForm(QDialog):
    def __init__(self, fields, submit_callback, default_values=None,button_text="Submit", parent=None):
        """
        Initialize a dynamic form with specified fields.
        :param fields: List of dictionaries defining form fields.
        :param button_text: Text for the submit button.
        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.submit_callback = submit_callback  
        self.setGeometry(200, 200, 400, 350)
        self.fields = fields
        self.field_widgets = {}
        self.default_values=default_values or{}
        # self.default_values={}
        self.button_text=button_text
        self.init_ui()

    def init_ui(self):
        """
        Initialize the form layout dynamically.
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create form fields dynamically
        for field in self.fields:
            label = QLabel(field['label'], self)
            default_value = self.default_values.get(field['name'], "")  # Get default value

            if field['type'] == 'text':
                input_widget = QLineEdit(self)
                input_widget.setText(default_value if isinstance(default_value, str) else "")
                input_widget.setPlaceholderText(field.get('placeholder', ''))
            elif field['type'] == 'password':
                input_widget = QLineEdit(self)
                input_widget.setEchoMode(QLineEdit.Password)
                input_widget.setText(default_value if isinstance(default_value, str) else "")
                input_widget.setPlaceholderText(field.get('placeholder', ''))
            elif field['type'] == 'combo':
                input_widget = QComboBox(self)
                options = field.get('options', [])

                # Add options to the combo box
                for option in options:
                    if isinstance(option, dict):
                        input_widget.addItem(option['name'], option['id'])
                    elif isinstance(option, str):
                        input_widget.addItem(option)
                    else:
                        raise ValueError(f"Invalid option type: {type(option)}")

                # Set default value for combo box
                if isinstance(default_value, dict) and "id" in default_value:
                    index = next((i for i, option in enumerate(options)
                                if isinstance(option, dict) and option.get("id") == default_value["id"]), -1)
                    if index != -1:
                        input_widget.setCurrentIndex(index)
                elif isinstance(default_value, str):
                    input_widget.setCurrentText(default_value)
                else:
                    input_widget.setCurrentIndex(0)  # Default to first item if no match found
            else:
                raise ValueError(f"Unsupported field type: {field['type']}")

            # Add field to the layout
            form_layout.addRow(label, input_widget)
            self.field_widgets[field['name']] = input_widget

        # Add submit button
        self.submit_button = QPushButton(self.button_text, self)
        self.submit_button.clicked.connect(self.handle_submit)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def handle_submit(self):
        """
        Collects form data and passes it to the submit callback.
        """
        form_data = {}
        
        for name, widget in self.field_widgets.items():
            # if QLineEdit
            if isinstance(widget, QLineEdit):
                form_data[name] = widget.text()
            # if QComboBox
            elif isinstance(widget, QComboBox):
                form_data[name] = {
                    "text": widget.currentText(),  # text
                    "data": widget.currentData()   # value if 
                }
            elif isinstance(widget, QCheckBox):
                form_data[name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                form_data[name] = widget.value()
            # add defualt falue
            else:
                form_data[name] = None  # set deafualt 
            
        #add data to callback
        self.submit_callback(form_data)


class DynamicTableButtons:
    # creat buttons 
    def creat_button(self, buttons, layout=None):
            """
            Create buttons dynamically and add them to the provided layout.
            """
            # Use provided layout or create a new one
            button_layout = layout or QHBoxLayout()

            for button_info in buttons:
                button = self.creat_button_cheeck(button_info)
                if button:
                    button_layout.addWidget(button)
                button.setDefault(True)
            return button_layout

    def creat_button_cheeck(self, button_info):
        """
        Create a QPushButton dynamically and connect it to the provided callback.
        """
        try:
            # Ensure button_info contains required keys
            if "text" not in button_info:
                raise ValueError("Button info must contain a 'text' key.")

            # Create the button
            button = QPushButton(button_info["text"])

            # Get the callback and validate it
            callback = button_info.get("callback")
            if callback is not None:
                button.clicked.connect(callback)
            else:
                button.clicked.connect(self.default_callback)  # Use a default callback

            return button

        except Exception as e:
            print(f"Error creating button: {e}")
            return None
    def default_callback(self):
        """
        Default callback function when no callback is provided.
        """
        QMessageBox.information(None, "Info", "This button has no action assigned.")

    def populate_table(self,table_widget, data, exclude_columns=None):
        """
        Populate a QTableWidget with dynamic data.

        Args:
            table_widget (QTableWidget): The table widget to populate.
            data (list of dict): The data to display in the table.
            exclude_columns (list): Columns to exclude from display (optional).
        """
        if not data:
            table_widget.clearContents()
            table_widget.setRowCount(0)
            # QMessageBox.information(None, "No Data", "No data available to display.")
            return

        # Extract column names and exclude specific columns
        exclude_columns = exclude_columns or []
        columns = [col for col in data[0].keys() if col not in exclude_columns]
        columns_header = [col.replace('_', ' ').capitalize() for col in columns]

        # Set up the table
        # table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(columns))

        table_widget.setHorizontalHeaderLabels(columns_header)
        table_widget.setRowCount(100)  # عرض 100 صف فقط في البداية

        # set row height
        # table_widget.resizeRowsToContents()

        # Set column resizing, sorting options, and enable manual resizing of columns
        header = table_widget.horizontalHeader()
        for i in range(len(columns)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)  # Stretch all columns to fill the screen
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Make the first column resizable manually
        table_widget.setSortingEnabled(True)  # Enable sorting on table columns

        for row_index, row_data in enumerate(reversed(data)):
            for col_index, column in enumerate(columns):


                value = row_data.get(column)
                if column == "status":  # Check if the column is 'status'
                    display_value = "Active" if value == 1 else "Inactive" if value == 0 else value

                else:
                    display_value = value if value is not None else "N/A"
                
                background_color = color_map.get(display_value, QColor("white"))

                # Handle complex data types
                if isinstance(display_value, (list, dict)):
                    display_value = str(display_value)

                # Create the table item
                item = QTableWidgetItem(str(display_value))
                
                # Set the background color
                item.setBackground(background_color)
                
                # Set the item in the table
                table_widget.setItem(row_index, col_index, item)