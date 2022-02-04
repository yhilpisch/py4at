#
# Python Module with Class
# for Vectorized Backtesting
# of SMA-based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
from scipy.optimize import brute
import matplotlib.pyplot as plt

testresult = pd.DataFrame()

class SMAVectorBacktester(object):
    ''' Class for the vectorized backtesting of SMA-based trading strategies.

    Attributes
    ==========
    symbol: str
        RIC symbol with which to work with
    SMA1: int
        time window in days for shorter SMA
    SMA2: int
        time window in days for longer SMA
    start: str
        start date for row_data retrieval
    end: str
        end date for row_data retrieval

    Methods
    =======
    get_data:
        retrieves and prepares the base row_data set
    set_parameters:
        sets one or two new SMA parameters
    run_strategy:
        runs the backtest for the SMA-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    update_and_run:
        updates SMA parameters and returns the (negative) absolute performance
    optimize_parameters:
        implements a brute force optimizeation for the two SMA parameters
    '''

    def __init__(self, symbol, SMA1, SMA2, start, end):
        self.symbol = symbol
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the row_data.
        '''
        raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv',
                          index_col=0, parse_dates=True).dropna() # dropna means that all NaN types raws will remove
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start:self.end]
        raw.rename(columns={self.symbol: 'price'}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1)) # # calculate the growing rate from div of price and shifted
        # ( last) price, with that it is easy to add (+) your stake ( normalized ). see math_play.py
        # Durch den Logaritmus lässt sich der Wachstumswert addieren! würde sonst nicht gehen, muss aber dann später wieder exponiert werden
        raw['SMA1'] = raw['price'].rolling(self.SMA1).mean() # Rolling Window means to move the row down on ... steps
        raw['SMA2'] = raw['price'].rolling(self.SMA2).mean() # mean is the middle ( approximation )
        # Plott price
        raw['price'].plot(title="Eur/Dol Price",figsize=(10, 6))
        plt.show()
        self.data = raw

    def set_parameters(self, SMA1=None, SMA2=None):
        ''' Updates SMA parameters and resp. time series.
        '''
        if SMA1 is not None:
            self.SMA1 = SMA1
            self.data['SMA1'] = self.data['price'].rolling(  # Rolling Window means to move the row down on ... steps
                self.SMA1).mean()
        if SMA2 is not None:
            self.SMA2 = SMA2
            self.data['SMA2'] = self.data['price'].rolling(self.SMA2).mean()

    def run_strategy(self):
        ''' Backtests the trading strategy.
        '''
        data = self.data.copy().dropna() # remove NaN Rows
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['return'] # Derives the log returns of the strategy given
        # the positionings and market returns
        data.dropna(inplace=True)
        data['creturns'] = data['return'].cumsum().apply(np.exp) # sums up the single log returns values for the stock
        # Any posetiv value in exp func is min 1
        testresult[self.SMA1] = data['creturns']
        #  ( for illustration only )
        # np.cumsum is the summ cell for cell
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp) # sums up the signle log returns values for  the
        # strategy ( for illustration only ). log and back with exp because of additive ability of logaritmus ( like decebil )
        # apply(np.exp) for the gross performance
        self.results = data
        # gross performance of the strategy
        aperf = data['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        # compared normal performence (creturns) with strategy performence ( cstrategy )
        operf = aperf - data['creturns'].iloc[-1]
        # General
        # Because of shifting and removing NaNs, there will be different signaled_data
        genperf = data['creturns'].iloc[-1]

        return round(aperf, 2), round(operf, 2),\
            round(genperf, 4), data['price'].iloc[0], data['price'].iloc[-1]

    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No signaled_data to plot yet. Run a strategy.')
        title = '%s | SMA1=%d, SMA2=%d' % (self.symbol,
                                               self.SMA1, self.SMA2)
        self.results[['creturns', 'cstrategy']].plot(title=title,
                                                     figsize=(10, 6))
        #plt.rcParams['savefig.dpi'] = 600
        #plt.savefig('filename.pdf')
        plt.show()

    def update_and_run(self, SMA):
        ''' Updates SMA parameters and returns negative absolute performance
        (for minimazation algorithm).

        Parameters
        ==========
        SMA: tuple
            SMA parameter tuple
        '''
        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.run_strategy()[0]

    def optimize_parameters(self, SMA1_range, SMA2_range):
        ''' Finds global maximum given the SMA parameter ranges.

        Parameters
        ==========
        SMA1_range, SMA2_range: tuple
            tuples of the form (start, end, step size)
        '''
        opt = brute(self.update_and_run, (SMA1_range, SMA2_range), finish=None)
        return opt, -self.update_and_run(opt)


if __name__ == '__main__':
    smabt = SMAVectorBacktester('EUR=', 42, 252,
                                '2010-1-1', '2020-12-31')
    print(smabt.run_strategy())
    smabt.plot_results( )


    smabt.set_parameters(SMA1=20, SMA2=100)
    print(smabt.run_strategy())
    smabt.plot_results()

    print(smabt.optimize_parameters((30, 56, 4), (200, 300, 4)))
