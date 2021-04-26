[![Python Tests](https://github.com/sopel-irc/sopel-stocks/actions/workflows/python-tests.yml/badge.svg?branch=master)](https://github.com/sopel-irc/sopel-stocks/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/sopel-modules.stocks.svg)](https://badge.fury.io/py/sopel-modules.stocks)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/sopel-irc/sopel-stocks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sopel-irc/sopel-stocks/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/sopel-irc/sopel-stocks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sopel-irc/sopel-stocks/context:python)

**Maintainer:** [@RustyBower](https://github.com/rustybower)

# sopel-stocks
sopel-stocks is an stock lookup plugin for Sopel

## Installing
If possible, use `pip` to install this plugin. Below are example commands; you
might need to add `sudo` and/or call a different `pip` (e.g. `pip3`) depending
on your system and environment. Do not use `setup.py install`; Sopel won't be
able to load the plugin correctly.

#### Published release

    pip install sopel-modules.stocks

#### From source

    # Clone the repo, then run this in /path/to/sopel-stocks
    pip install .

## Configuring
You can automatically configure this plugin using the `sopel configure --plugins` command.

However, if you want or need to configure this plugin manually, you will need to define the following in `~/.sopel/default.cfg`

    [stocks]
    api_key = API_KEY
    provider = alphavantage (or iexcloud)

## Requirements
#### API Key

    https://www.alphavantage.co/support/#api-key
    https://iexcloud.io/console/tokens

#### Python Requirements

    requests
    sopel

## Usage

    .stock djia
    DJIA $26559.5 110 (0.42%)⬆
    
    .stock msft
    MSFT $123.37 1.6 (1.31%)⬆
