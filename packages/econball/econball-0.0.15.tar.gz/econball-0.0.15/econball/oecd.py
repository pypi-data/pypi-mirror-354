"""A puller for OECD data using pandasdmx."""

# pylint: disable=unused-argument,line-too-long,unnecessary-lambda
import logging
from typing import List

import pandas as pd
import requests
from requests_cache.session import CachedSession


def pull(series: str, session: CachedSession) -> List[pd.Series]:
    """Pull time series from the OECD."""
    logging.info("Pulling OECD series %s", series)

    url = f"https://sdmx.oecd.org/public/rest/data/{series}?startPeriod=2010&endPeriod=2030&format=jsondata"
    response = requests.get(url, timeout=30.0)
    response.raise_for_status()
    data = response.json()
    data_val = data["data"]

    dimensions = data_val["structures"][0]["dimensions"]
    names = [
        x["name"]
        for x in [x["values"] for x in dimensions["series"] if x["id"] == "MEASURE"][0]
    ]
    ts_index = pd.DatetimeIndex(
        pd.to_datetime(
            [
                x["start"]
                for x in data_val["structures"][0]["dimensions"]["observation"][0][
                    "values"
                ]
            ]
        )
    )

    dataset_series = data_val["dataSets"][0]["series"]
    series_list = []
    for count, dataset_key in enumerate(dataset_series):
        observations = dataset_series[dataset_key]["observations"]
        observation_keys = sorted(observations.keys(), key=lambda x: int(x))

        series_list.append(
            pd.Series(
                name="_".join([series, names[count]]),
                data=[float(observations[x][0]) for x in observation_keys],
                index=ts_index,
            )
        )

    return series_list
