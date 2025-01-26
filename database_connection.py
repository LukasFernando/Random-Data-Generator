import os
from mysql.connector import connect

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = connect(
                host=os.getenv('DATABASE_HOST'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                database=os.getenv('DATABASE_NAME')
            )
        except Exception as e:
            print(f'Erro ao conectar ao MySQL: {e}')

    def close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
                print('Conexão com o MySQL foi encerrada.')
        except Exception as e:
            print(f'Erro ao encerrar a conexão com o MySQL: {e}')

