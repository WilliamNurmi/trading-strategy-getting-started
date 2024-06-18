"""Get candlestick price and volume data from Binance.

"""

import requests
import datetime
import pandas as pd
import numpy as np
import logging
import shutil
import os

from types import NoneType
from typing import Dict, Literal, Iterable
from tqdm_loggable.auto import tqdm

from eth_defi.utils import to_unix_timestamp
from tradingstrategy.timebucket import TimeBucket
from pathlib import Path
from tradingstrategy.utils.time import (
    generate_monthly_timestamps,
    naive_utcnow,
    naive_utcfromtimestamp,
)
from tradingstrategy.utils.groupeduniverse import resample_series
from tradingstrategy.lending import (
    LendingCandleType,
    convert_binance_lending_rates_to_supply,
)
from tradingstrategy.types import PrimaryKey
from tradingstrategy.lending import convert_interest_rates_to_lending_candle_type_map
from tradingstrategy.binance.constants import BINANCE_SUPPORTED_QUOTE_TOKENS, split_binance_symbol, DAYS_IN_YEAR


logger = logging.getLogger(__name__)



class BitstampDownloader:

    def __init__(self):
        """"""
        
    def fetch_candlestick_data(
        self,
        symbols: list[str] | str,
        time_bucket: TimeBucket,
        start_at: datetime.datetime,
        end_at: datetime.datetime,
        force_download=False,
        desc="Reading Bitstamp data",
    ) -> pd.DataFrame:
        # Load the Bitstamp ETHBTC 1h data from a CSV file into a DataFrame
        bitstamp_ethbtc_df = pd.read_csv('../../data/Bitstamp_ETHBTC_1h.csv', skiprows=1)
        bitstamp_ethbtc_df['date'] = pd.to_datetime(bitstamp_ethbtc_df['date'])
        bitstamp_ethbtc_df.set_index('date', inplace=True)
        bitstamp_ethbtc_df.sort_index(ascending=True, inplace=True)

        # Remove the name of the index to match df
        bitstamp_ethbtc_df.index.name = None

        # Display the first few rows of the dataframe to verify correct loading
        bitstamp_ethbtc_df = bitstamp_ethbtc_df.drop(columns=['unix', 'Volume BTC'])
        bitstamp_ethbtc_df.rename(columns={'Volume ETH': 'volume'}, inplace=True)

        # Add a 'pair_id' column with a constant value as it's not present in the original DataFrame
        bitstamp_ethbtc_df['pair_id'] = 'ETHBTC'

        # Reorder columns to match the desired format
        bitstamp_ethbtc_df = bitstamp_ethbtc_df[['open', 'high', 'low', 'close', 'volume', 'pair_id']]

        return bitstamp_ethbtc_df


