import os
from mysql.connector import connect
from sqlalchemy import create_engine

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.engine = None

    def connect(self):
        try:
            print('')
            host = os.getenv('DATABASE_HOST')
            user = os.getenv('DATABASE_USER')
            password = os.getenv('DATABASE_PASSWORD')
            database = os.getenv('DATABASE_NAME')

            self.connection = connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

        except Exception as e:
            print(f'Erro ao conectar ao MySQL: {e}')

    def close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
        except Exception as e:
            print(f'Erro ao encerrar a conexão com o MySQL: {e}')

