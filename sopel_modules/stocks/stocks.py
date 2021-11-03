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


def name_scrubber(name):
    p = re.compile(',? (ltd|ltee|llc|corp(oration)?|inc(orporated)?|limited|plc)\.?$', re.I)
    return p.sub('', name)


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
            '{symbol} {d[currencySymbol]}' + bold('{d[close]:,.2f}')
        )

        # Use realtime data instead of yesterday's close when available
        if bot.config.stocks.provider == 'yahoo':
            data['close'] = data['price'];

        if not 'currencySymbol' in data:
            data['currencySymbol'] = "$"

        if 'name' in data:
            data['name'] = name_scrubber(data['name'])

        # Change is None, usually on IPOs
        if not data['change']:
            message = message.format(
                symbol=symbol.upper(),
                d=data,
            )
        # Otherwise, check change versus previous day
        else:
            if data['change'] >= 0:
                message += color(u' \u2b06 {d[change]:+,.2f} {d[percentchange]:+,.2f}%', colors.GREEN)
            else:
                message += color(u' \u2b07 {d[change]:+,.2f} {d[percentchange]:+,.2f}%', colors.RED)

            message = message.format(
                symbol=symbol.upper(),
                d=data,
            )

        # Current trading session data
        if bot.config.stocks.provider == 'yahoo':
            if data['marketState'] == "PRE":
                message += color(' (PREMARKET)', colors.LIGHT_GREY)

            if data['marketState'] == "POST":
                message += color(' (POSTMARKET)', colors.LIGHT_GREY)

            message2 = ' | '
            message2 += color('{d[low]:,.2f}', colors.RED) + '-'
            message2 += color('{d[high]:,.2f}', colors.GREEN)
            message2 += ' | Cap {d[cap]}';
            message = ('[{d[name]}] {message}' + message2).format(
                message=message,
                d=data
            )

        # Print results to channel
        return bot.say(message)
