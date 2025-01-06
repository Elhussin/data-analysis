from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox,
    QLineEdit, QTableWidget, QHeaderView
)
from dataBase.database import PriceList  # Import the database connection class
from py.form import DynamicTableButtons  # Import custom table buttons functionality
from PyQt5.QtCore import QThread, pyqtSignal  # For threading (not used in this code)


class PriseList(QMainWindow):
    """
    A PyQt5-based main window for displaying and filtering a price list from a database.
    This class includes filters for company, brand, and column-based search functionality.
    """

    def __init__(self):
        """
        Initialize the PriceList window.
        Sets up the database connection, UI, and initial data fetching.
        """
        super().__init__()
        self.db_prise_list = PriceList()  # Initialize database connection
        self.creatTableOrbuttons = DynamicTableButtons()  # Initialize custom table buttons
        self.init_ui()  # Set up the user interface
        # Populate the table with initial data fetched from the database
        self.creatTableOrbuttons.populate_table(self.results_table, self.fetch_data())

    def fetch_data(self, query=None, params=()):
        """
        Fetch data from the database.

        :param query: Optional SQL query string. If not provided, a default query is used.
        :param params: Optional tuple of parameters for the SQL query.
        :return: A list of dictionaries representing the fetched data.
        """
        if query:
            return self.db_prise_list.fetch_all_data(query, params)
        else:
            # Default query to fetch all columns from the lens_price table
            query = """
            SELECT ID, Code, Price, Lens_Index, Type, Coating, Order_Type, Brand, Company
            FROM lens_price
            """
            return self.db_prise_list.fetch_all_data(query)

    def init_ui(self):
        """
        Initialize the user interface.
        Sets up filters, search functionality, and the results table.
        """
        main_widget = QWidget()  # Main widget to hold the layout
        main_layout = QVBoxLayout()  # Main vertical layout

        # Filters layout (grid layout for organizing filter components)
        filters_layout = QGridLayout()

        # Company filter
        self.company_label = QLabel("Company:")
        filters_layout.addWidget(self.company_label, 0, 0)

        self.company_filter = QComboBox()
        self.company_filter.addItem("Select Company")  # Default option
        companies = self.fetch_data("SELECT DISTINCT Company FROM lens_price")  # Fetch unique companies
        if companies:
            self.company_filter.addItems([c["Company"] for c in companies if c and "Company" in c])
        self.company_filter.currentTextChanged.connect(self.update_brands)  # Update brands when company changes
        filters_layout.addWidget(self.company_filter, 0, 1)

        # Brand filter
        self.brand_label = QLabel("Brand:")
        filters_layout.addWidget(self.brand_label, 0, 2)

        self.brand_filter = QComboBox()
        self.brand_filter.addItem("Select Brand")  # Default option
        filters_layout.addWidget(self.brand_filter, 0, 3)

        # Column selection filter
        self.column_label = QLabel("Search in Column:")
        filters_layout.addWidget(self.column_label, 0, 4)

        # List of columns to search in
        items = [
            "Select Column",
            "Code",
            "Price",
            "Lens Index",
            "Type",
            "Coating",
            "Order Type",
            "Brand",
            "Company"
        ]

        self.column_filter = QComboBox()
        self.column_filter.addItems(items)  # Add column options to the combo box
        filters_layout.addWidget(self.column_filter, 0, 5)

        # Search box
        self.search_label = QLabel("Search:")
        filters_layout.addWidget(self.search_label, 1, 0)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Start search term")
        self.search_box.textChanged.connect(self.perform_search)  # Perform search on text change
        filters_layout.addWidget(self.search_box, 1, 1, 1, 3)

        # Automatically search when company or column filter changes
        self.company_filter.currentIndexChanged.connect(self.perform_search)
        self.column_filter.currentIndexChanged.connect(self.perform_search)

        main_layout.addLayout(filters_layout)  # Add filters layout to the main layout

        # Results table
        self.results_table = QTableWidget()  # Table to display search results
        main_layout.addWidget(self.results_table)

        main_widget.setLayout(main_layout)  # Set the main layout for the widget
        self.setCentralWidget(main_widget)  # Set the main widget as the central widget

    def update_brands(self):
        """
        Update the brand filter based on the selected company.
        Fetches and displays brands associated with the selected company.
        """
        company = self.company_filter.currentText()
        if company == "Select Company":
            self.brand_filter.clear()
            self.brand_filter.addItem("Select Brand")
            return

        # Fetch brands for the selected company
        brands = self.fetch_data("SELECT DISTINCT Brand FROM lens_price WHERE Company = ?", (company,))
        self.brand_filter.clear()
        self.brand_filter.addItem("Select Brand")
        if brands:
            self.brand_filter.addItems([b["Brand"] for b in brands if b and "Brand" in b])

    def perform_search(self):
        """
        Perform the search based on selected filters and display results in the table.
        Filters data by company, brand, and search term (with optional column selection).
        """
        company = self.company_filter.currentText()
        brand = self.brand_filter.currentText()
        search_term = self.search_box.text()
        column = self.column_filter.currentText()

        # If no column selected, search in all columns
        if column == "Select Column":
            column = None
        else:
            column = column.replace(" ", "_")  # Replace spaces with underscores for SQL column names

        # Base query to fetch data
        query = """
            SELECT ID, Code, Price, Lens_Index, Type, Coating, Order_Type, Brand, Company
            FROM lens_price
        """
        params = []
        conditions = []

        # Add conditions dynamically based on selected filters
        if company != "Select Company":
            conditions.append("Company = ?")
            params.append(company)

        if brand != "Select Brand":
            conditions.append("Brand = ?")
            params.append(brand)

        if search_term:
            if column:  # If a column is selected
                conditions.append(f"{column} LIKE ?")
                params.append(f"%{search_term}%")
            else:  # If no column selected, search in all columns
                conditions.append("""
                    Code LIKE ? OR Price LIKE ? OR Lens_Index LIKE ? OR Type LIKE ? 
                    OR Coating LIKE ? OR Order_Type LIKE ? OR Brand LIKE ? OR Company LIKE ?
                """)
                params.extend([f"%{search_term}%"] * 8)  # Repeat for each column

        # Add conditions to the query dynamically
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Fetch filtered data as a list of dictionaries
        results = self.fetch_data(query, tuple(params))
        # Populate the table using the custom function
        self.creatTableOrbuttons.populate_table(self.results_table, results)