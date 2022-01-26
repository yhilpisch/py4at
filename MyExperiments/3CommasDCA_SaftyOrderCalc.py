from random import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class DCABot(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.results = None
        self.data = self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''

        raw = pd.read_csv('/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/Binance_BTCUSDT_minute.csv',
                          index_col=1,  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
                          parse_dates=True).dropna().drop(columns="unix")
        raw = raw.loc[self.start:self.end]


        # raw.rename(columns={self.symbol: 'price'}, inplace=True)
        return raw

    def Get_Signals(self):
        data = self.data.copy().dropna() # remove NaN Rows
        price = data["open"]
        data['return'] = np.log(price / price.shift(1))
        data['grows'] = data['return'].rolling(60 * 3).mean()

        # sell signals
        data['sell'] = np.where(data['grows'] <= -0.00007, data["open"], np.nan)
        # buy signals
        data['buy'] = np.where(data['grows'] >= 0.0003, data["open"], np.nan)


        self.results = data

    # def calc_saftyOrders(self):



    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')

        #pltneu = self.results[['open']].plot(title="scheise", figsize=(10, 6))
        plt.plot(self.results['open'] )
        plt.plot(self.results['buy'], '^', markersize=6, color='g')
        plt.plot(self.results['sell'], 'v', markersize=6, color='r')

        ax = plt.gca()
        #ax.set_xlim([xmin, xmax])
        ax.set_ylim([self.results["open"].min(), self.results["open"].max()])

        #plt.rcParams['savefig.dpi'] = 600
        #plt.savefig('filename.pdf')
        plt.show()

if __name__ == '__main__':
    lala = DCABot('2022-1-04', '2022-01-06')
    lala.Get_Signals()
    lala.plot_results()
    print("test")