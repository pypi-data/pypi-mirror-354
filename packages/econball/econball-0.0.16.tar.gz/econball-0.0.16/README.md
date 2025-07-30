# econball

<a href="https://pypi.org/project/econball/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/econball">
</a>

A library for pulling in and normalising economic data.

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [pyarrow](https://arrow.apache.org/docs/python/index.html)
- [fredapi](https://pandas.pydata.org/)
- [tqdm](https://github.com/tqdm/tqdm)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
- [yfinance](https://ranaroussi.github.io/yfinance/)
- [cbhist](https://github.com/8W9aG/cbhist)
- [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)
- [lxml](https://lxml.de/)
- [requests-cache](https://requests-cache.readthedocs.io/en/stable/)
- [python-dateutil](https://github.com/dateutil/dateutil)
- [pandasdmx](https://pandasdmx.readthedocs.io/en/v1.0/)

## Raison D'être :thought_balloon:

`econball` aims to be a library for pulling in historical information about economic indicators and pricing. All its about is in timeseries denoted by days.

## Architecture :triangular_ruler:

`econball` is a functional library which simply aims to pull down and normalise as much economic data as possible. Within it there are different pullers for various forms of economic data, all outputting a single time series representing the entity. The data that it pulls down is:

1. FRED: Macroeconomic Signals
2. YFinance: Equity Tickers
3. Coinbase: Crypto Tickers
4. EFD: Senate Trades
5. OECD

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install econball`

or install using this local repository:

`python setup.py install --old-and-unmanageable`

## Usage example :eyes:

The use of `tsuniverse` is entirely through code due to it being a library. It attempts to hide most of its complexity from the user, so it only has a few functions of relevance in its outward API.

### Generating Features

To generate features:

```python
from econball.pull import pull

df = pull()
```

## License :memo:

The project is available under the [MIT License](LICENSE).
