import datetime
import os

import pandas as pd
from pathlib import Path
import fileinput
import sys

filepath = '/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments/historyCryptoData/'


def set_format(filename):
    for line_number, line in enumerate(fileinput.input(filepath + filename, inplace=1)):
        if line.startswith("https://www.CryptoDataDownload.com"):
            continue
        sys.stdout.write(line)

    raw = pd.read_csv(filepath + filename,
                      index_col=1,  # ist wichtig Index muss Datum sein sonst geht raw.loc[ nicht
                      parse_dates=['date'])

    raw['date'] = raw.index

    if isinstance(raw.index, pd.DatetimeIndex):
        print(filename + ": no Format Errors")
        return

    try:
        # Classify date column by format type
        raw['format'] = 1
        raw.loc[raw.index.str.contains('-AM'), 'format'] = 2
        raw.loc[raw.index.str.contains('-PM'), 'format'] = 2
    except:
        print(filename + " error format")
        return

    raw.info()
    # Convert to datetime with two different format settings
    raw.loc[raw.format == 1, 'new_date'] = pd.to_datetime(raw.loc[raw.format == 1, 'date'],
                                                          format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
    raw.loc[raw.format == 2, 'new_date'] = pd.to_datetime(raw.loc[raw.format == 2, 'date'],
                                                          format='%Y-%m-%d %H-%p').dt.strftime('%Y-%m-%d %H:%M:%S')

    raw['new_date'] = pd.to_datetime(raw['new_date'])
    raw = raw.set_index('new_date', drop=True).drop(columns=["format", "date"])
    raw.index.rename("date", inplace=True)
    raw.to_csv(filepath + "{filename}_format.csv".format(filename=filename))
    os.remove(filepath + filename)
    print(filename + ": all Done")


for path in Path(filepath).glob("*.csv"):
    set_format(path.name)
