import os
from datetime import datetime
from random import random

import numpy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def generate_simpel_sample_slope(rows=100, freq='1min') -> pd.DataFrame:
    rows = int(rows)
    # generate a DatetimeIndex object given the frequency
    index = pd.date_range('2021-1-1', periods=rows, freq=freq)
    row = np.linspace(rows, 1, num=rows)
    # generate the DataFrame object
    df = pd.DataFrame({"open": row, "buy": np.nan}, index=index)
    df["buy"][0] = 1
    return df


def add_candle_data(df):
    df["high"] = df["open"] + 0.5
    df["low"] = df["open"] - 0.5
    df["close"] = df["open"]
    df["volume"] = 100

def generate_simpel_sample_momentum(rows=100, freq='1min') -> pd.DataFrame:
    rows = int(rows)
    # generate a DatetimeIndex object given the frequency
    index = pd.date_range('2021-1-1', periods=rows * 2, freq=freq)
    row = np.append(np.linspace(rows, 1, num=rows), np.linspace(1, rows, num=rows))
    # generate the DataFrame object
    df = pd.DataFrame({"open": row, "buy": np.False_}, index=index)
    add_candle_data(df)
    df.loc['2021-1-1 00:00:00', "buy"] = True
    return df


# test:
# hshsh = generate_simpel_sample_momentum()
# print("test")

def get_data_from_file(start, end, file_name):
    ''' Retrieves and prepares the row_data.
    '''
    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    raw = pd.read_csv(
        os.getcwd()+'/historyCryptoData/' + file_name,
        index_col="date",  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
        parse_dates=True
    ).dropna()
    # upside down
    raw.info()
    raw = raw.reindex(index=raw.index[::-1]).loc[start:end]
    return raw
