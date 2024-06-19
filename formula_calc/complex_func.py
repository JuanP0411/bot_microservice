import pandas as pd
import numpy as np


def check_MA_condition(df, window=100):
    # Calculate the 100-period moving average of the 'close' prices

    df['MA_100'] = df['close'].astype(float).rolling(window=window).mean()
    
    # Calculate the standard deviation of the 100-period moving average
    ma_100_stdev = df['close'].tail(100)
    ma_100_stdev = ma_100_stdev.std()
    
    # Calculate the expression: ma(close,100) - 2 * (stdev(ma(close,100)))
    expression_result = df['MA_100']  - 2 * ma_100_stdev
    selling_price = df['MA_100']  +  3 * ma_100_stdev
    stop_loss_price = df['MA_100']  - 3 * ma_100_stdev
    
    # Compare if ma(close,100) is lower than -2 * (stdev(ma(close,100)))
    print("close: ", df['close'].iloc[-1])
    print("Standard_dev", round(ma_100_stdev,3))
    print("lower band:", round(expression_result.iloc[-1],3))
    condition_met = round(df['MA_100'].iloc[-1],3)  < round(expression_result.iloc[-1],3)
    print("Condition met? : ",condition_met)

    return condition_met, round(selling_price.iloc[-1],3), round(stop_loss_price.iloc[-1],3)


# def calculate_rsi(df, window=14):
#     # Calculate price changes
#     print(df)
#     delta = df['close'].diff()
    
#     # Get gains and losses
#     gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
#     # Calculate Relative Strength (RS)
#     rs = gain / loss
    
#     # Calculate RSI
#     rsi = 100 - (100 / (1 + rs))
    
#     # Shift the RSI values by one period to get the RSI of the previous period
#     rsi_previous = rsi.shift(1)
#     print("rsi :" , rsi.iloc[-1])
#     print("rsi previous :", rsi_previous.iloc[-1])
#     if rsi.iloc[-1] >= 30 and rsi_previous.iloc[-1] < 30 :
#         return True
#     else :
#         return False


def calculate_rsi(close_prices, period=14):
    # Calculate price changes
    delta = close_prices['close'].diff()
    
    # Calculate upward and downward changes
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    # Calculate the average gains and losses using Wilder's smoothing method
    def rma(values, n):
        # rma is a recursive moving average
        alpha = 1 / n
        rma_values = np.zeros_like(values)
        rma_values[n-1] = np.mean(values[:n])
        for i in range(n, len(values)):
            rma_values[i] = alpha * values[i] + (1 - alpha) * rma_values[i-1]
        return rma_values
    
    avg_gain = rma(gain, period)
    avg_loss = rma(loss, period)
    
    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss

    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Initial RSI values will be NaN until enough data points are available
    rsi[:period] = np.nan
    print("rsi :" , round(rsi[-1],3))
    print("rsi previous :", round(rsi[-2],3))
    if round(rsi[-1],3) >= 30 and round(rsi[-2],3) < 30 :
        return True
    else :
        return False

def calculate_historic_volatility(df, window=10):
    # Calculate the logarithmic returns of the 'close' prices
    df['log_returns'] = np.log(df['close'].astype(float) / df['close'].shift(1).astype(float))
    
    # Calculate the rolling standard deviation of the logarithmic returns
    df['volatility'] = df['log_returns'].rolling(window=window).std() * np.sqrt(365)

    recent_volatility = df['volatility'].iloc[-1]
    
    # Print the recent volatility
    print("Recent historic volatility:", recent_volatility)

    return recent_volatility

