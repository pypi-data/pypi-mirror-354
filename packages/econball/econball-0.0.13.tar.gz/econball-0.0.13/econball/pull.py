"""The pull function for fetching the economic data."""

# pylint: disable=line-too-long
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pandas as pd
import requests_cache
import tqdm
from requests_cache.session import CachedSession

from .coinbase import pull as coinbase_pull
from .data import Data
from .efd import pull as efd_pull
from .fred import pull as fred_pull
from .oecd import pull as oecd_pull
from .yfinance import pull as yfinance_pull

_DEFAULT_MANIFEST = {
    str(Data.FRED): {
        "ECBESTRVOLWGTTRMDMNRT": True,  # Euro Short-Term Rate: Volume-Weighted Trimmed Mean Rate
        "SOFR30DAYAVG": True,  # 30-Day Average SOFR
        "SOFR": True,  # Secured Overnight Financing Rate"
        "ADPWNUSNERSA": True,  # Total Nonfarm Private Payroll Employment
        "GDP": True,  # Gross Domestic Product
        "ECIWAG": True,  # Employment Cost Index: Wages and Salaries: Private Industry Workers
        "NFCI": True,  # Chicago Fed National Financial Conditions Index
        "EFFR": True,  # Effective Federal Funds Rate
        "DTP10J28": True,  # 10-Year 0.5% Treasury Inflation-Indexed Note
        "AMERIBOR": True,  # Overnight Unsecured AMERIBOR Benchmark Interest Rate
        "SOFR90DAYAVG": True,  # 90-Day Average SOFR
        "SOFRVOL": True,  # Secured Overnight Financing Volume
        "DFEDTARU": True,  # Federal Funds Target Range - Upper Limit
        "IUDSOIA": True,  # Daily Sterling Overnight Index Average (SONIA) Rate
        "BBKMGDP": True,  # Brave-Butters-Kelley Real Gross Domestic Product
        "ECBDFR": True,  # ECB Deposit Facility Rate for Euro Area
        "ECBESTRTOTVOL": True,  # Euro Short-Term Rate: Total Volume
        "DFEDTARL": True,  # Federal Funds Target Range - Lower Limit
        "CORESTICKM159SFRBATL": True,  # Sticky Price Consumer Price Index less Food and Energy
        "CPIAUCSL": True,  # Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        "GDPC1": True,  # Real Gross Domestic Product
        "MEDCPIM158SFRBCLE": True,  # Median Consumer Price Index
    },
    str(Data.YFINANCE): {
        # Equities
        "MSFT": True,  # Microsoft
        "NVDA": True,  # NVIDIA
        "F": True,  # Ford
        "AAPL": True,  # Apple
        "LCID": True,  # Lucid Group, Inc
        "AMZN": True,  # Amazon
        "PLTR": True,  # Palantir
        "APLD": True,  # Applied Digital Corporation
        "GOOG": True,  # Alphabet
        "TSLA": True,  # Tesla
        "META": True,  # Meta
        "WBD": True,  # Warner Bros. Discovery, Inc.
        "2222.SR": True,  # Saudi Arabian Oil Company
        # Forex
        "EURUSD=X": True,  # Euro to USD
        "JPY=X": True,  # Yen to USD
        "GBPUSD=X": True,  # Sterling to USD
        "AUDUSD=X": True,  # AUD to USD
        "NZDUSD=X": True,  # NZD to USD
        # Futures
        "ES=F": True,  # E-Mini S&P 500
        "YM=F": True,  # Mini Dow Jones
        "NQ=F": True,  # Nasdaq 100
        "RTY=F": True,  # E-mini Russell 2000
    },
    str(Data.COINBASE): {
        "BTC-USD": True,  # Bitcoin
        "XRP-USD": True,  # Ripple
        "ETH-USD": True,  # Ethereum
        "USDT-USD": True,  # Tether
        "SOL-USD": True,  # Solana
        # "USDC-USD": True,  # USDC
        "DOGE-USD": True,  # DOGE
    },
    str(Data.EFD): {
        "AAPL": True,  # Apple Senate Trades
        "MSFT": True,  # Microsoft Senate Trades
        "NVDA": True,  # Nvidia Senate Trades
        "F": True,  # Ford Senate Trades
        "LCID": True,  # Lucid Group, Inc
        "AMZN": True,  # Amazon
    },
    str(Data.OECD): {
        "OECD.TAD.ATM,DSD_AGR@DF_OUTLOOK_2021_2030,1.0/NOR.A.CPC_0141...": True,  # Agricultural Outlook Norway Soy Beans
    },
}
_DATA_PROVIDERS = {
    str(Data.FRED): fred_pull,
    str(Data.YFINANCE): yfinance_pull,
    str(Data.COINBASE): coinbase_pull,
    str(Data.EFD): efd_pull,
    str(Data.OECD): oecd_pull,
}


def pull(
    manifest: dict[str, dict[str, Any]] | None = None,
    min_date: datetime.date | None = None,
    session: CachedSession | None = None,
) -> pd.DataFrame:
    """Pull the latest economic data."""
    if manifest is None:
        manifest = _DEFAULT_MANIFEST
    if session is None:
        session = CachedSession(
            "econball",
            expire_after=requests_cache.NEVER_EXPIRE,
            allowable_methods=("GET", "HEAD", "POST"),
            stale_if_error=True,
        )
    series_pool = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for k, v in _DEFAULT_MANIFEST.items():
            futures.extend([executor.submit(_DATA_PROVIDERS[k], x, session) for x in v])
        for future in tqdm.tqdm(as_completed(futures), desc="Downloading"):
            series = future.result()
            series_pool.extend(series)
    series_pool = [
        s
        if isinstance(s.index, pd.DatetimeIndex)
        else pd.Series(s.values, index=pd.to_datetime(s.index), name=s.name)
        for s in series_pool
    ]
    df = pd.concat(series_pool, axis=1).sort_index().asfreq("D", method="ffill").ffill()
    if min_date is not None:
        df = df[df.index.date >= min_date]  # type: ignore
    df = df[df.index.date < datetime.datetime.today().date()]  # type: ignore
    return df
