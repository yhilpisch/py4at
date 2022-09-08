from typing import Union

from ch03.sample_data import generate_sample_data
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

window = 3

data = generate_sample_data(10,1)
data.columns.values[0] = "orig"

#Rolling verschiebt die Tabele nur und vergleicht dann die werte je nach befehl (max,min ...)
data["max"] = data["orig"].rolling(window).max()
data["min"] = data["orig"].rolling(window).min()
data["mean"] = data["orig"].rolling(window).mean()
#row_data["sum"] = row_data["orig"].rolling(window).sum()


mpl.use('TkAgg')
plt.text = "all Rollings"
data.plot()
plt.show()
