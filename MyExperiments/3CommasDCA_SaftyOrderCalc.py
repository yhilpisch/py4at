from random import random

import numpy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class DCABot(object):

    def __init__(self, start, end, takeProfitProcent):
        self.start = start
        self.end = end
        self.results = None
        self.data = self.get_data()
        self.take_profit_procent = takeProfitProcent

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''

        raw = pd.read_csv(
            '/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/Binance_BTCUSDT_minute.csv',
            index_col=1,  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
            parse_dates=True).dropna().drop(columns="unix")
        raw = raw.loc[self.start:self.end]

        # raw.rename(columns={self.symbol: 'price'}, inplace=True)
        return raw

    def Get_Signals(self):
        data = self.data.copy().dropna()  # remove NaN Rows
        price = data["open"]
        data['return'] = np.log(price / price.shift(1))
        data['grows'] = data['return'].rolling(60 * 3).mean()

        # sell signals
        data['sell'] = np.where(data['grows'] <= -0.00007, data["open"], np.nan)
        # buy signals
        data['buy'] = np.where(data['grows'] >= 0.0003, data["open"], np.nan)

        self.results = data

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
        take_profit_price = start_buy_price * (1 + self.take_profit_procent)
        quantity = start_base_size / start_buy_price
        next_safety_order_price = start_buy_price - (safety_order_step_scale * price_deviation / 100 * start_buy_price)
        max_safety_trades_counter = 0

        for index, candle in signal_enter_df.iterrows():
            next_price = candle['open']
            if next_price > take_profit_price:
                return prepare_return_values(signal_enter_df, index, candle, max_safety_trades_counter)

            if max_safety_trades_counter > max_active_safety_trades_count:
                continue

            if next_price < next_safety_order_price:
                max_safety_trades_counter += 1
                quantity += safety_order_size * (safety_order_volume_scale ** max_safety_trades_counter) / next_price
                next_safety_order_price = start_buy_price - (max_safety_trades_counter ** (
                        safety_order_step_scale * price_deviation) / 100 * start_buy_price)

        print("Out of chart history")
        return prepare_return_values(signal_enter_df, index, candle, max_safety_trades_counter)

    def calc_times_for_each_signal(self, args):
        for chart_selection in self.buy_signal():
            return self.calc_safty_orders(chart_selection, **args)

    def buy_signal(self):
        for i, val in enumerate(self.results['buy']):
            if not numpy.isnan(val):
                yield self.results[i:]

    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')

        # pltneu = self.results[['open']].plot(title="scheise", figsize=(10, 6))
        plt.plot(self.results['open'])
        plt.plot(self.results['buy'], '^', markersize=6, color='g')
        plt.plot(self.results['sell'], 'v', markersize=6, color='r')

        ax = plt.gca()
        # ax.set_xlim([xmin, xmax])
        ax.set_ylim([self.results["open"].min(), self.results["open"].max()])

        # plt.rcParams['savefig.dpi'] = 600
        # plt.savefig('filename.pdf')
        plt.show()


def prepare_return_values(signal_enter_df, index, candle, max_safety_trades_counter):
    return {"duration": signal_enter_df.index[0] - index,
            "Price Enter": signal_enter_df.iloc[0]['open'],
            "Price Exit": candle['open'],
            "max_safety_trades_counter": max_safety_trades_counter}


if __name__ == '__main__':
    lala = DCABot('2022-1-04', '2022-01-06', 0.09)
    lala.Get_Signals()
    # lala.plot_results()
    kwargs = {"start_base_size": 1,
              "safety_order_size": 1,
              "max_active_safety_trades_count": 1,
              "safety_order_volume_scale": 1,
              "price_deviation": 1,
              "max_safety_trades_count": 1,
              "safety_order_step_scale": 1}
    result = lala.calc_times_for_each_signal(kwargs)
    print(result)
    print("End")
