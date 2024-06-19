from datetime import datetime
import re
from typing import List
import pandas as pd
from data_retrival.retrive_data import DataCacheV2
from tvDatafeed import TvDatafeed, Interval
import os
import json
from db.BasicDbOperations import BasicDbOperations
from environment_config import EnvironmentConfig
from formula_manage.utils import decrypt_data
from data_retrival.redis_connection import RedisConnection
from order_manager.orders import buy_stock, check_orders
from .complex_func import check_MA_condition, calculate_rsi, calculate_historic_volatility
# from db.queries.formula_queries import FormulaQueries

def apply_formulas_to_dataframe(df:pd.DataFrame,user_formula:pd.Series):
        #print("Applying formulas to DataFrame")
        applied_formulas = set()
        # TODO: change so it only applies to one formula
        column_name = user_formula[2]
        formula = user_formula[3]

        # if column_name in df.columns:
        #         #print(f"Skipping already existing column: {column_name}")
        #     pass
        # print("Formula ", formula, "Name : ", column_name)
        # processed_formula = preprocess_time_shifts(df, formula)
        # print("Processed_formula : ", processed_formula)
        # valid_words = ['open', 'close', 'volume', 'high', 'low']
        # if needs_calculation(processed_formula):
        #         df[column_name] = ne.evaluate(processed_formula, local_dict=df)
        # else:
        #     if processed_formula.lower() in valid_words:
        #         df[column_name] = ne.evaluate(processed_formula, local_dict=df)
        #     else:
        #         df.rename(columns={processed_formula: column_name}, inplace=True)

        #     applied_formulas.add(column_name)
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
     

def determine_formula_output():
    redis_conn = RedisConnection()
    redis_conn.connect()


#             # Obtain TV credentials from environment variables
    tv_username = os.environ.get("TRADING_VIEW_USER")
    tv_pass = os.environ.get("TRADING_VIEW_PASSWORD")
            
            # Initialize a DataCache object to obtain stock data
    attempts = 2  # Number of attempts to try

    for attempt in range(attempts):
        try:
            # Initialize the data cache with TvDatafeed and redis client
            data_cache = DataCacheV2(
                tv_data_feed=TvDatafeed(
                    username=tv_username,
                    password=tv_pass
                ),
                redis_client=redis_conn
            )

            # Get the interval enum for "5m"
            intervals = get_interval_enum("5m")

            # Fetch the stock data for TSLA from NASDAQ
            stock_df = data_cache.get_data(
                symbol="TSLA",
                exchange="NASDAQ",
                interval=intervals,
                n_bars=200
            )


        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt + 1 == attempts:
                print("All attempts failed. Something went wrong.")
                return None

    criteria_1,selling_price,stop_loss_price = check_MA_condition(stock_df)
    criteria_2 = calculate_rsi(stock_df)

    calculate_historic_volatility(df=stock_df)
    print("condition 1: ", criteria_1, "condition 2: ", criteria_2)
    print("Sell amount :", selling_price)
    print("stop loss: ", stop_loss_price)
    
    env_config = EnvironmentConfig()
    alpaca_key = env_config.alpaca_key
    alpaca_secret = env_config.alpaca_secret
    check_order_criteria = check_orders(Api_key=alpaca_key,Api_secret=alpaca_secret)


    if(criteria_1 == True and criteria_2 == True and check_order_criteria == True):
             

             #add verification to see if the last order has been sold, if it has then create new order
             print(" FINAL RESULT : Executed Trade")
             symbol = 'TSLA'
             qty = 1
             buy_stock(symbol=symbol,qty=qty,stop_price_value=stop_loss_price,sell_price=selling_price,Api_key=alpaca_key,Api_secret=alpaca_secret)
            #  sell_stock(symbol=symbol,qty=qty,limit_price=selling_price)
            #  stop_loss(symbol=symbol,qty=qty,stop_price=stop_loss_price)

             basic_db_operations = BasicDbOperations(env_config)
             db_conn = basic_db_operations.db_connection
             buy_price = 100.00
             query_result = basic_db_operations.add_logs_query(db_connection=db_conn,time=datetime.now(),buy_price=buy_price,sell_price=selling_price,stop_loss=stop_loss_price,
                                                    stock=symbol)
             print(query_result)



    else:
             print(" FINAL RESULT : Trade not executed")
    return True


def run_strategies(strategy_list: List):

    for strategy in strategy_list:
        strategy()




    return True