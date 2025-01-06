from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
from py.messages.SafeWhatsAppSender import SafeWhatsAppSender  # استيراد الكلاس الذي قمت بإنشائه

class WhatsAppSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sender = SafeWhatsAppSender()  # Initialize the WhatsApp sender
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Phone number input
        self.phone_label = QLabel("Phone Number (with country code):")
        main_layout.addWidget(self.phone_label)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Example: +966123456789")
        self.phone_input.setText("+966")
        main_layout.addWidget(self.phone_input)

        # Message input
        self.message_label = QLabel("Message:")
        main_layout.addWidget(self.message_label)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your message here...")
        arbicMessag="""عميلنا العزيز،
                    نود إبلاغكم بأن
                      طلبكم  رقم: 
                        جاهز للتسليم.
                    شكرًا لاختياركم حسام للنظارات.
                    لأي استفسارات، يُرجى التواصل معنا.

                    مع أطيب التحيات،
                    فريق حسام للنظارات
                    
                Dear Valued Customer,
                We are pleased to inform you that your 
                order number: 
                is ready for delivery.
                Thank you for choosing Hossam Optics.
                For any inquiries, please feel free to contact us.

                Best regards,
                Hossam Optics Team """
        self.message_input.setText(arbicMessag)
        main_layout.addWidget(self.message_input)

        # Send button
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        main_layout.addWidget(self.send_button)

        # Set the main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def send_message(self):
        """Handle the send button click event."""
        phone_number = self.phone_input.text().strip()
        message = self.message_input.toPlainText().strip()

        # Validate inputs
        if not phone_number:
            QMessageBox.warning(self, "Error", "Please enter a phone number.")
            return
        if not message:
            QMessageBox.warning(self, "Error", "Please enter a message.")
            return

        try:
            # Send the message using the SafeWhatsAppSender class
            self.sender.send_message_safely(phone_number, message)
            QMessageBox.information(self, "Success", "Message sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send message: {str(e)}")

