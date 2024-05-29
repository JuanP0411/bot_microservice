
from apscheduler.schedulers.background import BackgroundScheduler

import pandas as pd
from db.BasicDbOperations import BasicDbOperations
from environment_config import EnvironmentConfig
from formula_manage.formula_manager import Formula_manager
from formula_manage.scheduler import Scheduler
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from fastapi import FastAPI
from db.schemas import Formula
import uvicorn
from formula_manage.utils import create_user_dictionary

app = FastAPI()


        
    # Create an instance of EnvironmentConfig
env_config = EnvironmentConfig()
    
    # Create an instance of BasicDbOperations with env_config
basic_db_operations = BasicDbOperations(env_config)
    

db_conn = basic_db_operations.db_connection
result =basic_db_operations.load_dataframe_from_sql(db_connection=db_conn,data_table="user_signals")
    # List of tuples so just iterate through the tuples and calculate
    
    #Todo create a job that every minute iterates through the formulas 

    #Create a method that extracts ffrom the result df all the formulas and create a new df with all the formulas with the same period
    #turn this into a method 
    #the widget data is a dictionary structure should work
formula_dataframe = pd.DataFrame(result)

user_data = basic_db_operations.user_query(db_connection=db_conn)


    #setup Formula_manager to schedule formula checks for each time interval
background_formula_scheduler = BackgroundScheduler() 
formula_scheduler = Scheduler(background_formula_scheduler)
formula_manager = Formula_manager(formula_dataframe, formula_scheduler,user_data=user_data)
formula_manager.scedule_formulas()






@app.get('/patch-formula')
async def update_formula():
    new_user_signlas = basic_db_operations.load_dataframe_from_sql(db_connection=db_conn,data_table="user_signals")
    new_formula_dataframe = pd.DataFrame(new_user_signlas)
    print(new_formula_dataframe)
    formula_manager.update_formulas(new_formula_df=new_formula_dataframe)

    return True


@app.get('/update-users')
async def update_formula():
    user_data = basic_db_operations.user_query(db_connection=db_conn)
    formula_manager.user_data=create_user_dictionary(user_list=user_data)
    new_user_signlas = basic_db_operations.load_dataframe_from_sql(db_connection=db_conn,data_table="user_signals")
    new_formula_dataframe = pd.DataFrame(new_user_signlas)
    formula_manager.update_formulas(new_formula_df=new_formula_dataframe)
    return True


if __name__ == "__main__":

    uvicorn.run(app=app, host="127.0.0.1", port=5555, log_level= "debug")