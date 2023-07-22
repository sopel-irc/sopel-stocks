# coding=utf-8
import requests


def alphavantage(bot, symbol):
    r = requests.get(
        "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&apikey={api_key}".format(
            symbol=symbol, api_key=bot.config.stocks.api_key
        )
    )

    if not r.json():
        raise Exception("An error occurred.")

    if "Information" in r.json().keys():
        raise Exception(r.json()["Information"])

    if "Error Message" in r.json().keys():
        raise Exception(r.json()["Error Message"])

    days = sorted(r.json()["Time Series (Daily)"].keys(), reverse=True)

    # Only 1 day of history, likely this is a new stock on the market
    if len(days) == 1:
        today = days[0]
        close = r.json()["Time Series (Daily)"][today]["4. close"]
        prevclose = r.json()["Time Series (Daily)"][today]["1. open"]
    else:
        # Get today's entry
        today = days[0]
        prevdate = days[1]

        # dict_keys(['1. open', '2. high', '3. low', '4. close', '5. volume'])
        # open = r.json()['Time Series (Daily)'][today]['1. open']
        # high = r.json()['Time Series (Daily)'][today]['2. high']
        # low = r.json()['Time Series (Daily)'][today]['3. low']
        close = r.json()["Time Series (Daily)"][today]["4. close"]
        # volume = r.json()['Time Series (Daily)'][today]['5. volume']

        # Get yesterday's close
        prevclose = r.json()["Time Series (Daily)"][prevdate]["4. close"]

    # Calculate change
    change = float(close) - float(prevclose)

    # Calculate percentage change
    percentchange = float(change) / float(prevclose) * 100

    data = {"close": close, "change": change, "percentchange": percentchange}
    return data
