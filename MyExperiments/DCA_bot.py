from queue import Queue

from scipy import optimize
from ta.trend import macd_diff
from ta.utils import dropna

from MyExperiments.Three_commasDCA_safety_order_calc import *


class DCABot(SaftyOrder):

    s_result = Queue()

    def __init__(self, data, take_profit_percent, capital_limit=math.inf):
        super().__init__(data, take_profit_percent, capital_limit)

    def get_signals_general(self):
        df = dropna(self.row_data)
        df["macd"] = macd_diff(close=df["close"])
        c_max = df['macd'].max()
        c_min = c_max * 0.45
        buy_signal = df['macd'].map(lambda x: c_min < x < c_max)
        self.filter_signals(buy_signal, df)

    def get_signals(self):
        # Clean NaN values
        df = dropna(self.row_data)

        df["macd"] = macd_diff(close=df["close"])
        buy_signal = df['macd'].map(lambda x: 60 < x < 69)
        self.filter_signals(buy_signal, df)

    def filter_signals(self, buy_signal, df):
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
        return opt, -self.update_and_run((opt[0], opt[1], opt[2], opt[3]), *params)

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

        # not working, dont know way
        # DCABot.s_result.put((result["uPNL"].sum(), result['Profit'].iloc[-1]))

        try:
            win = result['Profit'].sum() - result["uPNL"].sum()
        except:
            print("empty")
            return -10000
        return -win
