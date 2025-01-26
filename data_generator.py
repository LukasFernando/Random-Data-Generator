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
        self.a = True

    def generate_data(self):
        for table_name in self.data_config.keys():
            entity_info = self.data_config[table_name]
            data_temp = {column_info['name']: [] for column_info in entity_info['columns']}
            
            for _ in range(entity_info['num-rows']):
                for column_info in entity_info['columns']:
                    data_temp[column_info['name']].append(self.__get_fake_value(column_info['type']))

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
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {path}')
        except json.JSONDecodeError as e:
            print(f'Erro ao decodificar o JSON: {e}')
        except Exception as e:
            print(f'Erro: {e}')

    def __get_fake_value(self, type:str):
        if type.startswith('foreign-key'):
            return random.randint(1, self.data_config[type.split(':')[1].strip()]['num-rows'])
        elif type == 'name':
            return self.fake.name()
        elif type == 'word':
            return self.fake.word()
        elif type == 'words':
            return self.fake.words()
        elif type == 'date':
            return self.fake.date_this_year()
        elif type == 'phone_number':
            return self.fake.phone_number()
        elif type == 'integer':
            return random.randint(0, 1000000000)
        elif type == 'double':
            return random.uniform(0, 1000000000)

    def __to_excel(self):
        print("Saving to Excel...")
        file_name = os.getenv('EXCEL_EXPORT_FILE')
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            for table_name in self.data.keys():
                df = self.data[table_name]
                df.to_excel(writer, sheet_name=table_name, index=False)
        
        print(f"Excel saved successfully! File name: {file_name}")

    def __to_database(self):
        print("Saving to the database...")
        print("Initializing connection to the database")
        db = DatabaseConnection()
        db.connect()
        print("Database connected successfully!")

        for table_name in self.data.keys():
            df = self.data[table_name]
            df.to_sql(table_name, con=db.engine, if_exists='append', index=False)
        
        print("Tables saved to the database successfully!")
        print("Closing connection to the database")
        db.close()
