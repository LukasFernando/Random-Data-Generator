import os
import json
import random
import pandas as pd
from faker import Faker
from database_connection import DatabaseConnection

class DataGenerator:
    def __init__(self):
        print("Starting data generation")
        self.fake = Faker()
        self.data_config = self.__load_data_config()
        self.to_excel = eval(os.getenv('TO_EXCEL'))
        self.to_database = eval(os.getenv('TO_DATABASE'))
        self.data = {}

    def generate_data(self):
        for table_name, entity_info in self.data_config.items():
            data_temp = {column_info['name']: [] for column_info in entity_info['columns']}
            
            for row_count in range(1, entity_info['num-rows']+1):
                for column_info in entity_info['columns']:
                    data_temp[column_info['name']].append(self.__generate_fake_value(column_info, row_count))

            self.data[table_name] = pd.DataFrame(data_temp)

    def save_data(self):
        print("Saving data to the selected types: Excel and/or Database")
        if self.to_excel:
            self.__to_excel()
        if self.to_database:
            self.__to_database()
        print("Data saved successfully!")

    def __load_data_config(self):
        try:
            path = os.getenv('CONFIG_JSON_PATH')
            print(f"Loading the configuration file. File name: {path}")
            with open(path) as file:
                return json.load(file)
        except Exception as e:
            raise Exception(e)

    def __generate_fake_value(self, column_info, row_count):
        """
        # Generating a fake value based on column type (e.g., name, email, integer)
        """
        min_num = column_info.get('min', 0)
        max_num = column_info.get('max', 1000000000)
        round_num = column_info.get('round', 5)
        type = column_info['type']
        generated_type = 'string'
        value = None
    
        # Foreign key type
        if type == 'foreign-key':
            generated_type = 'foreign-key'
            value = random.randint(1, self.data_config[column_info['reference-table']]['num-rows'])
        # String type
        elif type == 'name':
            value = self.fake.name()
        elif type == 'username':
            value = self.fake.name().replace(' ', '.').strip()
        elif type == 'word':
            value = self.fake.word()
        elif type == 'words':
            value = self.fake.words()
        # Email type
        elif type == 'email':
            generated_type = 'email'
            value = self.fake.email()
        # Date type
        elif type == 'date':
            generated_type = 'date'
            value = self.fake.date_this_year()
        # Enum type
        elif type == 'enum':
            value = random.choice(column_info['enum'])
        # Numeric type
        elif type == 'integer':
            generated_type = 'numeric'
            value = random.randint(min_num, max_num)
        elif type == 'double':
            generated_type = 'numeric'
            value = round(random.uniform(min_num, max_num), round_num)
        
        return self.__apply_column_transformations(value, generated_type, column_info, row_count)

    def __apply_column_transformations(self, current_value, generated_type, column_info, row_count):
        """
        Transforming the value based on the specified options.
        """
        unique = column_info.get('unique', False)

        # Apply 'unique' transformations based on value type (string, email, numeric)
        if unique and generated_type == 'foreign-key':
            current_value = row_count
        elif unique and generated_type == 'string':
            current_value = current_value + str(row_count)
        elif unique and generated_type == 'email':
            email_split = current_value.split('@')
            current_value = f'{email_split[0]}{row_count}{email_split[1]}'
        elif unique and generated_type == 'numeric':
            number_length = column_info.get('number-length', 10)
            str_row_count = str(row_count)
            current_value = int(str_row_count.ljust(number_length - len(str_row_count), '0') + str_row_count)

        # Apply unique and string case transformations (upper, lower, title)
        if column_info.get('upper', False):
            current_value = current_value.upper()
        elif column_info.get('lower', False):
            current_value = current_value.lower()
        elif column_info.get('title', False):
            current_value = current_value.title()
        
        return current_value

    def __to_excel(self):
        """
        Save the Excel
        """
        print("Saving to Excel...")
        file_name = os.getenv('OUTPUT_EXCEL_FILE')
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            for table_name, df in self.data.items():
                df.to_excel(writer, sheet_name=table_name, index=False)
        
        print(f"Excel saved successfully! File name: {file_name}")

    def __to_database(self):
        """
        Save in database
        """
        print("Saving to the database...")
        print("Initializing connection to the database")
        db = DatabaseConnection()
        db.connect()
        print("Database connected successfully!")

        for table_name, df in self.data.items():
            df.to_sql(table_name, con=db.engine, if_exists='append', index=False)
        
        print("Tables saved to the database successfully!")
        print("Closing connection to the database")
        db.close()
