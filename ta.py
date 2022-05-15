from numpy import genfromtxt
import talib

csvfile = genfromtxt('data/historical_klines.csv', delimiter=",")

closing_prices = csvfile[:, 4]
# print(closing_prices)

rsi = talib.RSI(closing_prices)
print(rsi)