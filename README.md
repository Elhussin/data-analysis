#  Orders Analysis Desktop Application

## Overview
This project is a feature-rich desktop application developed using PyQt5. It integrates multiple functionalities, including price list management, order management, WhatsApp messaging, eye test validation, contact lens power calculation, and date conversion. The application offers a seamless and efficient user experience through an intuitive graphical interface.

---

## Folder Structure

- **dataBase**: Handles database connections and models.
- **py**: Contains modules for various functionalities:
  - **admin**: Administrative features.
  - **auth**: Authentication mechanisms.
  - **date**: Includes the Date Converter application.
  - **eyeTest**: Eye Test Validation and Contact Lens Power Calculation.
  - **layOut**: UI layouts.
  - **messages**: WhatsApp Message Sender.
  - **order**: Order Management System and Orders Analysis Application.
  - **priseList**: Price List Management Application.
- **static**: Stores media and style files for UI assets.

---

## Features

### 1. Price List Management
- Manage and filter price lists.
- Search and filter by company, brand, and specific columns.

### 2. Order Management System
- Add, update, and delete orders.
- Validate order numbers and manage order statuses.

### 3. Orders Analysis Application
- Analyze and visualize order data.
- Interactive charts and summary statistics.

### 4. WhatsApp Message Sender
- Send WhatsApp messages safely and efficiently.
- Includes session management and rate limiting.

### 5. Eye Test Validation and Contact Lens Power Calculation
- Validate eye test data.
- Convert prescriptions to contact lens specifications.

### 6. Date Converter
- Convert dates between Gregorian and Hijri calendars.
- Real-time display of today’s dates in both formats.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- PyQt5
- SQLite3
- Other dependencies as specified in `requirements.txt`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Elhussin/data-analysis.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Ensure a SQLite database file (e.g., `database.db`) is available.
   - Update database connection settings in `dataBase/database.py`.
4. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

### Price List Management
- Use the GUI to manage and filter price lists by company, brand, or columns.

### Order Management
- Add, update, or delete orders through the interface.

### Orders Analysis
- Apply filters to view and analyze order statistics with interactive charts.

### WhatsApp Message Sender
- Enter phone numbers and messages to send WhatsApp messages safely.

### Eye Test Validation
- Input eye test data for validation and conversion.

### Date Converter
- Convert dates between Gregorian and Hijri calendars using the UI.

---

## Development and Contribution

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---
## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) 

## Contact
For inquiries, please contact:
- **Elhussein Taha**
- 📧 Email: hasin3112@gmail.com

---

## Acknowledgments
- Developed by Elhussein Taha.
- Inspired by real-world needs for integrated desktop applications.
