import pandas as pd
from ta.trend import macd_diff
from ta.utils import dropna

from Three_commasDCA_safety_order_calc import *


class DCABot(SaftyOrder):

    def get_signals(self):
        # Clean NaN values
        df = dropna(self.row_data)

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
        print("Signals amount: " + str(buy_signal.sum()))
        df['buy'] = buy_signal
        self.signaled_data = df


