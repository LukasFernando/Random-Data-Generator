# Random-Data-Generator

## Project Structure

```
project
│
├── .env
├── .gitignore
├── data_generation_config.json
├── data_generator.py
├── database_connection.py
├── generate_excel.py
├── main.py
└── README.md
```

## Steps to Use This Project

### 1. Clone this repository
```bash
git clone <repository-url>
```

### 2. Create environment variables (.env file)
```env
# Database
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=root
DATABASE_NAME=test

# Files
CONFIG_JSON_PATH=data_generation_config.json
OUTPUT_EXCEL_FILE=data.xlsx

# App
TO_EXCEL=True
TO_DATABASE=False
IF_TABLE_EXISTS=append
```

### Explanation of Variables

#### Database
- These are the database connection details. If you do not plan to save data to a database, you can skip these configurations.

#### Files
- `CONFIG_JSON_PATH`: The path to the JSON file containing the table configuration for data generation. An example structure of this file is provided below.

#### App
- `TO_EXCEL`: Specifies if the generated data should be saved to an Excel file (`True` or `False`).
- `TO_DATABASE`: Specifies if the generated data should be inserted into the database (`True` or `False`).
- `IF_TABLE_EXISTS`: Defines the behavior when the table already exists (`append`, `replace`, or `fail`).

### Example of `data_generation_config.json`
```json
{
    "table_name": {
        "columns": [
            {
                "name": "column name",
                "type": "column type (Note: This refers to data types provided by the Faker library, not SQL types like string, date, etc.)"
            }
        ],
        "num-rows": "number of rows to generate for this table"
    }
}
```

#### Sample Configuration
```json
{
    "company": {
        "columns": [
            {
                "name": "name",
                "type": "word"
            },
            {
                "name": "slogan",
                "type": "word"
            }
        ],
        "num-rows": 2
    },
    "dim_employee": {
        "columns": [
            {
                "name": "company_id",
                "type": "foreign-key",
                "reference-table": "company"
            },
            {
                "name": "name",
                "type": "name",
                "upper": true
            },
            {
                "name": "status",
                "type": "enum",
                "enum": ["ACTIVE", "INACTIVE"]
            }
        ],
        "num-rows": 5
    },
    "product": {
        "columns": [
            {
                "name": "company_id",
                "type": "foreign-key",
                "reference-table": "company"
            },
            {
                "name": "name",
                "type": "word",
                "upper": true
            },
            {
                "name": "category",
                "type": "enum",
                "enum": ["TECHNOLOGY", "HEALTH", "EDUCATION", "ENTERTAINMENT", "SPORTS"]
            },
            {
                "name": "value",
                "type": "double",
                "min": 10, 
                "max": 1000, 
                "round": 2 
            }
        ],
        "num-rows": 100
    }
}
```
#### Faker Library Data Types:
- **name:** Generates a random name.
- **word:** Generates a random word.
- **words:** Generates multiple random words.
- **email:** Generates a random email address.
- **date:** Generates a random date from this year (date_this_year).

#### Custom Data Types:
- **foreign-key:** Generates a foreign key, which will be a random number within the number of rows in the referenced table. Used when the table is linked to another.
- **integer:** Generates a random integer within a range defined by the min and max parameters.
- **double:** Generates a random floating-point number within the min and max range, with the possibility to round to a specific number of decimal places using the round parameter.
- **enum:** Generates a random value chosen from the values provided in the enum list.

#### Transformation Options:
These options allow you to modify the generated values:
- **unique (boolean):** Ensures that the generated value is unique within the table. This is available for string, number, email, and other types.
- **upper (boolean):** Converts the value to uppercase.
- **lower (boolean):** Converts the value to lowercase.
- **title (boolean):** Converts the value to title case (first letter capitalized).
- **min (integer):** Defines the minimum value for generating integers or floating-point numbers.
- **max (integer):** Defines the maximum value for generating integers or floating-point numbers.
- **round (integer):** Sets the number of decimal places to round generated double values.


### 3. Create and activate the virtual environment
#### Windows:
```bash
python -m venv .venv
```
```bash
.venv/Scripts/activate
```
#### Linux (or macOS):
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the project
```bash
python ./main.py
```

---

### Next Steps
- Customize the `data_generation_config.json` file as per your data generation needs.
- Explore the Faker library documentation to better understand how it works.
- If you added new data types in `data_generation_config.json`, you will need to modify the code where the conditions for each data type are handled. This part of the code is in the `data_generator.py` file, in the `__generate_fake_value` and `__apply_column_transformations` function.

For further clarification, refer to the comments and examples provided in this document.
