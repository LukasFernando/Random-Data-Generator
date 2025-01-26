import os
import json
import random
import pandas as pd
from dotenv import load_dotenv
from generate_data import GenerateData
from datetime import datetime, timedelta
from database_connection import DatabaseConnection

class Main:
    def __init__(self, to_excel:bool=True, to_database:bool=False):
        load_dotenv()
        self.db = DatabaseConnection()
        self.db.connect()
        self.to_excel = to_excel
        self.to_database = to_database
        # self.data_config = self.__load_data_config()
        # print(self.data_config)

    def start(self):
        GenerateData(self.to_excel, self.to_database)

    def test(self):
        if self.db.connection.is_connected():        
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            print(f"Banco de dados ativo: {result[0]}")

            cursor.close()

        self.db.close()

    # def __load_data_config(self):
    #     try:
    #         path = os.getenv('CONFIG_JSON_PATH')
    #         with open(path) as file:
    #             return json.load(file)
    #     except FileNotFoundError:
    #         print(f'Arquivo não encontrado: {path}')
    #     except json.JSONDecodeError as e:
    #         print(f'Erro ao decodificar o JSON: {e}')
    #     except Exception as e:
    #         print(f'Erro: {e}')

if __name__ == "__main__":
    main = Main(to_database=True)
    main.start()
