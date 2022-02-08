from random import random

import numpy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from Generating_test_Data import *
from itertools import islice


class DCABot(object):

    def __init__(self, data, takeProfitProcent):
        self.signaled_data = data
        self.row_data = data
        self.take_profit_percent = takeProfitProcent

    def Get_Signals(self):
        data = self.row_data.copy().dropna()  # remove NaN Rows
        price = data["open"]
        data['return'] = np.log(price / price.shift(1))
        data['grows'] = data['return'].rolling(60 * 3).mean()

        # sell signals
        data['sell'] = np.where(data['grows'] <= -0.00007, data["open"], np.nan)
        # buy signals
        data['buy'] = np.where(data['grows'] >= 0.0003, data["open"], np.nan)

        self.signaled_data = data

    def calc_safty_orders(self,
                          signal_enter_df,
                          start_base_size,  # First enter amount
                          safety_order_size,  # Enter the amount of funds your Safety Orders will use to Average the
                          # cost of the asset being traded, this can help your bot to close deals faster with more
                          # profit. Safety Orders are also known as Dollar Cost Averaging and help when prices moves
                          # in the opposite direction to your bot's take profit target.
                          max_active_safety_trades_count,  # This is the amount of Safety Orders the bot is allowed
                          # to place in advance on the exchange's order book for the asset being traded. A high
                          # number of Active Safety Orders will lock and reserve more funds for a running bot deal.
                          safety_order_volume_scale,  # The Safety Order Volume Scale is used to multiply the amount
                          # of funds used by the last Safety Order that was created
                          price_deviation,  # Price deviation to open safety orders (% from initial order)
                          max_safety_trades_count,  # This is the total number of Safety Orders the bot is allowed to
                          # use per deal that is opened. All Safety Orders created by the bot are placed as Limit
                          # Orders on the exchange's order book.
                          safety_order_step_scale  # The Safety Order Step Scale is used to multiply the Price
                          # Deviation percentage used by the last Safety Order placed on the exchange account.
                          ):
        # for index, row in Signal_Enter_df.iterrows():
        #     print(type(row['open']))

        # startBuySigRow = SignalEnterIter[0]
        start_buy_price = signal_enter_df.iloc[0]['open']
        start_time = signal_enter_df.iloc[0][0]
        take_profit_price = start_buy_price * (1 + self.take_profit_percent)
        quantity = start_base_size / start_buy_price
        next_safety_order_price = start_buy_price - (price_deviation / 100 * start_buy_price)
        max_safety_trades_counter = 0
        safety_buys = pd.DataFrame(
            data={'vol': [quantity], 'price': [start_buy_price], 'payed': [quantity * start_buy_price]})
        safety_buys["payed_Sum"] = safety_buys["payed"].cumsum()

        for index, candle in signal_enter_df.iloc[1:].iterrows():
            next_price = candle['open']
            if next_price > take_profit_price:
                profit = take_profit_price * safety_buys["vol_Sum"].iloc[-1] - safety_buys["payed_Sum"].iloc[-1]
                return prepare_return_values(signal_enter_df, index,
                                             next_safety_order_price,
                                             max_safety_trades_counter,
                                             self.take_profit_percent,
                                             profit=profit)

            if max_safety_trades_counter >= max_safety_trades_count:
                continue

            if next_price < next_safety_order_price:
                max_safety_trades_counter += 1
                # Buy
                quantity = safety_order_size * (
                            safety_order_volume_scale ** max_safety_trades_counter) / next_safety_order_price
                # collect data
                safety_buys = safety_buys.append({'vol': quantity, 'price': next_safety_order_price}, ignore_index=True)
                safety_buys["payed"] = (safety_buys['vol'] * safety_buys['price'])
                safety_buys["payed_Sum"] = safety_buys["payed"].cumsum()
                safety_buys["vol_Sum"] = safety_buys["vol"].cumsum()
                safety_buys["average_price"] = safety_buys["payed_Sum"] / safety_buys["vol_Sum"]
                # Get new average buy price
                take_profit_price = safety_buys["average_price"].iloc[-1] * (1 + self.take_profit_percent)
                # Next price
                if safety_order_step_scale == 1:
                    scale = (max_safety_trades_counter + 1)
                else:
                    scale = safety_order_step_scale ** (max_safety_trades_counter + 1)
                next_safety_order_price = start_buy_price - scale * price_deviation / 100 * start_buy_price

        #  print("Out of chart history")
        uPNL = safety_buys['payed_Sum'].iloc[-1]
        return prepare_return_values(signal_enter_df, index,
                                     next_safety_order_price,
                                     max_safety_trades_counter,
                                     self.take_profit_percent,
                                     uPNL=uPNL,)

    def calc_times_for_each_signal(self, args):
        results = []
        for chart_selection in self.buy_signal():
            results.append(self.calc_safty_orders(chart_selection, **args))
        return pd.DataFrame(results)

    def buy_signal(self):
        for i, val in enumerate(self.signaled_data['buy']):
            if not numpy.isnan(val):
                yield self.signaled_data[i:]

    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.signaled_data is None:
            print('No signaled_data to plot yet. Run a strategy.')

        # pltneu = self.signaled_data[['open']].plot(title="scheise", figsize=(10, 6))
        plt.plot(self.signaled_data['open'])
        plt.plot(self.signaled_data['buy'], '^', markersize=6, color='g')
        plt.plot(self.signaled_data['sell'], 'v', markersize=6, color='r')

        ax = plt.gca()
        # ax.set_xlim([xmin, xmax])
        ax.set_ylim([self.signaled_data["open"].min(), self.signaled_data["open"].max()])

        # plt.rcParams['savefig.dpi'] = 600
        # plt.savefig('filename.pdf')
        plt.show()


def prepare_return_values(signal_enter_df, index, price_exit, max_safety_trades_counter, percent,
                        profit=0,
                        uPNL = 0,):
    return {"duration": signal_enter_df.index[0] - index,
            "Price Enter": signal_enter_df.iloc[0]['open'],
            "Price Exit": price_exit,
            "max_safety_trades_counter": max_safety_trades_counter,
            "in Percent": percent,
            "uPNL": uPNL,
            "Profit": profit}


def real_data_test():
    data = get_data_from_file('2022-1-04', '2022-01-06')
    lala = DCABot(data, 0.09)
    lala.Get_Signals()
    # lala.plot_results()
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,
              "safety_order_volume_scale": 1,
              "price_deviation": 1,
              "max_safety_trades_count": 1,
              "safety_order_step_scale": 1}
    result = lala.calc_times_for_each_signal(kwargs)
    print(result)
    print("End")


def fake_data_test():
    data = generate_simpel_sample_momentum()
    lala = DCABot(data, 0.01)
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,  # uninteresting
              "safety_order_volume_scale": 1.1,
              "price_deviation": 1,
              "max_safety_trades_count": 10,
              "safety_order_step_scale": 1}
    result = lala.calc_times_for_each_signal(kwargs)
    print(result)
    print("End")


if __name__ == '__main__':
    real_data_test()
    #fake_data_test()
