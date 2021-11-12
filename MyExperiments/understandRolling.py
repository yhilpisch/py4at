from ch03.sample_data import generate_sample_data
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

window = 3

data = generate_sample_data(10,1)
das = pd.DataFrame(data)
ergb = pd.DataFrame(das, columns=["orig","min","mean","sum"])
ergb["orig"] = das
# Rolling verschiebt die Tabele nur und vergleicht dann die werte je nach befehl (max,min ...)
ergb["max"] = das.rolling(window).max()
ergb["min"] = das.rolling(window).min()
ergb["mean"] = das.rolling(window).mean()
#ergb["sum"] = das.rolling(window).sum()


mpl.use('TkAgg')
plt.text = "all Rollings"
ergb.plot()
plt.show()
plt
