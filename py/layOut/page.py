# page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Page(QWidget):
    """
    A reusable page component for PyQt5 applications. It consists of a title, content, 
    and a list of buttons with their respective callbacks.

    Attributes:
        title (str): The title of the page displayed at the top.
        content (str): The main content displayed below the title.
        button_texts (list of str): The text labels for the buttons.
        button_callbacks (list of callable): The callback functions triggered when buttons are clicked.
    """

    def __init__(self, title, content, button_texts, button_callbacks):
        """
        Initializes the Page widget with a title, content, and a dynamic list of buttons.

        Args:
            title (str): The title to display on the page.
            content (str): The content to display below the title.
            button_texts (list of str): List of button labels.
            button_callbacks (list of callable): List of functions to be called when each button is clicked.
        """
        super().__init__()
        
        # Create a vertical layout to arrange widgets
        layout = QVBoxLayout()
        
        # Add the title label
        self.label = QLabel(title)
        self.label.setObjectName('label')  # Assign a unique object name for styling
        layout.addWidget(self.label)
        
        # Add the content label
        self.content_label = QLabel(content)
        self.content_label.setObjectName('label')  # Assign a unique object name for styling
        layout.addWidget(self.content_label)

        # Dynamically add buttons based on the provided texts and callbacks
        for button_text, callback in zip(button_texts, button_callbacks):
            button = QPushButton(button_text)
            button.clicked.connect(callback)  # Connect the button to its corresponding callback
            layout.addWidget(button)
        
        # Set the layout for the Page widget
        self.setLayout(layout)
