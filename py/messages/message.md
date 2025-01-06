
# WhatsApp Message Sender

This is a PyQt5-based desktop application that allows you to send WhatsApp messages safely and efficiently. It uses the `pywhatkit` library to send messages and includes advanced features like session management, rate limiting, and error handling.

---

## Features

- **Send Single Messages**: Send a message to a specific phone number.
- **Safe Sending**: Includes intelligent delays and rate limiting to avoid being blocked by WhatsApp.
- **Session Management**: Tracks the number of messages sent per day and per session.
- **Error Handling**: Automatically handles errors like network issues or WhatsApp blocks.

---

## Requirements

- Python 3.7 or higher
- PyQt5
- pywhatkit
- SQLite3 (for session management, if needed)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/whatsapp-sender.git
   cd whatsapp-sender
   ```

2. **Install dependencies**:
   ```bash
   pip install PyQt5 pywhatkit
   ```

3. **Run the application**:
   ```bash
   python whatsapp_sender_app.py
   ```

---

## Usage

1. **Enter Phone Number**:  
   Enter the recipient's phone number in international format (e.g., +966123456789).

2. **Enter Message**:  
   Type your message in the message box.

3. **Send Message**:  
   Click the "Send Message" button to send the message.

---

## Code Structure

- `whatsapp_sender_app.py`: The main script that runs the PyQt5 application.
- `SafeWhatsAppSender.py`: Contains the `SafeWhatsAppSender` class for sending messages safely.
- `README.md`: This file.

---

## Example

### Sending a Single Message

1. Open the application.  
2. Enter the phone number: `+966123456789`.  
3. Enter the message: `Hello, this is a test message!`.  
4. Click "Send Message".

### Session Management

- The application tracks the number of messages sent per day and per session to avoid exceeding WhatsApp's limits.
- If the daily limit is reached, the application will stop sending messages until the next day.

### Error Handling

- If the message fails to send, the application will retry up to 3 times.
- If a potential block is detected, the application will wait for a few hours before retrying.

---

## Screenshots

### WhatsApp Sender App  
Screenshot of the WhatsApp Sender application.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/YourFeatureName`).  
3. Commit your changes (`git commit -m 'Add some feature'`).  
4. Push to the branch (`git push origin feature/YourFeatureName`).  
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Notes

- Ensure you are logged in to WhatsApp Web before using the application.
- The application uses `pywhatkit`, which relies on opening a browser window. Make sure Chrome is installed and set as the default browser.
- For advanced usage, consider using Selenium for more control over the browser.

---

## Support

If you encounter any issues, please open an issue on the GitHub repository.
