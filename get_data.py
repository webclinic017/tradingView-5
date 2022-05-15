import json, csv

import config
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET, testnet=True)

# get candlestick data
# csvfile = open('data/klines.csv', 'w', newline='')
# candlestick_writer = csv.writer(csvfile, delimiter=",")
#
# candles = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_15MINUTE)
#
# for c in candles:
#     candlestick_writer.writerow(c)
# csvfile.close()


# get historical candlestick data
csvfile02 = open('eth_historical_klines.csv', 'w', newline='')
candlestick_writer02 = csv.writer(csvfile02, delimiter=",")

ticker = "ETHUSDT"
start = '1 Jan, 2019'
historical_candles = client.get_historical_klines(symbol=ticker, interval=Client.KLINE_INTERVAL_1HOUR, start_str=start)

for c in historical_candles:
    candlestick_writer02.writerow(c)
csvfile02.close()

import pandas as pd
df = pd.read_csv('eth_historical_klines.csv')
df.iloc[:, 0] = df.iloc[:, 0] / 1000
df.to_csv('eth_klines.csv', index=False)

