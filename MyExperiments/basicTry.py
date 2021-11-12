
import numpy as np
import matplotlib.pyplot as plt

S0 = 100
r = 0.05
T = 1.0
sigma = 0.2

X = np.arange(0, 1000, 10);
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.random.standard_normal(len(X)) * np.sqrt(T))
#X = range(1000)
plt.hist(ST)
plt.plot(X, ST, )
plt.scatter(X, ST)
plt.show()
print("Done")