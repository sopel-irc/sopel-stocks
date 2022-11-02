# coding=utf-8
"""
stocks.py - Sopel Stocks Plugin
"""
import re
from datetime import datetime, timedelta
from sopel.config.types import NO_DEFAULT, ChoiceAttribute, StaticSection, ValidatedAttribute
from sopel.formatting import color, colors
from sopel.logger import get_logger
from sopel.module import commands, example

from .providers.alphavantage import alphavantage
from .providers.iexcloud import iexcloud

logger = get_logger(__name__)


STOCK_PROVIDERS = [
    'alphavantage',
    'iexcloud',
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
    # Unsupported Provider
    else:
        raise Exception('Error: Unsupported Provider')


@commands('stock')
@example('.stock msft')
@example('.stock amzn msft goog')
def stock(bot, trigger):
    """Get the current price for given stock(s)."""
    # If the user types .stock with no arguments, let them know proper usage
    if not trigger.group(2):
        return
    else:
        # Get symbol
        symbols = trigger.group(2).split()

        # Do regex checking on symbol to ensure it's valid
        symbols = [symbol for symbol in symbols if re.match('^([a-zA-Z0-9]{1,10}:[a-zA-Z0-9]{1,10}|[a-zA-Z0-9]{1,10})$', symbol)]

        # Get data from API
        for symbol in symbols:
            try:
                data = get_price(bot, symbol)
            except Exception as e:
                return bot.say(str(e))

            message = (
                '{symbol} ${close:g} '
            )

            # Change is None, usually on IPOs
            if not data['change']:
                message = message.format(
                    symbol=symbol.upper(),
                    close=float(data['close']),
                )
            # Otherwise, check change versus previous day
            else:
                if data['change'] >= 0:
                    message += color('{change:g} ({percentchange:.2f}%)', colors.GREEN)
                    message += color(u'\u2b06', colors.GREEN)
                else:
                    message += color('{change:g} ({percentchange:.2f}%)', colors.RED)
                    message += color(u'\u2b07', colors.RED)

                message = message.format(
                    symbol=symbol.upper(),
                    close=float(data['close']),
                    change=float(data['change']),
                    percentchange=float(data['percentchange']),
                )

            # Print results to channel
            bot.say(message)
        return
