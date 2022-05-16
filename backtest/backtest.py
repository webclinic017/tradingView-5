import backtrader as bt
import tradeView_project.vars as vars

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=2)

    def next(self):
        if self.rsi < vars.BACKTEST_OVERSOLD and not self.position:
            self.buy(size=vars.BACKTEST_LOT)

        if self.rsi > vars.BACKTEST_OVERBOUGHT and self.position:
            self.close()

cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname='klines.csv', dtformat=2)

cerebro.adddata(data)
cerebro.addstrategy(RSIStrategy)
cerebro.run()
cerebro.plot()