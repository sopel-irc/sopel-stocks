# coding=utf-8
import requests


def finnhub(bot, symbol):
    r = requests.get(
        "https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}".format(
            symbol=symbol, api_key=bot.config.stocks.api_key
        )
    )

    if not r.json():
        raise Exception("An error occurred.")
    
    close = r.json()['c']
    # prevclose = r.json()['pc']
    change = r.json()['d']
    percentchange = r.json()['dp']

    data = {"close": close, "change": change, "percentchange": percentchange}
    return data
