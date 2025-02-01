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
                "type": "name"
            },
            {
                "name": "slogan",
                "type": "word"
            }
        ],
        "num-rows": 2
    },
    "product": {
        "columns": [
            {
                "name": "company_id",
                "type": "foreign-key: company"
            },
            {
                "name": "name",
                "type": "word"
            },
            {
                "name": "category",
                "type": "word"
            },
            {
                "name": "value",
                "type": "double"
            }
        ],
        "num-rows": 100
    }
}
```

If you are unfamiliar with the Faker library, it is recommended to explore its documentation to understand the available data types.

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
- If you added new data types in `data_generation_config.json`, you will need to modify the code where the conditions for each data type are handled. This part of the code is in the `data_generator.py` file, in the `__get_fake_value` function.

For further clarification, refer to the comments and examples provided in this document.
