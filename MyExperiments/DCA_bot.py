import threading
from queue import Queue

import pandas as pd
from ta.trend import macd_diff
from ta.utils import dropna
from scipy import optimize

from Three_commasDCA_safety_order_calc import *


class DCABot(SaftyOrder):

    def __init__(self, data, takeProfitProcent):
        super().__init__(data, takeProfitProcent)
        self.result = Queue()
        # Declraing a lock
        self.lock = threading.Lock()

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

    # This does overfitting the stradegy
    def optimize_parameters(self, rranges, params):
        opt = optimize.brute(self.update_and_run, rranges, args=params, finish=None, workers=-1)
        return opt, -self.update_and_run(opt)

    def update_and_run(self, rranges, start_base_size, safety_order_size, max_active_safety_trades_count):
        (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale) = rranges

        kwargs = {"start_base_size": start_base_size,
                  "safety_order_size": safety_order_size,
                  "max_active_safety_trades_count": max_active_safety_trades_count,  # uninteresting
                  "safety_order_volume_scale": safety_order_volume_scale,
                  "price_deviation": price_deviation,
                  "max_safety_trades_count": max_safety_trades_count,
                  "safety_order_step_scale": safety_order_step_scale}
        result = self.calc_times_for_each_signal(kwargs)

        #self.result.put((result["uPNL"].sum(), result['Profit'].iloc[-1]))

        try:
            result["sum_profit"] = result["Profit"].cumsum()
            win = result['Profit'].iloc[-1] - result["uPNL"].sum()
        except:
            print("empty")
            return -10000
        return win
