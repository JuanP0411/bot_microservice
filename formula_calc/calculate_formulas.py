import re
from typing import List
import numexpr as ne
import pandas as pd
from data_retrival.retrive_data import DataCacheV2
from tvDatafeed import TvDatafeed, Interval
import os
import json
from formula_manage.utils import decrypt_data
from data_retrival.redis_connection import RedisConnection
def apply_formulas_to_dataframe(df:pd.DataFrame,user_formula:pd.Series):
        #print("Applying formulas to DataFrame")
        applied_formulas = set()
        # TODO: change so it only applies to one formula
        column_name = user_formula[2]
        formula = user_formula[3]

        if column_name in df.columns:
                #print(f"Skipping already existing column: {column_name}")
            pass
        print("Formula ", formula, "Name : ", column_name)
        processed_formula = preprocess_time_shifts(df, formula)
        print("Processed_formula : ", processed_formula)
        valid_words = ['open', 'close', 'volume', 'high', 'low']
        if needs_calculation(processed_formula):
                df[column_name] = ne.evaluate(processed_formula, local_dict=df)
        else:
            if processed_formula.lower() in valid_words:
                df[column_name] = ne.evaluate(processed_formula, local_dict=df)
            else:
                df.rename(columns={processed_formula: column_name}, inplace=True)

            applied_formulas.add(column_name)
            #print(f"Applied formula: {column_name}")
        return df.iloc[-1]
        #print("Completed applying formulas")

def needs_calculation(formula):
        # This is a simple placeholder implementation.
        # Adjust the logic based on your specific requirements.
        return any(op in formula for op in ["+", "-", "*", "/", "MA", "HV","log","sqrt","where"])

def preprocess_time_shifts(df, formula):
        # Print the original formula for debugging
        # print(f"Original formula: {formula}")
        # print("Before preprocessing time shifts:", df.columns.tolist())

        # Handling the HV operation
        hv_pattern = r'HV\((\w+),(\d+)\)'
        hv_matches = re.findall(hv_pattern, formula)
        for match in hv_matches:
            column, window_length = match
            hv_column_name = f"hv_{column}_{window_length}"
            if hv_column_name not in df.columns:
                window_length = int(window_length)
                df[hv_column_name] = df[column].pct_change().rolling(window=window_length).std() * (252 ** 0.5)
                formula = formula.replace(f"HV({column},{window_length})", hv_column_name)

        # Process the MA operation
        ma_matches = re.findall(r'MA\((\w+),\s*(\d+)\)', formula)
        for match in ma_matches:
            column, periods = match
            periods = int(periods)
            ma_column_name = f"ma_{column}_{periods}"

            # Check if the column name already exists and create a unique name
            original_ma_column_name = ma_column_name
            suffix = 1
            while ma_column_name in df.columns:
                ma_column_name = f"{original_ma_column_name}_{suffix}"
                suffix += 1

            if ma_column_name not in df.columns:
                df[ma_column_name] = df[column].astype(float).rolling(window=periods).mean()
                formula = formula.replace(f"MA({column},{periods})", ma_column_name)
        
        # Clean the formula of control characters
        formula = re.sub(r'[\r\n]', '', formula)
        formula = re.sub(r'[^\x20-\x7E]+', '', formula)
        return formula


#calculates the formula and determines wether to buy or sell
def determine_formula_output(formula_df_list:List[pd.DataFrame],user_data: dict):
     #iterate through the dataframe and determine
     #for each formula wether to buy or sell depending on threshold
     redis_conn = RedisConnection()
     redis_conn.connect()
     for df in formula_df_list:
        trade_or_not = True
        print("Executing formula for", df[1])
        for index, row in df.iterrows():

            
            # Obtain TV credentials from environment variables
            tv_username = os.environ.get("TRADING_VIEW_USER")
            tv_pass = os.environ.get("TRADING_VIEW_PASSWORD")
            
            # Initialize a DataCache object to obtain stock data
            data_cache = DataCacheV2(tv_data_feed=TvDatafeed(
                username=tv_username,
                password=tv_pass),
                redis_client=redis_conn)
            
            # Parse data and obtain stock data
            intervals = get_interval_enum(row[8]["period"])
            stock_df = data_cache.get_data(
                symbol=row[8]["selected_symbol"],
                exchange=row[8]["selected_exchange"],
                interval=intervals,
                n_bars=row[8]["num_periods"])
            
            # Apply formulas to the dataframe
            calculated_formula = apply_formulas_to_dataframe(df=stock_df, user_formula=row)
            
            # Determine buy or sell decision
            decision = determine_buy_or_sell(formula_data=row, calculated_data=calculated_formula, user_data=user_data)
            #assign the value of true or false to a variable
            #if determine buy or sell returns false at any point leave it at false
            #check at teh end of the loop
            if(decision == False):
                 trade_or_not = False
                
        if(trade_or_not == True):
             print(" FINAL RESULT : Executed Trade")
        else:
             print(" FINAL RESULT : Trade not executed")
     return True

#add logic to grab user credentials, add method in utils to decrypt tvpassword
def determine_buy_or_sell(formula_data:pd.Series, calculated_data: pd.Series, user_data: dict):
    #Replace with == "buy"
    formula_username = formula_data.iloc[1]
    if(formula_data.iloc[9] == "buy"):
        #Check if the value at the of the formula is above or below the threshold to buy
        if(formula_data.iloc[5] == False):
            print("compared Values")
            print(calculated_data.iloc[6], formula_data.iloc[4])
            if( calculated_data.iloc[6]>=formula_data.iloc[4]):
                #TODO implement buying stock logic
                tv_username = user_data[formula_username]["tv_user"]
                tv_password = user_data[formula_username]["tv_pass"]
                print("bought stock")
                return True
            else:
                 print("stock not bought")
                 return False

        else:
            print("compared Values")
            print(calculated_data.iloc[6], formula_data.iloc[4])
            if( calculated_data.iloc[6]<=formula_data.iloc[4]):
                #TODO implement buying stock logic

                tv_username = user_data[formula_username]["tv_user"]
                tv_password = user_data[formula_username]["tv_pass"]
                decrypt_data(tv_password)
                print("bought stock inverted")
                return True
            else:
                 print("stock not bought inverted")
                 return False

    #Replace with == "sell"       
    elif(formula_data.iloc[9] == "buy"):
        #check if the value of the formula is above or below to the threshold to sell
        if(formula_data.iloc[5] == False):
            #add check to see if formula is valid or not 
            print("compared Values")
            print(calculated_data.iloc[6], formula_data.iloc[4])
            if( calculated_data.iloc[6]>=formula_data.iloc[4]):
                #TODO implement buying stock logic
                tv_username = user_data[formula_username]["tv_user"]
                tv_password = user_data[formula_username]["tv_pass"]
                decrypt_data(tv_password)
                print("Sold stock")
                return True
            else:
                 print("stock not Sold")
                 return False


        else:
            print("compared Values")
            print(calculated_data.iloc[6], formula_data.iloc[4])
            if( calculated_data.iloc[6]<=formula_data.iloc[4]):
                #TODO implement buying stock logic
                tv_username = user_data[formula_username]["tv_user"]
                tv_password = user_data[formula_username]["tv_pass"]
                decrypt_data(tv_password)
                print("Sold stock inverted")
                return True
            else:
                 print("stock not sold inverted")
                 return False


    return True



def get_interval_enum(interval_str):
        interval_map = {
        "1m": Interval.in_1_minute,
        "5m": Interval.in_5_minute,
        "15m": Interval.in_15_minute,
        "30m": Interval.in_30_minute,
        "1h": Interval.in_1_hour,
        "2h": Interval.in_2_hour,
        "4h": Interval.in_4_hour,
        "1d": Interval.in_daily,
        "1W": Interval.in_weekly,
        "1M": Interval.in_monthly
        }

        return interval_map[interval_str]
     
