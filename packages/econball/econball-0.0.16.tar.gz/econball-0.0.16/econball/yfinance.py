"""A puller for yahoo finance data."""

# pylint: disable=global-statement,unused-argument
import logging

import curl_cffi
import pandas as pd
import yfinance as yf  # type: ignore
from requests_cache.session import CachedSession


def pull(series: str, session: CachedSession) -> list[pd.Series]:
    """Pull the yfinance data."""
    logging.info("Pulling yfinance series %s", series)
    series_name = "yfinance_" + series
    try:
        df = yf.Ticker(series).history(start="2000-01-01")
        df.index = df.index.date  # type: ignore
        df = df.sort_index()
        return [
            df["Close"].rename(series_name + "_close"),
            df["Volume"].rename(series_name + "_volume"),
        ]
    except curl_cffi.requests.exceptions.HTTPError as exc:
        logging.warning(str(exc))
        logging.warning("Could not pull %s", series)
        return []
