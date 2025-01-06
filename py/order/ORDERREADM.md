# Order Management System

## Overview

The **Order Management System** is a PyQt5-based desktop application for managing orders. It includes features such as adding, updating, deleting, and searching for orders, along with advanced filters and validation logic.

## Features

- **Order Management**:

  - Add, update, and delete orders.
  - Validate order numbers (length and format).

- **Search and Filter**:

  - Search orders by number.
  - Filter orders by status (e.g., "Send To Lab", "Delivery", "In Shop").

- **Dynamic UI**:

  - Dynamically update input fields and buttons based on user actions.
  - Add confirmation dialogs for critical actions like deleting or reverting status.

- **Database Integration**:

  - Supports retrieving, filtering, and modifying order data stored in a database.

## Code Structure

### Main Components

1. **`OrderManage`**** Class**:

   - Main GUI widget for managing orders.

2. **Database Models**:

   - `OrderModel`: Handles database interactions related to orders.
   - `BranchManagerDatabase`: Manages branch and user relationships.

3. **Utility Functions**:

   - `validate_order_number`: Validates order number format.
   - `construct_order_number`: Constructs complete order numbers based on branch ID and input.
   - `show_auto_close_messagebox`: Displays timed success/error messages.

### Key Methods

1. **`setup_search`**:

   - Adds search box and filter dropdown for filtering orders.

2. **`perform_search`**:

   - Fetches filtered orders based on user input and filter selection.

3. **`load_order_table`**:

   - Populates the table with order data from the database.

4. **`update_order_status`**:

   - Updates the status of an order with restrictions based on the current status.
   - Includes confirmation dialogs for critical changes.

5. **`delete_order_by_index`**:

   - Deletes an order based on its table row index with user confirmation.

## Installation

### Prerequisites

- Python 3.x
- PyQt5
- SQLite (or any supported database)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd order_management_system
   ```
2. Install required Python packages:
   ```bash
   pip install PyQt5
   ```
3. Ensure the database is configured and accessible.

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Use the search bar and filters to view orders.
3. Perform actions like adding, updating, or deleting orders using the provided buttons and input fields.

## Code Example

```python
# Example: Adding a new order
order_manage = OrderManage()
order_manage.send_order("1234")
```

## Future Enhancements

- Add multi-user authentication and role-based permissions.
- Export order data to Excel or CSV.
- Enhance the UI with additional filters and sorting options.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

