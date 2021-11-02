# coding=utf-8
import requests


def yahoo(bot, symbol):
    url = 'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{symbol}'.format(symbol=symbol)
    yparams = {'modules': 'price'}
    yheaders = {'User-Agent': 'sopel.chat'} # Yahoo ignores the default python requests ua

    r = requests.get(url, params=yparams, headers=yheaders)

    # Catch errors
    if r.status_code == 400 and 'finance' in r.json():
        e = r.json()['finance']['error']
        raise Exception("Yahoo API Error: {}: {}".format(e['code'], e['description']))

    if r.status_code == 404 and 'quoteSummary' in r.json():
        e = r.json()['quoteSummary']['error']
        raise Exception(e['description'])

    if r.status_code != 200:
        raise Exception('HTTP Error {}: {}'.format(r.status_code, r.text))

    q = r.json()['quoteSummary']['result'][0]['price']

    if q['marketState'] == "PRE":
        data = {
            'price': q['preMarketPrice']['raw'],
            'change': q['preMarketChange']['raw'],
            'percentchange': q['preMarketChangePercent']['raw'] * 100,
            'low': q['regularMarketDayLow']['raw'],
            'high': q['regularMarketDayHigh']['raw'],
            'cap': q['marketCap']['fmt'],
            'name': q['longName'].rsplit(',', 1)[0],
            'close': q['regularMarketPreviousClose']['raw'],
            'currencySymbol': q['currencySymbol'],
            'marketState': q['marketState'],
        }
        return data

    if q['marketState'] == "POST":
        data = {
            'price': q['postMarketPrice']['raw'],
            'change': q['postMarketChange']['raw'],
            'percentchange': q['postMarketChangePercent']['raw'] * 100,
            'low': q['regularMarketDayLow']['raw'],
            'high': q['regularMarketDayHigh']['raw'],
            'cap': q['marketCap']['fmt'],
            'name': q['longName'].rsplit(',', 1)[0],
            'close': q['regularMarketPreviousClose']['raw'],
            'currencySymbol': q['currencySymbol'],
            'marketState': q['marketState'],
        }
        return data

    data = {
        'price': q['regularMarketPrice']['raw'],
        'change': q['regularMarketChange']['raw'],
        'percentchange': q['regularMarketChangePercent']['raw'] * 100,
        'low': q['regularMarketDayLow']['raw'],
        'high': q['regularMarketDayHigh']['raw'],
        'cap': q['marketCap']['fmt'],
        'name': q['longName'].rsplit(',', 1)[0],
        'close': q['regularMarketPreviousClose']['raw'],
        'currencySymbol': q['currencySymbol'],
        'marketState': q['marketState'],
    }
    return data
