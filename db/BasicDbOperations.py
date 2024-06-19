import pandas as pd
import psycopg2

from db.database_connection import PostgresDatabaseConnection
class BasicDbOperations:
    def __init__(self, env_config):
        self.db_connection = env_config.get_db_connection()
        self.data_table = env_config.data_table
        self.debug = env_config.debug

    def create_database(self):

    # SQL to create the users table
        create_user_table_sql = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            session_data JSONB,
            role TEXT NOT NULL
        )
    '''
    
    # SQL to create the users table
        create_user_signals_sql = '''
        CREATE TABLE IF NOT EXISTS user_signals (
            id SERIAL PRIMARY KEY,
            username TEXT ,
            signal_name TEXT,
            formula TEXT,
            threshold REAL,
            invert BOOLEAN,
            graph_type VARCHAR(255),
            graph_details TEXT,
            widget_data JSONB,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    '''

    # Execute the SQL commands
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SET client_encoding TO 'utf8'")
            cursor.execute(create_user_table_sql)
            cursor.execute(create_user_signals_sql)
            self.db_connection.commit()
            cursor.close()
            print("Tables created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error creating tables:", error)
        finally:
            if self.db_connection:
                self.db_connection.close()

    @staticmethod
    def load_dataframe_from_sql(db_connection:PostgresDatabaseConnection, data_table, id=None):
        # Construct the basic SQL query
        query = f"SELECT * FROM {data_table}"

        # Modify the query if an ID is provided
        if id is not None:
            query += f" WHERE id = {id}"
        try:
            result = db_connection.execute(query, operation_type='query', debug=1, log=1)
            return result
        except Exception as e:
            # Log the error, handle it, or raise it again
            raise ValueError(f"An error occurred: {e}")
       
    def query_by_field(self, field_value, field_name="path", select_fields=None):
        """
        Executes a query to retrieve specified fields based on a match with the provided field_value in the field_name column.

        Args:
            field_value: The value to look for in the field_name column.
            field_name: The name of the column to query. Defaults to "path".
            select_fields: A list of field names to be returned by the query. If None, defaults to '*'.

        Returns:
            The result of the query execution.
        """
        # If no specific fields are requested, select all fields
        if select_fields is None:
            select_fields = '*'
        else:
            # Join the fields into a string separated by commas
            select_fields = ', '.join(select_fields)

        query = f"SELECT {select_fields} FROM {self.data_table} WHERE {field_name} = ?"
        result = self.db_connection.execute(query, (field_value,), operation_type='query', debug=self.debug, log=1)
        return result
    @staticmethod
    def user_query(db_connection:PostgresDatabaseConnection):
        """
        Executes a query to retrieve all data from table users
        Returns:
            The result of the query execution.
        """

        query = f"SELECT username, tv_user, tv_password FROM users"
        result = db_connection.execute(query, operation_type='query', debug=1,log=1)
        return result
    
    @staticmethod 
    def add_logs_query(db_connection:PostgresDatabaseConnection,time,buy_price,sell_price,stop_loss,stock):
        """
        Executes a query to add a log to the database
        Returns:
            The result of the query execution.
        """
        query = '''INSERT INTO buy_logs (time, buy_price, sell_price, stop_loss, stock)
                   VALUES (%s, %s, %s, %s, %s)
                '''
        result = db_connection.execute(query,(time,buy_price,sell_price,stop_loss,stock),operation_type='insert')
        return result      



