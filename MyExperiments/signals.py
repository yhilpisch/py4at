import numpy as np
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import macd_diff
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from matplotlib import pyplot as plt


df = generate_simpel_sample_momentum()
#df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")
df["macd"] = macd_diff(close=df["close"])

print("yes")

# Load datas
df = pd.read_csv(
    '/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/Binance_BTCUSDT_minute.csv',
    index_col=1,  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
    parse_dates=True).dropna().drop(columns="unix")
df = df.loc['2021-12-04':'2022-01-04']
# Clean NaN values
df = dropna(df)

df["macd"] = macd_diff(close=df["close"])
buy_signal = df['macd'].map(lambda x: 60 < x < 69)
# filtering signals, because just one in series is needed
a = 0
for i, v in enumerate(buy_signal):
    if v and a == 0:
        a = 10
        continue
    if a > 0:
        buy_signal[i] = False
        a -= 1
print("Signals amount" + str(buy_signal.sum()))
# df["buy_signal"] = np.where(df['macd'] > 60, df['macd'], np.nan)
plt.figure(dpi=600)
plt.plot(df["close"])
plt.plot(df["close"][buy_signal], '^', markersize=1, color='g')
plt.show()







#  Beispiel von Github
# Add all ta features
df = add_all_ta_features(
    df, open="open", high="high", low="low", close="close", volume="Volume BTC")


# Load datas
df = pd.read_csv('ta/tests/data/datas.csv', sep=',')

# Clean NaN values
df = dropna(df)

# Initialize Bollinger Bands Indicator
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)


# Add Bollinger Bands features
df['bb_bbm'] = indicator_bb.bollinger_mavg()
df['bb_bbh'] = indicator_bb.bollinger_hband()
df['bb_bbl'] = indicator_bb.bollinger_lband()

# Add Bollinger Band high indicator
df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

# Add Bollinger Band low indicator
df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

# Add Width Size Bollinger Bands
df['bb_bbw'] = indicator_bb.bollinger_wband()

# Add Percentage Bollinger Bands
df['bb_bbp'] = indicator_bb.bollinger_pband()