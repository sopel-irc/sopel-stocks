# coding=utf-8
import requests


def iexcloud(bot, symbol):
    r = requests.get('https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}&displayPercent=true'.format(symbol=symbol, api_key=bot.config.stocks.api_key))
    # Catch errors
    if r.status_code != 200:
        raise Exception('Error: {}'.format(r.text))

    data = {
        'close': r.json()['latestPrice'],
        'change': r.json()['change'],
        'percentchange': r.json()['changePercent']
    }
    return data
