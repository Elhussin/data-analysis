from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget, QApplication, QDialog
from PyQt5.QtCore import QSettings
from dataBase.database import UserDatabase
from py.auth.login import LoginDialog
from py.order.OrdersAnalysis import OrdersAnalysisApp
from py.admin.admin import AdminPanel
from py.layOut.layout import Layout
from py.user_panal import UserPanal
from py.date.DateConverter import DateConverterApp
from py.eyeTest.EyeContactLens import EyeContactLens
from py.order.Order import OrderManage
from py.priseList.priceList import PriseList
from py.messages.message import WhatsAppSenderApp
from py.functian import clean_all_caches,confirm_exit
import logging
import sys
class MainWindow(QMainWindow):
    """
    The main window for the application, managing user login and navigation
    between different pages and functionalities.
    """
    def __init__(self):
        super().__init__()
        # Initialize application icon and title
        
        # self.login_dialog = LoginDialog(self)  # Login dialog instance
        # self.login_dialog.show()
        self.db = UserDatabase()  # Database connection instance
        # Initialize the main user interface
        # if self.login_dialog.exec_() == QDialog.Accepted:

        #     self.init_ui() #تهيئة واجهة المستخدم الرئيسية
        # else:
        #     sys.exit()

        # Initialize the main user interface
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the main user interface, including layouts, headers, footers, 
        and stacked widget for managing pages.
        """
        self.settings = QSettings("MyCompany", "MyApp")
        


        # Create the application's main pages
        self.stacked_widget = self.create_stacked_widget()
        
        # Create header, footer, and sidebar
        self.create_header_footer_sidebar()
        
        layout = QVBoxLayout()  # Create vertical layout
        container = QWidget()  # Main application container
        container.setLayout(layout)  # Assign the layout to the container
        self.setCentralWidget(container)  # Set the container as the central widget
        
        layout.addWidget(self.header)
        layout.addLayout(self.main_layout)
        layout.addWidget(self.footer)

        # Center the window on the screen
        self.center_window()
        self.show()  # Display the main window
    
    def create_stacked_widget(self):
        """
        Create a QStackedWidget containing the application's main pages.

        Returns:
            QStackedWidget: The stacked widget containing all pages.
        """
        stacked_widget = QStackedWidget()  # Stacked widget for page navigation
        
        # Add pages to the stacked widget
        stacked_widget.addWidget(OrdersAnalysisApp())  # Search page
        stacked_widget.addWidget(AdminPanel())  # Admin panel
        stacked_widget.addWidget(UserPanal())  # User panel
        stacked_widget.addWidget(DateConverterApp())  # Date converter
        stacked_widget.addWidget(EyeContactLens())  # Contact lens calculator
        stacked_widget.addWidget(OrderManage())  
        stacked_widget.addWidget(PriseList())  
        stacked_widget.addWidget(WhatsAppSenderApp())
        # stacked_widget.addWidget(OrderManage(self))  # Contact lens calculator
        # تأخير إضافة OrderManage حتى يتم إنشاء sidebar
        self.order_manage_page = None  # Placeholder
        return stacked_widget

    def create_header_footer_sidebar(self):
        """
        Create the header, footer, and sidebar components of the main layout.
        """
        self.header = Layout.create_header(self)  # Header
        self.footer = Layout.create_footer(self)  # Footer
        self.sidebar = Layout.create_sidebar(self)  # Sidebar

        # Main layout combining sidebar and stacked widget
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stacked_widget)

    def toggle_sidebar(self):
        """
        Toggle the visibility of the sidebar.
        """
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def log_out(self):
        """
        Log out the user, clean the session, and prompt for re-login.
        """
        if self.settings.contains("user_id"):
            # Deactivate the active session in the database
            saved_user_id = self.settings.value("user_id", "")
            self.db.dec_active_session(saved_user_id)
            self.settings.clear()
        # Close the current session and clean the cache
            self.close()
        self.hide()

        self.coll_clean_all_cash()
        
        # Prompt the login dialog
        self.login_dialog = LoginDialog(self)
        if self.login_dialog.exec_() == QDialog.Accepted:
            self.init_ui()
        else:
            self.close()

    # Navigation methods to switch between pages
    def go_to_orders_analysis(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_admin_panal(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_user_panal(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_date_convert(self):
        self.stacked_widget.setCurrentIndex(3)

    def contact_lens_callculter(self):
        self.stacked_widget.setCurrentIndex(4)
    
    def go_to_order_panal(self):
        self.stacked_widget.setCurrentIndex(5)
    
    def go_to_price_list(self):
        self.stacked_widget.setCurrentIndex(6)
    
    def send_message_safely(self):
        self.stacked_widget.setCurrentIndex(7)

    def center_window(self):
        """
        Center the application window on the screen.
        """
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate center position
        center_x = (screen_width - self.width()) // 2
        center_y = (screen_height - self.height()) // 2

        self.move(center_x, center_y)
    
    def go_to_order_panal(self):
        if self.order_manage_page is None:
            self.order_manage_page = OrderManage(self)
            self.stacked_widget.addWidget(self.order_manage_page)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
    

    def coll_clean_all_cash(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

            # Root path of your project
        root_directory = "."

        # Call the function to clean all __pycache__ folders 1day=86400 
        deleted_folders = clean_all_caches(root_path=root_directory, folder_name="__pycache__", age_limit_seconds=0)

        if deleted_folders > 0:
            print(f"Successfully deleted {deleted_folders} folder(s).")
        else:
            print("No old cache folders found or an error occurred.")

    def closeEvent(self, event):
            event.accept()
        # if confirm_exit(self):
        #     event.accept()
        # else:
        #     event.ignore()
    
