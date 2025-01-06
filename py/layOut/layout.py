from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QSettings
from py.functian import get_credentials_user_id_qsettings
class Layout:
    """
    A class to create reusable GUI components for a PyQt5 application, including a header, footer, and sidebar.
    """
    
    def create_header(self):
        """
        Creates a header with buttons for navigation and functionalities.

        Returns:
            QFrame: The header frame containing buttons.
        """
        header = QFrame()
        header_layout = QHBoxLayout()
        header.setObjectName('header')  # Assign a unique name for styling purposes

        # Define button labels and their corresponding callback functions
        button_texts = [
            "Admin", "User","Order", "Orders Analysis","Price List", "Date Converter",
            "Calculator","Message", "Sidebar", "Log Out"
        ]
        button_callbacks = [
            self.go_to_admin_panal,
            self.go_to_user_panal,
            self.go_to_order_panal,
            self.go_to_orders_analysis,
            self.go_to_price_list,
            self.go_to_date_convert,
            self.contact_lens_callculter,
            self.send_message_safely,
            self.toggle_sidebar,
            self.log_out
        ]

        # Check user settings to determine user-specific configurations
        get_user_id = get_credentials_user_id_qsettings()

        user = self.db.get_user_by_id(get_user_id)  # Fetch user details from the database

        # Create buttons dynamically and apply permissions based on user type
        header_buttons = QHBoxLayout()
        for button_text, callback in zip(button_texts, button_callbacks):
            # Check if 'user_type' exists in user data
            if user:
                if 'user_type' in user:
                    # Show Admin button only if user_type is Admin
                    if button_text == "Admin" and user['user_type'] != "Admin":
                        continue  # Skip the Admin button for non-admin users
                    
                    # Show User button only if user_type is User
                    if button_text == "User" and user['user_type'] != "User":
                        continue  # Skip the User button for non-user accounts
                
            # Create the button and set its properties
            self.setCursor(QCursor(Qt.PointingHandCursor))  # Set the cursor to a pointing hand
            button = QPushButton(button_text)
            button.setDefault(True)  # Allow pressing the button using Enter key
            button.clicked.connect(callback)  # Connect the button to its callback
            header_buttons.addWidget(button)

        header_layout.addLayout(header_buttons)
        header.setLayout(header_layout)
        return header

    def create_footer(self):
        """
        Creates a footer with application version and developer details.

        Returns:
            QFrame: The footer frame containing information.
        """
        footer = QFrame()
        footer_layout = QHBoxLayout()
        footer.setObjectName('footer')  # Assign a unique name for styling purposes

        # Add footer content
        footer_layout.addWidget(QLabel("Version 1.0 | Developed by Elhussein Taha"))
        footer.setLayout(footer_layout)
        return footer

    def create_sidebar(self):
        """
        Creates a sidebar with a close button.

        Returns:
            QFrame: The sidebar frame containing navigation buttons.
        """
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')  # Assign a unique name for styling purposes

        sidebar_layout = QVBoxLayout()

        # Add a Close button to the sidebar
        # sidebar_layout.addWidget(QPushButton("Close", clicked=self.toggle_sidebar))

        sidebar.setLayout(sidebar_layout)
        sidebar_layout.setAlignment(Qt.AlignTop)
        return sidebar
