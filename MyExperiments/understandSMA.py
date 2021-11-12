
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv',
                   index_col=0, parse_dates=True).dropna()