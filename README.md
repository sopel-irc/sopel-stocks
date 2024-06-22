# sopel-stocks

A stock lookup plugin for Sopel IRC bots

[![Python Tests](https://github.com/sopel-irc/sopel-stocks/actions/workflows/python-tests.yml/badge.svg?branch=master)](https://github.com/sopel-irc/sopel-stocks/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/sopel-stocks.svg)](https://badge.fury.io/py/sopel-stocks)

**Maintainer:** [@RustyBower](https://github.com/rustybower)


## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-stocks
```

### Requirements

This release of `sopel-stocks` requires Python 3.8+ and Sopel 8.0 or higher.

You will need an API key from one of the following providers:

* [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
* [Finnhub](https://finnhub.io/dashboard) (recommended)
* [IEX Cloud](https://iexcloud.io/console/tokens)


### Configuring

The easiest way to configure `sopel-stocks` is via Sopel's
configuration wizard—simply run `sopel-plugins configure stocks`
and enter the values for which it prompts you.

However, if you want or need to configure this plugin manually, you will need to
define the following in `~/.sopel/default.cfg`

    [stocks]
    api_key = API_KEY
    provider = finnhub (or alphavantage/iexcloud)


## Usage

    .stock msft
    <sopel> MSFT $123.37 1.6 (1.31%)⬆

    .stock aapl amzn goog
    <sopel> AAPL $150.83 -2.51 (-1.64%)⬇
    <sopel> AMZN $97.06 -5.38 (-5.25%)⬇
    <sopel> GOOG $90.445 -4.215 (-4.45%)⬇
