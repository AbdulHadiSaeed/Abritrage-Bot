# 28-02-2020
# Improving opportunities
# https://github.com/MD3XTER/Arbitrage-Bot

import time
import ccxt
from datetime import datetime
import threading

exchangesData = {
    "hitbtc": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.001
    },
    "binance": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.001
    },
    "bittrex": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.0025
    },
    "poloniex": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.0025
    },
    "exmo": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.002
    },
}

min_profit = 0

exchanges = [
    "binance",
    "bittrex",
    "hitbtc",
    "poloniex",
]


def main():
    threading.Thread(target=thread_function, args=(exchanges, "BTC/USDT")).start()

    threading.Thread(target=thread_function, args=(exchanges, "ETH/USDT")).start()

    threading.Thread(target=thread_function, args=(exchanges, "LTC/USDT")).start()

    threading.Thread(target=thread_function, args=(exchanges, "DASH/USDT")).start()



def get_min_amount(exchange_id, symbol):
    exchange = eval("ccxt.{0}()".format(exchange_id))

    exchange.load_markets()

    return float(exchange.markets[symbol]["limits"]["amount"]["min"])


def thread_function(exchanges, symbol):
    min_ask_exchange_id = ""
    min_ask_price = 99999999
    max_bid_exchange_id = ""
    max_bid_price = 0
    exchange_symbol = ""
    count=0



    while (1):
        # print("-----------------------------")
        count+=1





        # print("Searching for the best opportunity for {0} on {1}".format(symbol, exchanges))

        ask_exchange_id, ask_price, bid_exchange_id, bid_price = get_biggest_spread_by_symbol(exchanges, symbol)

        increase_percentage = (bid_price - ask_price) / ask_price * 100
        now1 = datetime.now()
        now = now1.strftime('[' + "%m/%d/%Y, %H:%M:%S" + ']')

        print((increase_percentage,symbol,now),"Number of Count=",count)


        # print("[{0} - {1}] - [{2}] - Price Spread: {3:.2}%".format(ask_exchange_id, bid_exchange_id, symbol, increase_percentage))

        if increase_percentage > 0:
            print("[{0} - {1}] - [{2}] - Price Spread: {3:.2}%".format(ask_exchange_id, bid_exchange_id, symbol,
                                                                       increase_percentage))
            exchange_symbol = symbol
            min_ask_exchange_id = ask_exchange_id
            min_ask_price = ask_price
            max_bid_exchange_id = bid_exchange_id
            max_bid_price = bid_price
            # print("\n----------Settings-----------")
            ask_amount = get_min_amount(min_ask_exchange_id, exchange_symbol)
            # print("Min Ask amount: {0}".format(ask_amount))
            bid_amount = get_min_amount(max_bid_exchange_id, exchange_symbol)
            # print("Min Bid amount: {0}".format(bid_amount))
            amount = max(ask_amount, bid_amount)
            # print("Actual amount: {0}".format(amount))
            # print("Min profit: {0}%".format(min_profit))

            # print("\n--------Best Spread----------")
            # print("[{0} - {1}] - [{2}]: Spread percentage: {3:.2}%".format(min_ask_exchange_id, max_bid_exchange_id, exchange_symbol, increase_percentage))

            # print("\n-----Market Opportunity------")
            print("Buy {0} {1} from {2} at {3} {4}".format(amount, exchange_symbol.split("/")[0], min_ask_exchange_id,
                                                           min_ask_price, exchange_symbol.split("/")[0]))
            print("Sell {0} {1} on {2} at {3} {4}".format(amount, exchange_symbol.split("/")[0], max_bid_exchange_id,
                                                          max_bid_price, exchange_symbol.split("/")[0]))

            # print("\n-------------Fees------------")
            min_ask_fee = min_ask_price * amount * exchangesData[min_ask_exchange_id]["transactionFee"]
            print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(min_ask_exchange_id, exchangesData[min_ask_exchange_id]["transactionFee"]*100, min_ask_fee, exchange_symbol.split("/")[0]))

            max_bid_fee = max_bid_price * amount * exchangesData[max_bid_exchange_id]["transactionFee"]
            print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(max_bid_exchange_id,
                                                                  exchangesData[max_bid_exchange_id][
                                                                      "transactionFee"] * 100, max_bid_fee,
                                                                  exchange_symbol.split("/")[0]))

            print("\n-----------Profit------------")
            cost = amount * min_ask_price
            # print("You will have to spend: {0:.4} {1}".format(cost, exchange_symbol.split("/")[1]))
            profit = ((max_bid_price - min_ask_price) * amount) - (max_bid_fee + min_ask_fee)
            print("You will make {0:.4} {1} profit(including fees)".format(profit, exchange_symbol.split("/")[1]))

            print("\n-----------Buy/Sell----------")
            if profit >= min_profit:
                print("profit profit profit:)")
            else:
                print("It seems like you won't make enough profit :(")


def get_biggest_spread_by_symbol(exchanges, symbol):
    ask_exchange_id = ""
    min_ask_price = 99999999

    bid_exchange_id = ""
    max_bid_price = 0

    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        try:
            order_book = exchange.fetch_order_book(symbol)
            #print(exchange,symbol,order_book)
            bid_price = order_book['bids'][0][0] if len(
                order_book['bids']) > 0 else None
            ask_price = order_book['asks'][0][0] if len(
                order_book['asks']) > 0 else None


            if ask_price < min_ask_price:
                ask_exchange_id = exchange_id
                min_ask_price = ask_price
            if bid_price > max_bid_price:
                bid_exchange_id = exchange_id
                max_bid_price = bid_price

            increase_percentage = (bid_price - ask_price) / ask_price * 100
            if increase_percentage >= 1:
                return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price
        except:
            # pass
            print("")
            print("{0} - There is an error!".format(exchange_id))

    min_ask_price += 0.235
    max_bid_price -= 0.235

    return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price


if __name__ == "__main__":

    main()
