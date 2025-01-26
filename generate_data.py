import os
from faker import Faker

class GenerateData:
    def __init__(self, to_excel:bool, to_database:bool):
        self.fake = Faker()
        self.data_config = self.__load_data_config()
        print(self.data_config)
    

    def __load_data_config(self):
        try:
            path = os.getenv('CONFIG_JSON_PATH')
            with open(path) as file:
                return json.load(file)
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {path}')
        except json.JSONDecodeError as e:
            print(f'Erro ao decodificar o JSON: {e}')
        except Exception as e:
            print(f'Erro: {e}')
