import os
from dotenv import load_dotenv


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
        self.database_log_filename = os.path.join(
            base_dir, os.environ.get("DB_LOG_NAME", "../databases/db_operations.log")
        )
        self.database_log_level_name = os.getenv("DB_LOG_LEVEL", "INFO").upper()

        self.alpaca_secret = os.environ.get("ALPACA_SECRET")
        self.alpaca_key = os.environ.get("ALPACA_KEY")

        self.trade_value_percent = os.environ.get("TRADE_VALUE_PERCENT")
        self.trade_value_cap = os.environ.get("TRADE_VALUE_CAP")

        # Connection configurations
        self.use_secure_connection = bool(
            int(os.environ.get("USE_SECURE_CONNECTION", 0))
        )
