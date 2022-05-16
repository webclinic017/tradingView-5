import json, csv

import config
from binance.client import Client
import vars

client = Client(config.API_KEY, config.API_SECRET, testnet=True)

# get historical candlestick data
csvfile = open('backtest/historical_klines.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=",")

historical_candles = client.get_historical_klines(symbol=vars.TICKER_VARIABLE,
                                                  interval=Client.KLINE_INTERVAL_1HOUR,
                                                  start_str=vars.BACKTEST_START)

for c in historical_candles:
    candlestick_writer.writerow(c)
csvfile.close()

import pandas as pd
df = pd.read_csv('backtest/historical_klines.csv')
df.iloc[:, 0] = df.iloc[:, 0] / 1000
df.to_csv('klines.csv', index=False)

