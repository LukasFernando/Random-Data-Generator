from dotenv import load_dotenv
from data_generator import DataGenerator
from database_connection import DatabaseConnection

class Main:
    def __init__(self):
        print("Application started")
        print("Loading environment variables (.env)")
        load_dotenv()

    def start(self):
        dg = DataGenerator()
        dg.generate_data()
        dg.save_data()

if __name__ == "__main__":
    main = Main()
    main.start()














