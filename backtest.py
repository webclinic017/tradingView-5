import backtrader as bt

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=20)

    def next(self):
        if self.rsi < 20 and not self.position:
            self.buy(size=0.01)

        if self.rsi > 80 and self.position:
            self.close()


class SMAStrategy(bt.Strategy):
    params = (('period', 20),)
    def __init__(self):
        self.sma = bt.talib.SMA(self.data, timeperiod=self.p.period)

cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname='eth_klines.csv', dtformat=2)

cerebro.adddata(data)
cerebro.addstrategy(SMAStrategy)
cerebro.run()
cerebro.plot()