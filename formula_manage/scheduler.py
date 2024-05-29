from apscheduler.schedulers.background import BackgroundScheduler
from formula_calc.calculate_formulas import determine_formula_output
from apscheduler.triggers.interval import IntervalTrigger

class Scheduler:
    def __init__(self, scheduler:BackgroundScheduler):
        self.scheduler = scheduler





    def schedule_formulas(self,time:int,period:str,df,uuid:str,user_data:dict):
        if(period == "min"):
            interval = IntervalTrigger(minutes=time)
        elif(period == "hour"):
            interval = IntervalTrigger(hours=time)
        elif(period == "day"):
            interval = IntervalTrigger(days=time)


        self.scheduler.add_job(
           func=determine_formula_output,
           trigger=interval,
           kwargs={'formula_df_list':df, 'user_data': user_data},
           id=uuid
        )

    # def start_scheduler(self):
    #     self.scheduler.start()

    def modify_scheduled_job(self,job_uuid:str,):
        self.scheduler.modify_job(id=job_uuid)
        return True
