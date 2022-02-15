import pandas as pd

''' Retrieves and prepares the row_data.
'''
raw = pd.read_csv(
    '/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/Binance_BTCUSDT_1h.csv',
    index_col=1,  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
    parse_dates=['date'])

# Classify date column by format type
raw['date'] = raw.index
raw['format'] = 1
raw.loc[raw.index.str.contains('-AM'), 'format'] = 2
raw.loc[raw.index.str.contains('-PM'), 'format'] = 2
#raw['new_date'] = pd.to_datetime(raw.index)
raw.info()
# Convert to datetime with two different format settings
raw.loc[raw.format == 1, 'new_date'] = pd.to_datetime(raw.loc[raw.format == 1, 'date'], format = '%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
raw.loc[raw.format == 2, 'new_date'] = pd.to_datetime(raw.loc[raw.format == 2, 'date'], format = '%Y-%m-%d %H-%p').dt.strftime('%Y-%m-%d %H:%M:%S')

raw['new_date'] = pd.to_datetime(raw['new_date'])
raw = raw.set_index('new_date', drop=True).drop(columns=["format", "date"])
raw.index.rename("date", inplace=True)
raw.to_csv('/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/Binance_BTCUSDT_1h_format.csv')
print("all Done")