# coding=utf-8
"""
stocks.py - Sopel Stocks Plugin
"""
import re
import requests
from datetime import datetime, timedelta
from sopel.config.types import NO_DEFAULT, ChoiceAttribute, StaticSection, ValidatedAttribute
from sopel.formatting import bold, color, colors
from sopel.logger import get_logger
from sopel.module import commands, example, NOLIMIT

from .providers.alphavantage import alphavantage
from .providers.iexcloud import iexcloud
from .providers.yahoo import yahoo

logger = get_logger(__name__)


STOCK_PROVIDERS = [
    'alphavantage',
    'iexcloud',
    'yahoo'
]


# Define our sopel stocks configuration
class StocksSection(StaticSection):
    provider = ChoiceAttribute(
        'provider',
        STOCK_PROVIDERS,
        default=NO_DEFAULT
    )
    api_key = ValidatedAttribute('api_key', default=NO_DEFAULT)


def setup(bot):
    bot.config.define_section('stocks', StocksSection)


# Walk the user through defining variables required
def configure(config):
    config.define_section('stocks', StocksSection, validate=False)
    config.stocks.configure_setting(
        'provider',
        'Enter stocks provider ({}):'.format(', '.join(STOCK_PROVIDERS)),
        default=NO_DEFAULT
    )
    config.stocks.configure_setting(
        'api_key',
        'Enter provider API key:',
        default=NO_DEFAULT
    )


def get_price(bot, symbol):
    # Alphavantage
    if bot.config.stocks.provider == 'alphavantage':
        return alphavantage(bot, symbol)
    # IEX Cloud
    elif bot.config.stocks.provider == 'iexcloud':
        return iexcloud(bot, symbol)
    # Yahoo Finance
    elif bot.config.stocks.provider == 'yahoo':
        return yahoo(bot, symbol)
    # Unsupported Provider
    else:
        raise Exception('Error: Unsupported Provider')


@commands('stock')
@example('.stock msft')
def stock(bot, trigger):
    """Get the current price for a given stock."""
    # If the user types .stock with no arguments, let them know proper usage
    if not trigger.group(2):
        return
    else:
        # Get symbol
        symbol = trigger.group(2)

        # Do regex checking on symbol to ensure it's valid
        if bot.config.stocks.provider == 'yahoo':
            if not re.match('^[a-zA-Z0-9]{1,10}(\.[a-zA-Z0-9]{1,10})?$', symbol):
                bot.say('Invalid Symbol')
                return
        else:
            if not re.match('^[a-zA-Z0-9]{1,10}(:[a-zA-Z0-9]{1,10})?$', symbol):
                bot.say('Invalid Symbol')
                return

        # Get data from API
        try:
            data = get_price(bot, symbol)
        except Exception as e:
            return bot.say(str(e))

        message = (
            '{symbol} {currencySymbol}' + bold('{close:0.2f}')
        )

        # Use realtime data instead of yesterday's close when available
        if bot.config.stocks.provider == 'yahoo':
            data['close'] = data['price'];

        if not 'currencySymbol' in data:
            data['currencySymbol'] = "$"

        # Change is None, usually on IPOs
        if not data['change']:
            message = message.format(
                symbol=symbol.upper(),
                currencySymbol=data['currencySymbol'],
                close=data['close'],
            )
        # Otherwise, check change versus previous day
        else:
            if data['change'] >= 0:
                message += color(' ({change:+0.2f} {percentchange:+0.2f}%) \u2b06', colors.GREEN)
            else:
                message += color(' ({change:+0.2f} {percentchange:+0.2f}%) \u2b07', colors.RED)

            message = message.format(
                symbol=symbol.upper(),
                currencySymbol=data['currencySymbol'],
                close=data['close'],
                change=data['change'],
                percentchange=data['percentchange'],
            )

        # Current trading session data
        if bot.config.stocks.provider == 'yahoo':
            if data['marketState'] == "PRE":
                message2 = ' | ' + color('PREMARKET', colors.GREY);
                message += message2

            if data['marketState'] == "POST":
                message2 = ' | ' + color('POSTMARKET', colors.GREY);
                message += message2

            message2 = ' | '
            message2 += color('L {low:0.2f} ', colors.RED);
            message2 += color('H {high:0.2f} ', colors.GREEN);
            message2 += '| {name} | Cap {cap}';
            message += message2.format(
               low=data['low'],
               high=data['high'],
               name=data['name'],
               cap=data['cap'],
            )

        # Print results to channel
        return bot.say(message)
