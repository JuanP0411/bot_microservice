import pandas as pd
from .utils import sort_formulas, create_user_dictionary
from .scheduler import Scheduler
import uuid
class Formula_manager:
 
    def __init__(self,df:pd.DataFrame,scheduler: Scheduler,user_data:list):
     self.formulas_1m = sort_formulas(df=df,period="1m")
     self.formulas_5m = sort_formulas(df=df,period="5m") 
     self.formulas_15m = sort_formulas(df=df,period="15m")
     self.formulas_1h = sort_formulas(df=df,period="1h")
     self.formulas_1d = sort_formulas(df=df,period="1d")
     self.uuid_1m = str(uuid.uuid4())
     self.uuid_5m = str(uuid.uuid4())
     self.uuid_15m = str(uuid.uuid4())
     self.uuid_1h = str(uuid.uuid4())
     self.uuid_1d = str(uuid.uuid4())
     self.user_data = create_user_dictionary(user_list=user_data)
     self.scheduler = scheduler


    def scedule_formulas(self):
        #Schedule formulas for 1 minute interval
        self.scheduler.schedule_formulas(df=self.formulas_1m,period="min",time=5,uuid=self.uuid_1m,user_data=self.user_data)
        #Schedule formulas for 5 minute interval
        self.scheduler.schedule_formulas(df=self.formulas_5m,period="min",time=1,uuid=self.uuid_5m,user_data=self.user_data)
        #Schedule formulas for 15 minute interval
        self.scheduler.schedule_formulas(df=self.formulas_15m,period="min",time=15,uuid=self.uuid_15m,user_data=self.user_data)
        #Schedule formulas for 1 hour interval
        self.scheduler.schedule_formulas(df=self.formulas_1h,period="hour",time=1,uuid=self.uuid_1h,user_data=self.user_data)
        #Schedule formulas for 1 day interval
        self.scheduler.schedule_formulas(df=self.formulas_1d,period="day",time=1,uuid=self.uuid_1d,user_data=self.user_data)
        self.scheduler.scheduler.start()

        return True
    
    def update_formulas(self,new_formula_df:pd.DataFrame):
        self.formulas_1m = sort_formulas(df=new_formula_df,period="1m")
        self.formulas_5m = sort_formulas(df=new_formula_df,period="5m") 
        self.formulas_15m = sort_formulas(df=new_formula_df,period="15m")
        self.formulas_1h = sort_formulas(df=new_formula_df,period="1h")
        self.formulas_1d = sort_formulas(df=new_formula_df,period="1d")

        self.scheduler.scheduler.modify_job(self.uuid_1m,kwargs={'formula_df_list': self.formulas_1m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_5m,kwargs={'formula_df_list': self.formulas_5m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_15m,kwargs={'formula_df_list': self.formulas_15m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_1h,kwargs={'formula_df_list': self.formulas_1h,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_1d,kwargs={'formula_df_list': self.formulas_1d,'user_data': self.user_data})
        return True
    
    def update_user(self):
        
        self.scheduler.scheduler.modify_job(self.uuid_1m,kwargs={'formula_df_list': self.formulas_1m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_5m,kwargs={'formula_df_list': self.formulas_5m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_15m,kwargs={'formula_df_list': self.formulas_15m,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_1h,kwargs={'formula_df_list': self.formulas_1h,'user_data': self.user_data})
        self.scheduler.scheduler.modify_job(self.uuid_1d,kwargs={'formula_df_list': self.formulas_1d,'user_data': self.user_data})
        return True
    
    


     
