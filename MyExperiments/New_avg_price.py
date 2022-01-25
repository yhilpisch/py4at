# Calculates the add Funds button new average price

avg = 4.476
vol = 1045.14617218
price = 3.732
new_vol = 3000

New_avg = (avg * vol + price * new_vol) / (vol + new_vol)
print(New_avg)
