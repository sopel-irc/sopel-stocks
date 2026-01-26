"""Finnhub data provider for Sopel stocks plugin"""
import requests

from sopel.tools import get_logger

logger = get_logger('stocks')


def finnhub(bot, symbol):
    r = requests.get(
        "https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}".format(
            symbol=symbol.upper(), api_key=bot.config.stocks.api_key
        )
    )

    logger.info("Finnhub API response for %s: %s", symbol, r.text)

    if not r.json():
        raise Exception("An error occurred.")

    close = r.json()['c']
    # prevclose = r.json()['pc']
    change = r.json()['d']
    percentchange = r.json()['dp']

    data = {"close": close, "change": change, "percentchange": percentchange}
    return data
