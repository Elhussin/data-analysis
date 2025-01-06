# Orders Analysis Application

This is a PyQt5-based application designed to analyze and visualize order data. It provides a user-friendly interface to filter and display order statistics, including charts and a summary table.

---

## Features

1. **Dynamic Filters:**
   - Filter orders by **User**, **Branch**, **Status**, and **Date Range**.
   - Filters are dynamically populated based on the available data.

2. **Interactive Charts:**
   - **Order Status Distribution:** A pie chart showing the distribution of orders by status.
   - **Order Distribution by Branch:** A pie chart showing the distribution of orders by branch.

3. **Summary Table:**
   - Displays filtered orders in a table format.

4. **Summary Statistics:**
   - Total Orders
   - Total Branches
   - Total Users
   - Delayed Orders
   - Same-Day Updates

5. **Responsive Design:**
   - Uses `QScrollArea` and `QSplitter` to ensure the application works well on different screen sizes.

---

## Requirements

To run this application, you need the following:

- Python 3.7 or higher
- PyQt5
- PyQtChart (for charting functionality)
- A database connection (e.g., `OrderModel` and `UserDatabase`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/orders-analysis.git
   cd orders-analysis
    ```
    1. Install the required dependencies:
        ```bash 
            pip install PyQt5 PyQtChart    pip install PyQt5 PyQtChart
        ```
    2. Run the application:

        ```bash 
        python main.py
            ```
---
## Usage

1. **Apply Filters**:

    - Use the dropdown menus and date pickers to filter the data.

    - Click the Apply Filters button to update the results.

2. **View Charts**:

    - The Order Status Distribution and Order Distribution by Branch charts will update automatically based on the applied filters.

3. **View Summary Table**:

    - The table below the charts will display the filtered orders.

4. View Summary Statistics:

    - The summary section at the top of the application will show key statistics based on the filtered data.

## Code Structure

- **OrdersAnalysisApp Class**:

    - Main application class that initializes the UI and handles user interactions.

    - Methods:

        - **filter_data_per_user**: Filters data based on the logged-in user's permissions.

        - setup_database: Initializes the database connection and fetches data.

        - **init_ui**: Sets up the user interface.

        - **apply_filters**: Applies filters and updates the UI.

        - **update_summary**: Updates the summary statistics.

        - **update_status_counts**: Updates the status counts.

        - **update_branch_counts**: Updates the branch counts.

        - **update_charts**: Updates the charts.
- **main.py:**

    - Entry point of the application.

---
## Screenshots
   Orders Analysis Application


## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Create a new branch (git checkout -b feature/YourFeature).

3. Commit your changes (git commit -m 'Add some feature').

4. Push to the branch (git push origin feature/YourFeature).

5. Open a pull request.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.

---
## Contact
For questions or feedback, please contact:

- Your Name

- Email: your.email@example.com

- GitHub: your-github-profile

---
## Acknowledgments
- Thanks to the PyQt5 and PyQtChart communities for their excellent libraries.

- Inspired by real-world order analysis needs.
---