import streamlit as st
import json
import datetime
from db.database_connection import SQLiteDatabaseConnection

class FormulaQueries:
    def __init__(self, db_connection:SQLiteDatabaseConnection):
        # Initialize session state for formulas if not already present
        self.db_connection = db_connection


    def load_user_formulas(self,username):

        #IF user role is equal to professor then access al the formulas from all the students
        user_role = st.session_state["role"]
        if user_role == "professor" :
            sql = 'SELECT id, signal_name, formula, threshold, invert, graph_type, graph_details, widget_data FROM user_signals'
            user_formulas = self.db_connection.execute(sql = sql, operation_type='query')
        else : 
            sql = 'SELECT id, signal_name, formula, threshold, invert, graph_type, graph_details, widget_data FROM user_signals WHERE username = %s'
            user_formulas = self.db_connection.execute(sql, (username,), operation_type='query')
        """Load user-specific formulas from the database."""
        
        if user_formulas:
            st.session_state['formulas'] = [
                {
                    'id': row[0],
                    'name': row[1],
                    'formula': row[2],
                    'threshold': float(row[3]),
                    'invert': row[4],
                    'graph_type': row[5],
                    'graph_details': row[6],
                    'widget_data': row[7] if row[7] else {}
                }
                for row in user_formulas
            ]
        else:
            st.session_state['formulas'] = []

    
    def save_user_signal(self, username, signal_name, formula, threshold, invert, graph_type, graph_details, widget_data):
        # Preprocess widget_data to convert datetime.date and datetime.datetime objects to string
        preprocessed_widget_data = {}
        for key, value in widget_data.items():
            if isinstance(value, datetime.date):
                # For datetime.date objects
                preprocessed_widget_data[key] = value.isoformat()
            elif isinstance(value, datetime.time):
                # For datetime.time objects, format them into a string (HH:MM:SS)
                preprocessed_widget_data[key] = value.strftime("%H:%M:%S")
            else:
                preprocessed_widget_data[key] = value
                
        print(f"widget data{preprocessed_widget_data}")
        serialized_widget_data = json.dumps(preprocessed_widget_data)
        try:
            sql = '''
            INSERT INTO user_signals (username, signal_name, formula, threshold, invert, graph_type, graph_details, widget_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            self.db_connection.execute(sql, (username, signal_name, formula, threshold, invert, graph_type, graph_details, serialized_widget_data), operation_type='insert')
        except Exception as e:
            print(f"Error saving user signal: {e}")

    def update_user_signal(self, signal_id, username, signal_name, formula, threshold, invert, graph_type, graph_details, widget_data):
        # Serialize widget data to JSON
        serialized_widget_data = json.dumps(widget_data)
        
        sql = '''
        UPDATE user_signals
        SET signal_name = %s, formula = %s, threshold = %s, invert = %s, graph_type = %s, graph_details = %s, widget_data = %s
        WHERE id = %s AND username = %s
        '''
        print(f"SQL: {serialized_widget_data}")
        self.db_connection.execute(sql, (signal_name, formula, threshold, invert, graph_type, graph_details, serialized_widget_data, signal_id, username), operation_type='update')

    def delete_user_signal(self, signal_id, username):
        sql = 'DELETE FROM user_signals WHERE id = %s AND username = %s'
        return self.db_connection.execute(sql, (signal_id, username), operation_type='delete')

    def get_user_signals(self, username):
        sql = 'SELECT signal_name, formula, threshold, invert, graph_type, graph_details FROM user_signals WHERE username = %s'
        return self.db_connection.execute(sql, (username,), operation_type='query')
    
    def save_formulas_in_order(self, username, formulas):
        # Delete existing user formulas
        delete_sql = 'DELETE FROM user_signals WHERE username = %s'
        self.db_connection.execute(delete_sql, (username,), operation_type='delete')

        # Re-insert formulas in the new order
        insert_sql = '''
            INSERT INTO user_signals (username, signal_name, formula, threshold, invert, graph_type, graph_details)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        for formula in formulas:
            self.db_connection.execute(insert_sql, (username, formula['name'], formula['formula'], 
                                                    formula['threshold'], formula['invert'], 
                                                    formula['graph_type'], formula['graph_details']), 
                                    operation_type='insert')
