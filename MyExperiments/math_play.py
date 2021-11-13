import math as m

# Using log continuous growth rates in finance
# Is more easy to get dif by multiplying ( normalized )
#
minus = 1.33510 - 1.33010
z = 1.33510 / 1.33010
z2 = 1.33010 / 1.33510
e = m.log(z2)  # calculate the growing rate from div of prices ( normalized )

print(e)  # , z, minus) # 0.003752068036798753 1.0037591158559507 0.004999999999999893
print((e + 1) * 1.33510)  # 1.33009061396407
print(e * 1.33010)  # -0.004990625695745985
