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

    if not 'marketState' in q:
        raise Exception("Unable to parse market data for {}".format(symbol))

    if not 'regularMarketPrice' in q or not q['regularMarketPrice']:
        raise Exception("Unable to parse market data for {}".format(symbol))

    if 'currencySymbol' in q:
        if q['currencySymbol'] == "$" and q['currency'] == "CAD":
            cs = "C$"
        elif q['currencySymbol'] == "$" and q['currency'] != "USD":
            cs = q['currency'] + q['currencySymbol']
        else:
            cs = q['currencySymbol']
    else:
        cs = "$"

    cap = 'N/A'
    if 'fmt' in q['marketCap']:
        cap = cs + q['marketCap']['fmt']

    if q['quoteType'] == "EQUITY" and q['marketState'] == "PRE":
        data = {
            'price': q['preMarketPrice']['raw'],
            'change': q['preMarketChange']['raw'],
            'percentchange': q['preMarketChangePercent']['raw'] * 100,
            'low': q['regularMarketDayLow']['raw'],
            'high': q['regularMarketDayHigh']['raw'],
            'cap': cap,
            'name': q['longName'],
            'close': q['regularMarketPreviousClose']['raw'],
            'currencySymbol': cs,
            'marketState': q['marketState'],
        }
        return data

    if q['quoteType'] == "EQUITY" and ((
        q['marketState'] == "POST" or
        q['marketState'] == "POSTPOST") and
        'raw' in q['postMarketPrice']):
        data = {
            'price': q['postMarketPrice']['raw'],
            'change': q['postMarketChange']['raw'],
            'percentchange': q['postMarketChangePercent']['raw'] * 100,
            'low': q['regularMarketDayLow']['raw'],
            'high': q['regularMarketDayHigh']['raw'],
            'cap': cap,
            'name': q['longName'],
            'close': q['regularMarketPrice']['raw'],
            'rmchange': q['regularMarketChange']['raw'],
            'rmpercentchange': q['regularMarketChangePercent']['raw'] * 100,
            'currencySymbol': cs,
            'marketState': q['marketState'],
        }
        return data

    data = {
        'price': q['regularMarketPrice']['raw'],
        'change': q['regularMarketChange']['raw'],
        'percentchange': q['regularMarketChangePercent']['raw'] * 100,
        'low': q['regularMarketDayLow']['raw'],
        'high': q['regularMarketDayHigh']['raw'],
        'cap': cap,
        'name': q['longName'],
        'close': q['regularMarketPreviousClose']['raw'],
        'currencySymbol': cs,
        'marketState': q['marketState'],
    }
    return data
