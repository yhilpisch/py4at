import math as m
import numpy as np
import pandas as pd

# Using log continuous growth rates in finance
# Is more easy to get dif by multiplying ( normalized )
#

"""minus = 1.33510 - 1.33010
z = 1.33510 / 1.33010
z2 = 1.33010 / 1.33510
e = m.log(z2)  # calculate the growing rate from div of prices ( normalized )

print(e)  # , z, minus) # 0.003752068036798753 1.0037591158559507 0.004999999999999893
print((e + 1) * 1.33510)  # 1.33009061396407
print(e * 1.33010)  # -0.004990625695745985"""

data = np.array([1, 3, 7, 9], dtype=np.float64)
pdata = pd.DataFrame(data)
pdata["normal"] = pdata[0] / pdata[0].shift(1)
pdata["log"] = np.log(pdata[0] / pdata[0].shift(1))
pdata["log10"] = np.log10(pdata[0] / pdata[0].shift(1))


e = pdata["normal"][1]
for i in pdata["normal"][2:]:
    e *= i
print(e)

#
e = pdata["log"][1]
for i in pdata["log"][2:]:
    e += i
print(np.exp(e))


# Mit Log 10 das gleiche wie mit euler
e = pdata["log10"][1]
for i in pdata["log10"][2:]:
    e += i
print(10 ** e)




print(m.log(10))
print(np.log(10))

nl = m.log(10)
print(m.exp(nl))

l10 = m.log(10, 10)
print(10 ** l10)


