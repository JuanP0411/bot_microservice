
from apscheduler.schedulers.background import BackgroundScheduler

import pandas as pd
from db.BasicDbOperations import BasicDbOperations
from environment_config import EnvironmentConfig
from formula_manage.formula_manager import Formula_manager
from formula_manage.scheduler import Scheduler

from fastapi import FastAPI
import uvicorn
from formula_manage.utils import create_user_dictionary
from formula_calc.calculate_formulas import determine_formula_output

app = FastAPI()


        
    # Create an instance of EnvironmentConfig
env_config = EnvironmentConfig()
    
    # Create an instance of BasicDbOperations with env_config


strategy_list = [determine_formula_output]

    #setup Formula_manager to schedule formula checks for each time interval
background_formula_scheduler = BackgroundScheduler() 
formula_scheduler = Scheduler(background_formula_scheduler)
formula_manager = Formula_manager(strategy_list, formula_scheduler)
formula_manager.scedule_formulas()



if __name__ == "__main__":

    uvicorn.run(app=app, host="127.0.0.1", port=5555, log_level= "debug")