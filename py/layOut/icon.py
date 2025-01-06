from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class IconManager:
    """
    Manages the system tray icon for a PyQt5 application, allowing users to interact
    with the application through a tray menu.

    Attributes:
        app (QApplication): The main application instance.
        icon_path (str): The file path to the application's icon.
        app_name (str): The name of the application, used for the tooltip.
    """

    def __init__(self, app, icon_path, app_name="My App"):
        """
        Initializes the IconManager, setting up the tray icon and menu.

        Args:
            app (QApplication): The main application instance.
            icon_path (str): Path to the icon file.
            app_name (str): The name of the application.
        """
        self.app = app
        self.icon_path = icon_path
        self.app_name = app_name

        # Set the main application window icon
        self.app.setWindowIcon(QIcon(icon_path))

        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self.app.activeWindow())
        self.tray_icon.setToolTip(app_name)

        # Create the context menu for the tray icon
        self.tray_menu = QMenu()
        self._create_tray_menu()
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def _create_tray_menu(self):
        """
        Creates the context menu for the system tray icon with options like Open, Hide, and Exit.
        """
        # Add "Open" option to the menu
        open_action = QAction("Open")
        open_action.triggered.connect(self.open_main_window)
        self.tray_menu.addAction(open_action)

        # Add "Hide" option to the menu
        hide_action = QAction("Hide")
        hide_action.triggered.connect(self.hide_main_window)
        self.tray_menu.addAction(hide_action)

        # Add "Exit" option to the menu
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.exit_application)
        self.tray_menu.addAction(exit_action)

    def open_main_window(self):
        """
        Displays the main application window if it is currently hidden.
        """
        window = self.app.activeWindow()
        if window:
            window.show()

    def hide_main_window(self):
        """
        Hides the main application window.
        """
        window = self.app.activeWindow()
        if window:
            window.hide()

    def open_settings(self):
        """
        Placeholder for a function to display the settings window.
        Replace this with the actual implementation for opening the settings window.
        """
        pass

    def exit_application(self):
        """
        Exits the application gracefully.
        """
        QApplication.quit()

def set_default_title(app_name="APP"):
    """
    Sets a default title for the active window if no title is set.

    Args:
        app_name (str): The default title to set if none exists.
    """
    active_window = QApplication.activeWindow()
    if active_window and not active_window.windowTitle():  # If no title is set
        active_window.setWindowTitle(app_name)
