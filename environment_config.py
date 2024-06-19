import os
from dotenv import load_dotenv
from db.database_connection import SQLiteDatabaseConnection, PostgresDatabaseConnection

class EnvironmentConfig:
    def __init__(self):
        load_dotenv()  # Load environment variables from a .env file
        
        # Path configurations
        # Define the base directory relative to this file's location
        base_dir = os.path.dirname(__file__)

        # Database configurations
        self.host = os.environ.get("DB_HOST")
        self.data_table = os.environ.get("DATA_NAME", "data_table")
        self.passphrase = os.environ.get("DB_PASSPHRASE", "Passphrase")
        self.port = os.environ.get("DB_PORT")
        self.user = os.environ.get("DB_USER")

        # Debugging and performance configurations

        self.debug = int(os.environ.get("DEBUG", 1))
        self.database_log_filename=os.path.join(base_dir, os.environ.get("DB_LOG_NAME", "../databases/db_operations.log"))
        self.database_log_level_name = os.getenv('DB_LOG_LEVEL', 'INFO').upper()  

        self.alpaca_secret= os.environ.get("ALPACA_SECRET")
        self.alpaca_key = os.environ.get("ALPACA_KEY")


        # Connection configurations
        self.use_secure_connection = bool(int(os.environ.get('USE_SECURE_CONNECTION', 0)))
    def get_db_connection(self):
        # Decide which database connection to use based on the environment configuration
                return PostgresDatabaseConnection(host=self.host,database=self.data_table,passworddb=self.passphrase,port=self.port,user=self.user)
