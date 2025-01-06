from PyQt5.QtWidgets import QApplication,QHBoxLayout, QFrame, QWidget, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont,QIcon
from py.eyeTest.EyeContactLensValidator import ContactLensValidator
from py.eyeTest.EyeTestValidator import EyeTestValidator
from py.functian import load_stylesheet
import sys
# from py.layOut.icon import Icon 
import os
class EyeContactLens(QWidget):
    """
    A class to represent the form table widget for eye test and contact lens validation.

    This widget allows the user to input values for the eye test (SPH, CYL, AXIS, etc.) 
    and perform validation and conversion into different lens types (Spheric, Toric).
    """

    def __init__(self):
        """
        Initialize the form table and associated validators.

        Sets up the table with 2 rows and 8 columns for entering eye test data. It also sets up 
        a result table for displaying calculated lens values.
        """
        super().__init__()
        self.contact_lens_validator = ContactLensValidator()  # Initializes the contact lens validator
        self.eye_test_validator = EyeTestValidator()  # Initializes the eye test validator
        # load_stylesheet(self, "py/static/style/auth.qss")  # Load custom stylesheet for the widget
        
        self.init_ui()  # Initialize the user interface
    
    def init_ui(self):
        """
        Initialize the user interface for the form table.

        Sets up the table for input, a button for validation, and the result table.
        """
        # self.setWindowTitle("Lens Power Form")  # Set the window title
        # self.setGeometry(100, 100, 600, 400)  # Set the window size and position

        # Create tables for input and results
        # Define the column headers for the main table
        self.header=["SPH", "CY", "AX", "ADD", "PD", "SG", "BV"]
        # Define the column headers for the result table
        self.result_header= ["Exact SPH", "Exact CY", "SPH", "CY", "AX", "ADD", "BV"]
        self.table = self.create_table(2, 8, self.header,["R","L"])  # Create the input data table
        self.verticalHEader=["","R","L","","R","L"]
        self.result_table = self.create_table(6, 8, self.result_header, self.verticalHEader)  # Create the result table

        # Create check button
        self.check_button = self.create_check_button()
        self.check_button.setObjectName("cotact_lens")
        layout = QVBoxLayout()  # Create the vertical layout
        layout.addWidget(self.table)  # Add the input table to the layout
        layout.addWidget(self.check_button, alignment=Qt.AlignCenter)  # Add the validation button centered
        layout.addWidget(self.result_table)  # Add the result table to the layout


        self.setLayout(layout)  # Set the layout for the widget
        # Connect cell change signal to the handler
        self.table.cellChanged.connect(self.on_cell_change)  # Detect changes in table cells
  
    def create_table(self, rows, cols, headers,vertical_headers):
        """
        Create a QTableWidget with the specified number of rows, columns, and headers.

        Args:
            rows (int): Number of rows in the table.
            cols (int): Number of columns in the table.
            headers (list): List of column headers.

        Returns:
            QTableWidget: The created table widget.
        """
        table = QTableWidget(rows, cols)  # Initialize the table with the specified rows and columns
        table.setColumnCount(len(headers))  # تأكد من ضبط عدد الأعمدة
        table.setHorizontalHeaderLabels(headers)  # Set the column headers
        table.setVerticalHeaderLabels(vertical_headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns stretchable
        table.setVerticalScrollMode(QTableWidget.ScrollPerItem)  # Enable vertical scrolling per item
        # table.setHorizontalScrollMode(QTableWidget.ScrollPerItem)  # Enable vertical scrolling per item
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setMaximumHeight(150 if rows == 2 else 400)  # Set the maximum height depending on the number of rows
        return table

    def create_check_button(self):
        """
        Create a button that triggers the validation and processing of data in the form.

        Returns:
            QPushButton: The created button widget.
        """
        button = QPushButton("Calculate")  # Create the button with text "Validate"
        button.clicked.connect(self.validate_and_process_data)  # Connect button click to validation function
        button.setMaximumWidth(200)  # Set the maximum width of the button
        return button


    def validate_and_process_data(self):
        """
        Validate the entered data and process it to calculate and display lens powers (Spheric, Toric).

        This function performs the following:
        - Extracts data from the table.
        - Validates the eye test data.
        - Formats and updates the table with the formatted values.
        - Converts the eye test data into lens powers and updates the result table.
        """
        data = self.extract_data_from_table()  # Extract data from the table

        # Filter out irrelevant data (e.g., empty values)
        filtered_data = self.filter_data(data)

        # Validate CYL and AX for both eyes
        if not self.validate_cyl_and_ax(filtered_data):
            return  # Stop if validation fails

        # Validate eyes test power
        formatted_data = self.check_valida_eye_test_power(filtered_data)
        
        # Format the eye test data
        formatted_data = self.eye_test_power_format(formatted_data)
        
        # Add formatted Power to the table
        self.update_table_with_data(formatted_data)
    
        # Updates the values in the filtered_data list to match the corresponding values from formatted_data.
        filtered_data=self.update_resualt_data_power_format(filtered_data,formatted_data )
       
        # Loop through each entry in filtered_data
        lens_data = self.process_lens_data(filtered_data)

        # Add results to the result table
        self.update_result_table(lens_data)

    def extract_data_from_table(self):
        """
        Extract data from the table into a list of dictionaries.

        Returns:
            list: A list of dictionaries containing the data for each row in the table.
        """
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]  # Extract headers
        data = []

        for row in range(self.table.rowCount()):  # Loop through each row
            row_data = {headers[col]: self.table.item(row, col).text() if self.table.item(row, col) else "" 
                        for col in range(self.table.columnCount())}  # Extract cell data
            data.append(row_data)  # Add row data to the list

        return data

    def filter_data(self, data):
        """
        Filter out irrelevant values from the extracted data (e.g., empty values, non-relevant keys).

        Args:
            data (list): A list of dictionaries containing the extracted data.

        Returns:
            list: A list of filtered dictionaries.
        """
        def filter_row(row_data):
            return {key: value for key, value in row_data.items() if value not in ['', None, 'R/L', 'PD', 'SG']}

        return [filter_row(row) for row in data]  # Filter out unnecessary values

    def validate_cyl_and_ax(self, data):
        """
        Validate that the CYL and AX values are not missing for any row.

        Args:
            data (list): A list of dictionaries containing the extracted data.

        Returns:
            bool: True if CYL and AX are valid for all rows, False if any row has missing data.
        """
        for row in data:
            if not self.eye_test_validator.cheek_cyl_ax_not_null(row):  # Check if CYL or AX is missing
                QMessageBox.warning(self, f"Error", "CYL or AX is missing for one or both eyes in a row {row}.")
                return False  # Stop if validation fails
        
        return True  # If all rows are valid, continue

    def check_valida_eye_test_power(self, data):
        """
        Format the eye test data to ensure the values are correct.
        
        Args:
            data (list): List of dictionaries containing eye test data.
            
        Returns:
            list: A new list of formatted data dictionaries.
        """
        formatted_data = []
        for row in data:
            if 'SPH' in row:
                formatted_row = {**row, 'SPH': self.eye_test_validator.is_valida_eye_test_power(row['SPH'])}
            else:
                formatted_row = {**row, 'SPH': ''}  # Or set a default value if SPH is missing
            
            if 'CY' in row:
                formatted_row['CY'] = self.eye_test_validator.is_valida_eye_test_power(row['CY'])
            else:
                formatted_row['CY'] = ''  # Or set a default value if CY is missing
            
            formatted_data.append(formatted_row)  # Add formatted row to the data list
        
        return formatted_data  # Return the formatted data

    def update_table_with_data(self, formatted_data):
        """
        Update the main table with the formatted eye test data.

        Args:
            formatted_data (list): A list of formatted dictionaries containing the eye test data.
        """
        for row_idx, row_data in enumerate(formatted_data):  # Loop through the formatted data
            for col_idx, header in enumerate(self.header):  # Loop through each column
                cell_value = row_data.get(header, '')  # Get the cell value
                
                if cell_value:
                    current_item = self.table.item(row_idx, col_idx)
                    if current_item is None or current_item.text() != str(cell_value):  # Update if value has changed
                        item = QTableWidgetItem(str(cell_value))  # Create a new item with the updated value
                        self.table.setItem(row_idx, col_idx, item)  # Set the updated item in the table
                        item.setBackground(QColor(200, 255, 200))  # Green background for valid values

    def eye_test_power_format(self, data):
        """
        Format and adjust the SPH, CYL, and AX values for a list of eye test data.

        Args:
            data (list): A list of dictionaries where each dictionary represents an eye test row.
            
        Returns:
            list: A list of dictionaries with formatted SPH, CYL, and AX values.
        """
        formatted_data = []
        
        for row in data:
            formatted_row = self.eye_test_validator.power_format(row)  # Apply the formatting to the row
            formatted_data.append(formatted_row)  # Add the formatted row to the result list

        return formatted_data  # Return the list of formatted data

    def process_lens_data(self, filtered_data):
        """
        Convert the filtered eye test data into contact lens power (Spheric and Toric).

        Args:
            filtered_data (list): A list of dictionaries containing the filtered eye test data.

        Returns:
            list: A list of dictionaries containing the processed lens data (Spheric and Toric).
        """
        r_spher = self.contact_lens_validator.convert_to_spheric(filtered_data[0])  # Convert right eye data to spheric
        l_spher = self.contact_lens_validator.convert_to_spheric(filtered_data[1])  # Convert left eye data to spheric

        r_toric = self.contact_lens_validator.convert_to_toric(filtered_data[0])  # Convert right eye data to toric
        l_toric = self.contact_lens_validator.convert_to_toric(filtered_data[1])  # Convert left eye data to toric

        return [
            {**r_spher, 'R/L': 'R'}, {**l_spher, 'R/L': 'L'}, 
            {**r_toric, 'R/L': 'R'}, {**l_toric, 'R/L': 'L'}
        ]  # Return the processed lens data for both eyes

    def update_result_table(self, lens_data):
        """
        Update the result table with the processed lens data.
        """
        # Clear the result table before adding new data
        self.result_table.setRowCount(0)

        # عناوين الرأس العمودي
        self.verticalHEader = ["", "R", "L", "", "R", "L"]

        # Add "Spheric" row with custom styling and spanning across columns
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        spheric_item = QTableWidgetItem()
        self.apply_cell_style(spheric_item, "Spheric", QColor(173, 216, 230))  # Light blue background for Spheric
        self.result_table.setItem(row_position, 0, spheric_item)
        self.result_table.setSpan(row_position, 0, 1, len(self.result_header))  # Span across columns

                # Variable to count rows for when to add "Toric" row
        row_count = 0

        # Iterate over each row in lens_data and insert it into the result table
        for row_data in lens_data:
            row_idx = self.result_table.rowCount()  # Get the current row index
            self.result_table.insertRow(row_idx)  # Add a new row to the table

            # Insert data into each column of the result table
            for col_idx, header in enumerate(self.result_header):
                cell_value = row_data.get(header, '')  # Get the value for the header from row_data
                item = QTableWidgetItem(str(cell_value))
                self.result_table.setItem(row_idx, col_idx, item)

                # Apply custom styling based on the header and cell value
                if header == "Exact SPH" or header == "Exact CY":
                    item.setBackground(QColor(255, 255, 100))  # Yellow background for Exact SPH and Exact CY
                elif cell_value:
                    item.setBackground(QColor(200, 255, 200))  # Green background for valid values
                else:
                    item.setBackground(QColor(255, 200, 200))  # Red background for empty cells
            row_count += 1

            # After adding the first two rows of data, add a "Toric" row
            if row_count == 2:
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)

                # Apply styling for "Toric" row
                Toric_item = QTableWidgetItem()
                self.apply_cell_style(Toric_item, "Toric", QColor(173, 216, 230))  # Light yellow background for Toric
                self.result_table.setItem(row_position, 0, Toric_item)
                self.result_table.setSpan(row_position, 0, 1, len(self.result_header))  # Span across columns

        # تحديث عناوين الرأس العمودي
        self.result_table.setVerticalHeaderLabels(self.verticalHEader)

    def apply_cell_style(self, item, text, background_color=QColor(173, 216, 230), font_size=14, font_bold=True):
        """
        Helper function to apply style to a table cell.

        This function applies the following styles to the QTableWidgetItem:
        - Text alignment: Center
        - Font: Arial, font size, bold or normal
        - Background color: Customizable
        
        Args:
            item (QTableWidgetItem): The table item to which the style will be applied.
            text (str): The text to display in the cell.
            background_color (QColor): The background color to set for the cell (default: light blue).
            font_size (int): The font size to use (default: 14).
            font_bold (bool): Whether the font should be bold (default: True).

        Returns:
            QTableWidgetItem: The styled table item.
        """
        item.setText(text)
        item.setTextAlignment(Qt.AlignCenter)
        
        # Set the font size and weight
        font = QFont("Arial", font_size, QFont.Bold if font_bold else QFont.Normal)
        item.setFont(font)
        
        # Set the background color
        item.setBackground(background_color)
        
        return item

    def on_cell_change(self, row, col):
        """
        Handler for when a cell in the table is changed.

        This function checks the validity of the entered data, formats it accordingly, 
        and updates the cell's background color. If the value is valid, it may 
        trigger an update to a cell in the next row (for certain columns).
        If an error is detected, the cell is highlighted in red and focused.

        Args:
            row (int): The row index of the changed cell.
            col (int): The column index of the changed cell.
        """
        item = self.table.item(row, col)  # Get the table item at the specified row and column.
        
        if item and item.text():  # Check if the cell contains any text.
            # Validate the cell and get the result along with any necessary formatted value and nextCell flag.
            is_valid, formatted_value, nextCell = self.validate_cell(row, col, item.text())
            
            if is_valid:
                item.setText(formatted_value)  # Update the cell with the formatted value.
                item.setBackground(QColor(100, 200, 150))  # Set green background for valid value.
                
                # If nextCell flag is True, update the next row's corresponding cell.
                if nextCell:
                    add_l = QTableWidgetItem(str(formatted_value))  # Ensure value is a string.
                    self.table.setItem(row + 1, col, add_l)  # Set the value in the next row.
                    item.setBackground(QColor(100, 200, 150))  # Ensure green background for the valid cell.
            else:
                item.setBackground(QColor(255, 0, 0))  # Set red background for invalid value.
                item.setText("")  # Clear the cell if the value is invalid.
                # Focus on the invalid cell
                self.table.setCurrentCell(row, col)  # Set focus to the cell with the error.
        else:
            # If the cell is empty, set a red background to indicate an issue.
            item.setBackground(QColor(255, 0, 0))  # Red background for empty or invalid value.
            self.table.setCurrentCell(row-1, col)  # Focus on the empty cell for the user to correct it.

    def validate_cell(self, row, col, value):
        """
        Validate the value entered in a specific table cell based on its column.

        This method checks if the entered value is valid according to the rules of each column 
        (e.g., valid numbers, specific formats, or value ranges). The method also returns whether 
        the cell should trigger an update to the next row.

        Args:
            row (int): The row index of the changed cell.
            col (int): The column index of the changed cell.
            value (str): The value entered in the cell.

        Returns:
            bool: Whether the value is valid.
            str: The formatted value to be set in the cell.
            bool: A flag indicating whether the next cell in the row should be updated.
        """
        # Validate columns 1 (SPH) and 2 (CY) which accept formatted numbers.
        if col in [0,1]:
            formatted_value = self.eye_test_validator.is_valida_eye_test_power(value)
            return bool(formatted_value), formatted_value, False
        
        # Validate column 3 (AXIS) for correct axis values.
        elif col == 2:
            if self.eye_test_validator.check_axis(value):
                return True, self.eye_test_validator.remove_sign_axs(value), False
        
        # Validate column 4 (ADD) for specific number formatting and range checking.
        elif col == 3:
            formatted_value = self.eye_test_validator.is_valida_eye_test_power(value)
            if self.eye_test_validator.check_add(value):
                return True, formatted_value, True
        
        # Validate column 5 (PD) to ensure it is a valid PD value.
        elif col == 4:
            if self.eye_test_validator.check_pd(value):
                value = float(value) / 2 if float(value) > 40 else value  # Adjust value if needed.
                value = self.eye_test_validator.remove_sign(value)  # Remove any sign if applicable.
                return self.eye_test_validator.check_pd(value), value, True
        
        # Validate column 6 (SG) for a valid SG value.
        elif col == 5:
            return self.eye_test_validator.check_SG(value), value, True
        
        # Validate column 7 (Vertex Distance) for a valid range (typically between 10 and 14).
        elif col == 6:
            if  self.eye_test_validator.Check_vertex_distance(value):
                return self.eye_test_validator.Check_vertex_distance(value), value, True
            else:
                QMessageBox.warning(self, "Error", "The value must be a positive number between 10 and 14 (inclusive). Default is used.")
                return False, value, False

        # Return False if none of the above conditions were met.
        return False, value, False

    def update_resualt_data_power_format(self, filtered_data, formatted_data):
        """
        Updates the values in the filtered_data list to match the corresponding values from formatted_data.
        
        This method compares each item in `filtered_data` with the corresponding item in `formatted_data`.
        If a matching key exists in both dictionaries, the value in `filtered_data` will be updated with 
        the value from `formatted_data`. This ensures that `filtered_data` reflects the correct values 
        for the keys present in `formatted_data`.

        Args:
            filtered_data (list of dict): The list of dictionaries that contains the filtered data to be updated.
            formatted_data (list of dict): The list of dictionaries that contains the correctly formatted data.

        Returns:
            list of dict: The updated `filtered_data` list with values that match those in `formatted_data`.
            
        Example:
            filtered_data = [{'SPH': '+04.00', 'CY': '-02.00', 'AX': '91', 'ADD': '+02.00', 'PD': '25.00', 'SG': '18', 'BV': '11'}]
            formatted_data = [{'SPH': '+04.00', 'CY': '-02.00', 'AX': '91'}]
            updated_data = update_resualt_data_power_format(filtered_data, formatted_data)
            
            # The `filtered_data` will now have the values updated from `formatted_data` where the keys match.
        """
        # Loop through each entry in filtered_data
        for i, item in enumerate(filtered_data):
            # Check the corresponding item in formatted_data
            formatted_item = formatted_data[i]
            
            # Loop through each key in formatted_item and update the value in filtered_data
            for key, value in formatted_item.items():
                if key in item:
                    item[key] = value  # Update the value in filtered_data with the value from formatted_data
                    
        return filtered_data


    def create_footer(self):
            footer = QFrame()
            footer_layout = QHBoxLayout()
            footer.setObjectName('footer')
            footer_layout.addWidget(QLabel("Version 1.0 | Developed by Elhussein Taha"))
            footer.setLayout(footer_layout)
            return footer
    
