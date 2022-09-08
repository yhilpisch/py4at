#
# Python Module with Class
# for Vectorized Backtesting
# of Momentum-based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
from MomVectorBacktester import *


class MRVectorBacktester(MomVectorBacktester):
    ''' Class for the vectorized backtesting of
    Mean Reversion-based trading strategies.

    Attributes
    ==========
    symbol: str
        RIC symbol with which to work with
    start: str
        start date for row_data retrieval
    end: str
        end date for row_data retrieval
    amount: int, float
        amount to be invested at the beginning
    tc: float
        proportional transaction costs (e.g. 0.5% = 0.005) per trade

    Methods
    =======
    get_data:
        retrieves and prepares the base row_data set
    run_strategy:
        runs the backtest for the mean reversion-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    '''

    def run_strategy(self, SMA, threshold):
        ''' Backtests the trading strategy.
        '''
        data = self.data.copy().dropna()
        data['sma'] = data['price'].rolling(SMA).mean()
        data['distance'] = data['price'] - data['sma']
        data.dropna(inplace=True)
        # sell signals
        data['position'] = np.where(data['distance'] > threshold,
                                    -1, np.nan)
        # buy signals
        data['position'] = np.where(data['distance'] < -threshold,
                                    1, data['position'])
        # crossing of current price and SMA (zero distance)
        data['position'] = np.where(data['distance'] *
                                    data['distance'].shift(1) < 0,
                                    0, data['position'])
        data['position'] = data['position'].ffill().fillna(0)
        data['strategy'] = data['position'].shift(1) * data['return']
        # determine when a trade takes place
        trades = data['position'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc #second indexer is used as mask only in Pandas (Mask is an boolen Array) # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
        data['money'] = self.amount * data['return']
        data['creturns'] = self.amount * data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # absolute performance of the strategy
        aperf = self.results['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        operf = aperf - self.results['creturns'].iloc[-1]
        return round(aperf, 2), round(operf, 2)

    # This does overfitting the stradegy
    def optimize_parameters(self, *range):
        opt = brute(self.update_and_run, range, finish=None)
        return opt, -self.update_and_run(opt)

    def update_and_run(self, SMA):
        return -self.run_strategy(int(SMA[0]), int(SMA[1]))[0]


if __name__ == '__main__':
    """    mrbt = MRVectorBacktester('GDX', '2010-1-1', '2020-12-31',
                              10000, 0.0)
    pri£mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MRVectorBacktester('GDX', '2010-1-1', '2020-12-31',
                              10000, 0.001)
    print(mrbt.run_strategy(SMA=25, threshold=5))"""
    mrbt = MRVectorBacktester('GLD', '2010-1-1', '2020-12-31', 10000, 0.001)
    print("Best: ")
    print(mrbt.run_strategy(SMA=60, threshold=9.2))
    print("Best opt: ")
    # print(mrbt.optimize_parameters((10, 80, 2), (0, 11)))
    mrbt.plot_results()
