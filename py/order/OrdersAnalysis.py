from PyQt5.QtCore import QDate, QLocale, Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from dataBase.database import OrderModel, UserDatabase
from datetime import datetime
from collections import Counter
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QDateEdit, QGridLayout, QGroupBox, QLineEdit, QScrollArea, QTableWidget, QSizePolicy, QSplitter
)
from py.form import DynamicForm, DynamicTableButtons

from py.functian import get_credentials_user_id_qsettings, show_auto_close_messagebox


class OrdersAnalysisApp(QMainWindow):
    def __init__(self):
        """
        Initialize the main window and set up the UI.
        """
        super().__init__()
        self.setWindowTitle("Orders Analysis")
        self.setGeometry(100, 100, 1200, 800)
        try:
            self.setup_locale()
            self.setup_database()
            self.init_ui()
        except Exception as e:
            self.log_error("Initialization Error", e)
            print(f"Error: {e}")
 
    def setup_locale(self):
        """Set the application locale to English."""
        english_locale = QLocale(QLocale.English, QLocale.UnitedStates)
        QLocale.setDefault(english_locale)

    def setup_database(self):
        """Initialize database connections and fetch initial data."""
        try:
            self.db_order = OrderModel()
            self.db_users = UserDatabase()
            self.dynamic_buttons_or_tables=DynamicTableButtons()
            self.filter_data = self.filter_data_per_user()
            self.order_data = self.db_order.fetch_orders(filters=self.filter_data)

            # Extract unique values for filters
            self.unique_status = {entry['status'] for entry in self.order_data}
            self.unique_user = {entry['user'] for entry in self.order_data}
            self.unique_branch = {entry['branch'] for entry in self.order_data}
        except Exception as e:
            self.log_error("Database Setup Error", e)
    
    def filter_data_per_user(self):
        """
        Filter data based on the logged-in user's permissions.
        Returns:
            dict: Filter conditions based on user type.
        """
        try:
            self.user_id = get_credentials_user_id_qsettings()
            if self.user_id:
                self.userData = self.db_users.get_user_by_id(self.user_id)

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
        except Exception as e:
            self.log_error("User Filtering Error", e)
            return {}

    def init_ui(self):
        """
        Initialize the main user interface.
        """
        try:
            # Create a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # Create a container widget for the scroll area
            container = QWidget()
            main_layout = QVBoxLayout(container)

            # Add filters, summary, and charts/table to the main layout
            self.init_filters(main_layout)
            self.init_summary(main_layout)
            self.init_charts_and_table(main_layout)

            # Set the container widget to the scroll area
            scroll_area.setWidget(container)

            # Set the scroll area as the central widget
            self.setCentralWidget(scroll_area)
        except Exception as e:
            self.log_error("UI Initialization Error", e)

    def init_filters(self, parent_layout):
        """
        Initialize the filters section.
        """
        filters_layout = QGridLayout()

        # Define filters and their configurations
        self.filters = {
            "Date From": {"type": QDateEdit, "format": "yyyy-MM-dd"},
            "Date To": {"type": QDateEdit, "format": "yyyy-MM-dd"},
            "Branch": {"type": QComboBox, "items": ["All Branches"] + list(self.unique_branch)},
            "Status": {"type": QComboBox, "items": ["All Status"] + list(self.unique_status)},
            "Users": {"type": QComboBox, "items": ["All Users"] + list(self.unique_user)},
            "New": {"type": QComboBox,"items": [""]},

        }

        # Dynamically create filter widgets
        self.filter_widgets = {}
        for i, (label, config) in enumerate(self.filters.items()):
            filters_layout.addWidget(QLabel(label), i // 2, (i % 2) * 2)
            widget = self.create_filter_widget(config)
            self.filter_widgets[label] = widget
            filters_layout.addWidget(widget, i // 2, (i % 2) * 2 + 1)

        # Apply Filters Button
        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.apply_filters)
        # filters_layout.addWidget(self.apply_button, len(self.filters) // 2, (len(self.filters) % 2) * 2, 1, 2)
        filters_layout.addWidget(self.apply_button, len(self.filters) // 2, 3, 1, 1)

        # Add filters layout to the parent layout
        parent_layout.addLayout(filters_layout)

    def create_filter_widget(self, config):
        """
        Create a filter widget based on the given configuration.
        """
        if config["type"] == QComboBox:
            widget = config["type"]()
            widget.addItems(config["items"])
        elif config["type"] == QDateEdit:
            widget = config["type"]()
            widget.setCalendarPopup(True)
            widget.setDisplayFormat(config["format"])
            widget.setDate(QDate.currentDate())
            widget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        return widget
    
    def init_summary(self, parent_layout):
        """
        Initialize the summary section.
        """
        self.summary_layout = QGridLayout()

        # Summary Labels
        self.total_orders_label = QLabel("Total Orders: 0")
        self.total_branches_label = QLabel("Total Branches: 0")
        self.total_users_label = QLabel("Total Users: 0")
        self.delayed_orders_label = QLabel("Delayed Orders: 0")
        self.same_day_updates_label = QLabel("Same Day Updates: 0")

        self.summary_layout.addWidget(self.total_orders_label, 0, 0)
        self.summary_layout.addWidget(self.total_branches_label, 0, 1)
        self.summary_layout.addWidget(self.total_users_label, 0, 3)
        self.summary_layout.addWidget(self.delayed_orders_label, 1, 0)
        self.summary_layout.addWidget(self.same_day_updates_label, 1, 1)

        # Add status counts to summary
        self.status_labels = {}
        for i, status in enumerate(self.unique_status):
            self.status_labels[status] = QLabel(f"{status}: 0")
            self.summary_layout.addWidget(self.status_labels[status], 3 + i // 2, i % 2)

        # Add summary layout to the parent layout
        parent_layout.addLayout(self.summary_layout)

    def init_charts_and_table(self, parent_layout):
        """
        Initialize the charts and table section.
        """
        # Chart Widgets
        self.status_chart_view = QChartView()
        self.branch_chart_view = QChartView()

        # Set minimum size for charts
        self.status_chart_view.setMinimumSize(400, 300)
        self.branch_chart_view.setMinimumSize(400, 300)

        # Make charts expandable
        self.status_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.branch_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a group box for status chart and values
        status_group = self.create_chart_group("Order Status Distribution", self.status_chart_view, self.status_labels)

        # Create a group box for branch chart and values
        self.branch_group = QGroupBox("Order Distribution by Branch")
        self.branch_layout = QHBoxLayout()  # Initialize branch_layout
        self.branch_layout.addWidget(self.branch_chart_view)
        self.branch_values_layout = QVBoxLayout()  # Initialize branch_values_layout
        self.branch_layout.addLayout(self.branch_values_layout)
        self.branch_group.setLayout(self.branch_layout)

        # Order Table
        self.table = QTableWidget(self)
        self.table.setObjectName('OrderTable')
        self.table.setMinimumHeight(300)

        # Create a group box for the table
        table_group = QGroupBox("Orders Table")
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        # Use QSplitter to divide the space between charts and table
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.create_charts_widget(status_group, self.branch_group))
        splitter.addWidget(table_group)

        # Add splitter to the parent layout
        parent_layout.addWidget(splitter)

    def create_chart_group(self, title, chart_view, labels=None):
        """
        Create a group box for a chart and its associated labels.
        """
        group = QGroupBox(title)
        layout = QHBoxLayout()
        layout.addWidget(chart_view)
        if labels:
            values_layout = QVBoxLayout()
            for label in labels.values():
                values_layout.addWidget(label)
            layout.addLayout(values_layout)
        group.setLayout(layout)
        return group

    def create_charts_widget(self, status_group, branch_group):
        """
        Create a widget containing the charts.
        """
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        charts_layout.addWidget(status_group)
        charts_layout.addWidget(branch_group)
        return charts_widget

    def apply_filters(self):
        """
        Apply filters to the data and update the UI.
        """
        # Read filter values
        selected_users = self.filter_widgets["Users"].currentText()
        selected_branch = self.filter_widgets["Branch"].currentText()
        selected_status = self.filter_widgets["Status"].currentText()
        date_from = datetime.combine(self.filter_widgets["Date From"].date().toPyDate(), datetime.min.time())
        date_to = datetime.combine(self.filter_widgets["Date To"].date().toPyDate(), datetime.max.time())

        user_filter= self.filter_data_per_user()
        filtered_data = self.db_order.fetch_orders(user_filter)

        # Apply filters
        if selected_users != "All Users":
            filtered_data = [entry for entry in filtered_data if entry['user'] == selected_users]

        if selected_branch != "All Branches":
            filtered_data = [entry for entry in filtered_data if entry['branch'] == selected_branch]

        if selected_status != "All Status":
            filtered_data = [entry for entry in filtered_data if entry['status'] == selected_status]

        filtered_data = [
            entry for entry in filtered_data
            if date_from <= datetime.strptime(entry['date_send'].split(" ")[0], "%Y-%m-%d") <= date_to
        ]

        # Calculate delayed orders
        delayed_orders = [
            entry for entry in filtered_data
            if entry['updated_at'] and
            (datetime.strptime(entry['updated_at'].split(" ")[0], "%Y-%m-%d") - datetime.strptime(entry['date_send'].split(" ")[0], "%Y-%m-%d")).days > 1
        ]

        # Calculate same-day updates
        same_day_updates = [
            entry for entry in filtered_data
            if entry['updated_at'] and entry['date_send'][:10] == entry['updated_at'][:10]
        ]

        # Update summary, status counts, branch counts, and charts
        self.update_summary(filtered_data, delayed_orders, same_day_updates)
        self.dynamic_buttons_or_tables.populate_table(self.table, filtered_data)
        self.update_status_counts(filtered_data)
        self.update_branch_counts(filtered_data)
        self.update_charts(filtered_data)

    def update_summary(self, filtered_data, delayed_orders, same_day_updates):
        """
        Update the summary labels.
        Args:
            filtered_data (list): Filtered data based on applied filters.
            delayed_orders (list): List of delayed orders.
            same_day_updates (list): List of orders updated on the same day.
        """
        self.total_orders_label.setText(f"Total Orders: {len(filtered_data)}")
        self.total_branches_label.setText(f"Total Branches: {len(set(entry['branch'] for entry in filtered_data))}")
        self.total_users_label.setText(f"Total Users: {len(set(entry['user'] for entry in filtered_data))}")
        self.delayed_orders_label.setText(f"Delayed Orders: {len(delayed_orders)}")
        self.same_day_updates_label.setText(f"Same Day Updates: {len(same_day_updates)}")
    

    def update_status_counts(self, filtered_data):
        """
        Update the status counts to display the percentage of each status.
        Args:
            filtered_data (list): Filtered data based on applied filters.
        """
        # Calculate the count of each status
        status_counts = Counter(entry['status'] for entry in filtered_data)
        
        # Calculate the total number of orders
        total_orders = len(filtered_data)
        
        # Update the labels to show the percentage of each status
        for status, label in self.status_labels.items():
            if total_orders > 0:
                percentage = (status_counts.get(status, 0) / total_orders) * 100
                label.setText(f"{status} : {status_counts.get(status, 0)}  ({percentage:.2f}%) ")  # Display percentage with 2 decimal places
            else:
                label.setText(f"{status}: 0%")  # If there are no orders, show 0%          
    
    def update_branch_counts(self, filtered_data):
        """
        Update the branch counts to display the percentage of each branch.
        Args:
            filtered_data (list): Filtered data based on applied filters.
        """
        # Clear previous branch values
        for i in reversed(range(self.branch_values_layout.count())):
            self.branch_values_layout.itemAt(i).widget().setParent(None)

        # Calculate the total number of orders
        total_orders = len(filtered_data)

        # Update branch counts with percentages
        branch_counts = Counter(entry['branch'] for entry in filtered_data)
        for branch, count in branch_counts.items():
            if total_orders > 0:
                percentage = (count / total_orders) * 100
                self.branch_values_layout.addWidget(QLabel(f"{branch}: {count} ({percentage:.2f}%)"))
            else:
                self.branch_values_layout.addWidget(QLabel(f"{branch}: {count} (0%)"))
        
    def update_charts(self, filtered_data):
        """
        Update the charts.
        Args:
            filtered_data (list): Filtered data based on applied filters.
        """
        try:
            # Update status chart
            status_counts = Counter(entry['status'] for entry in filtered_data)
            status_series = QPieSeries()
            for status, count in status_counts.items():
                status_series.append(status, count)
            status_chart = QChart()
            status_chart.addSeries(status_series)
            status_chart.setTitle("Order Status Distribution")
            self.status_chart_view.setChart(status_chart)

            # Update branch chart
            branch_counts = Counter(entry['branch'] for entry in filtered_data)
            branch_series = QPieSeries()
            for branch, count in branch_counts.items():
                branch_series.append(branch, count)
            branch_chart = QChart()
            branch_chart.addSeries(branch_series)
            branch_chart.setTitle("Order Distribution by Branch")
            self.branch_chart_view.setChart(branch_chart)
        except Exception as e:
            self.log_error("Filter Application Error", e)

    def log_error(self, context, error):
        """Log errors for debugging and display a user-friendly message."""
        print(f"{context}: {error}")
        show_auto_close_messagebox(self,"Error", f"An error occurred: {error}")