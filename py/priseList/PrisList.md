
# Price List Management Application

This is a PyQt5-based desktop application for managing and filtering a price list stored in a SQLite database. The application allows users to filter data by company, brand, and specific columns, and displays the results in a table.

## Features

- **Dynamic Filters**: Filter data by company and brand.
- **Column-Based Search**: Search within specific columns or across all columns.
- **Real-Time Updates**: The table updates dynamically as filters are applied.
- **Database Integration**: Connects to a SQLite database to fetch and display data.
- **Custom Table Population**: Uses a custom `DynamicTableButtons` class to populate the table with data.

## Requirements

- Python 3.7 or higher
- PyQt5
- SQLite3

## Installation

### Clone the repository:

```bash
git clone https://github.com/your-username/price-list-management.git
cd price-list-management
```

### Install dependencies:

```bash
pip install PyQt5
```

### Set up the database:

- Ensure you have a SQLite database file (e.g., `database.db`) with a table named `lens_price`.
- The table should have the following columns:
  - `ID` (Primary Key)
  - `Code`
  - `Price`
  - `Lens_Index`
  - `Type`
  - `Coating`
  - `Order_Type`
  - `Brand`
  - `Company`

### Update the database connection:

- Modify the `dataBase/database.py` file to point to your SQLite database file.

## Usage

### Run the application:

```bash
python main.py
```

### Using the Application:

- **Company Filter**: Select a company from the dropdown to filter the data by company.
- **Brand Filter**: Select a brand from the dropdown to filter the data by brand.
- **Column Filter**: Select a column to search within a specific column or leave it as "Select Column" to search across all columns.
- **Search Box**: Enter a search term to filter the data dynamically.

## Code Structure

- `main.py`: The main script to run the application.
- `dataBase/database.py`: Handles the database connection and queries.
- `py/form.py`: Contains the `DynamicTableButtons` class for populating the table.
- `README.md`: This file.

## Example Data

The `lens_price` table should contain data in the following format:

| ID  | Code | Price | Lens_Index | Type  | Coating  | Order_Type | Brand  | Company    |
| --- | ---- | ----- | ---------- | ----- | -------- | ---------- | ------ | ---------- |
| 1   | 001  | 100   | 1.50       | TypeA | Coating1 | OrderType1 | BrandX | Company A  |
| 2   | 002  | 150   | 1.60       | TypeB | Coating2 | OrderType2 | BrandY | Company A  |
| 3   | 003  | 200   | 1.67       | TypeC | Coating3 | OrderType3 | BrandZ | Company B  |

## Screenshots

### Application Screenshot
Example screenshot of the application in action.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## How to Download the README.md File

1. Copy the content above into a text editor.
2. Save the file as `README.md`.
3. Place it in the root directory of your project.
