import alpaca_trade_api as tradeapi


BASE_URL = 'https://paper-api.alpaca.markets'

def buy_stock(symbol, qty,sell_price,stop_price_value,Api_key,Api_secret):
    api = tradeapi.REST(Api_key, Api_secret, BASE_URL, api_version='v2')
    sell_price = round(sell_price,2)
    stop_price_value = round(stop_price_value,2)
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc',  # Good till canceled
            order_class='bracket',
            take_profit=dict(
                limit_price=sell_price
            ),
            stop_loss=dict(
                stop_price=stop_price_value
            )
        )
        print(f"Buy order for {qty} shares of {symbol} placed successfully.")
        return order
    except Exception as e:
        print(f"An error occurred while placing a buy order: {e}")


def sell_stock(symbol, qty, limit_price,Api_key='',Api_secret='' ):
    api = tradeapi.REST(Api_key, Api_secret, BASE_URL, api_version='v2')
    limit_price = round(limit_price, 2)
    print("CHECKING ORDRS")
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='limit',
            time_in_force='gtc',  # Good till canceled
            limit_price= limit_price
        )
        print(f"Sell order for {qty} shares of {symbol} at a price of {limit_price} placed successfully.")
        return order
    except Exception as e:
        print(f"An error occurred while placing a sell order: {e}")
    

    return True


def stop_loss(symbol, qty, stop_price,Api_key='',Api_secret=''):
    api = tradeapi.REST(Api_key, Api_secret, BASE_URL, api_version='v2')
    try:
        stop_price = round(stop_price, 2)
        order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='stop',
        time_in_force='gtc',
        stop_price=stop_price
        )
        print(f"stop_loss order for {qty} shares of {symbol} at a price of {stop_price} placed successfully.")
    except Exception as e:
        print(f"An error occurred while placing a sell order: {e}")
    return True


def check_orders(Api_key='',Api_secret=''):
    api = tradeapi.REST(Api_key, Api_secret, BASE_URL, api_version='v2')
    open_orders = api.list_orders(status='open')

    bracket_orders = [order for order in open_orders if order.order_class == 'bracket']

    if bracket_orders:
        print("Bracket orders still exist will not be placing a new order")
        return False
    else:
        print("Bracket order does not exist")
        return True
