import sqlite3
import logging
import sqlite3
import psycopg2
#import mysql.connector


class BaseDatabaseConnection:
    def execute(self, sql, params=None, operation_type='execute', debug=1, log=0):
        if self.conn is None:
            self._connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params or ())
            if operation_type in ['insert', 'delete', 'update']:
                self.conn.commit()
                
                return cursor.lastrowid
            elif operation_type == 'query':
                return cursor.fetchall()
            if True:
                print(f'Executed SQL: {sql} | Params: {params}')    
        except Exception as e:
            print(f"An SQL error occurred: {e}")
            if debug:
                print(f'Failed SQL: {sql} | Params: {params}')
            return None
        finally:
            if log:
                logging.info(f"Executed SQL: {sql} | Operation Type: {operation_type} | Params: {params}")
            cursor.close()
    
    def delete(self, sql, params, debug=0, log=0):
        """Execute a DELETE SQL command."""
        if self.conn is None:
            self._connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            self.conn.commit()
            if debug:
                print(f'Deleted {cursor.rowcount} row(s).')
            return cursor.rowcount
        except Exception as e:
            print(f"An SQL error occurred during delete: {e}")
            if debug:
                print(f'Failed SQL: {sql} | Params: {params}')
            return -1
        finally:
            if log:
                logging.info(f"Executed DELETE SQL: {sql} | Params: {params}")
            cursor.close()        



    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

class SQLiteDatabaseConnection(BaseDatabaseConnection):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path,check_same_thread=False)

    
class PostgresDatabaseConnection(BaseDatabaseConnection):
    def __init__(self, host,passworddb,user,port,database):
        self.host = host
        self.conn = None
        self.password = passworddb
        self.user = user
        self.port = port
        self.database = database

    def _connect(self):
        self.conn = psycopg2.connect(database=self.database,user=self.user,password=self.password,port=self.port,host=self.host)

    def cursor(self):
        """
        Create and return a cursor object for executing SQL commands.
        """
        if self.conn is None or self.conn.closed:
            self._connect()
        return self.conn.cursor()

    def commit(self):
        """
        Commit any pending transaction to the database.
        """
        if self.conn is not None and not self.conn.closed:
            self.conn.commit()

    
