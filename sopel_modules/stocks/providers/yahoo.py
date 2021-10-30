# coding=utf-8
import requests


def yahoo(bot, symbol):
    url = 'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{symbol}'.format(symbol=symbol)
    yparams = {'modules': 'price'}
    yheaders = {'User-Agent': 'sopel.chat'} # Yahoo ignores the default python requests ua

    r = requests.get(url, params=yparams, headers=yheaders)
    # Catch errors
    if r.status_code != 200:
        raise Exception('Error: {}'.format(r.text))

    data = {
        'price': r.json()['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw'],
        'change': r.json()['quoteSummary']['result'][0]['price']['regularMarketChange']['raw'],
        'percentchange': r.json()['quoteSummary']['result'][0]['price']['regularMarketChangePercent']['raw'] * 100,
        'low': r.json()['quoteSummary']['result'][0]['price']['regularMarketDayLow']['raw'],
        'high': r.json()['quoteSummary']['result'][0]['price']['regularMarketDayHigh']['raw'],
        'cap': r.json()['quoteSummary']['result'][0]['price']['marketCap']['fmt'],
        'name': r.json()['quoteSummary']['result'][0]['price']['shortName'],
        'close': r.json()['quoteSummary']['result'][0]['price']['regularMarketPreviousClose']['raw']
        # name = name.rsplit(',', maxsplit=1)[0]
    }
    return data
