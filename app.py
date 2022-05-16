import csv, pprint
import numpy, talib, websocket, json
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, jsonify
import backtrader as bt
import config
from binance.client import Client
from binance.enums import *
from flask_cors import CORS
import vars

client = Client(config.API_KEY, config.API_SECRET)

app = Flask(__name__)
app.secret_key = b'fasdiyakewdsiclzsciocxzhcbzdofzbczcwre789q75afkjhas'
CORS(app)

@app.route("/")
def index():
    title = "binance trading bot"
    info = client.get_account()
    balances = info['balances']
    exchange = client.get_exchange_info()
    symbols = exchange['symbols']

    return render_template('index.html', title=title, balances=balances, symbols=symbols)


@app.route("/buy", methods=['POST'])
def buy():
    try:
        order = client.create_order(
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")
    return redirect("/")


@app.route("/sell", methods=['POST'])
def sell():
    try:
        order = client.order_market_sell(
            symbol=request.form['sell_symbol'],
            quantity=request.form['sell_quantity']
        )
    except Exception as e:
        flash(e.message, "error")
    return redirect("/")

@app.route("/history")
def history():
    ticker = "ETHUSDT"
    start = '1 Dec, 2019'
    historical_candles = client.get_historical_klines(symbol=ticker, interval=Client.KLINE_INTERVAL_1DAY,start_str=start)

    processed_candlesticks = []
    for data in historical_candles:
        candle = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }
        processed_candlesticks.append(candle)

    return jsonify(processed_candlesticks)

@app.route("/backtest", methods=['POST'])
def backtest():
    BACKTEST_SYMBOL=request.form['backtest_symbol']
    BACKTEST_PERIOD=float(request.form['backtest_length'])
    BACKTEST_OVERBOUGHT=float(request.form['backtest_overbought'])
    BACKTEST_OVERSOLD=float(request.form['backtest_oversold'])
    BACKTEST_QUANTITY=float(request.form['backtest_quantity'])

    class RSIStrategy(bt.Strategy):
        def __init__(self):
            self.rsi = bt.talib.RSI(self.data, period=BACKTEST_PERIOD)

        def next(self):
            if self.rsi < BACKTEST_OVERSOLD and not self.position:
                self.buy(size=BACKTEST_QUANTITY)

            if self.rsi > BACKTEST_OVERBOUGHT and self.position:
                self.close()


    def get_data():
        csvfile = open('backtest/historical_klines.csv', 'w', newline='')
        candlestick_writer = csv.writer(csvfile, delimiter=",")

        historical_candles = client.get_historical_klines(symbol=BACKTEST_SYMBOL,
                                                          interval=Client.KLINE_INTERVAL_1HOUR,
                                                          start_str=vars.BACKTEST_START)

        for c in historical_candles:
            candlestick_writer.writerow(c)
        csvfile.close()
    def format_csv():
        df = pd.read_csv('backtest/historical_klines.csv')
        df.iloc[:, 0] = df.iloc[:, 0] / 1000
        df.to_csv('klines.csv', index=False)

    get_data()
    format_csv()

    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(dataname='klines.csv', dtformat=2)
    cerebro.adddata(data)
    cerebro.addstrategy(RSIStrategy)
    cerebro.run()
    cerebro.plot()

    return redirect("/")

closes = []
in_position = False

@app.route("/bot", methods=['POST'])
def bot():
    RSI_PERIOD = request.form['rsi_length']
    RSI_OVERSOLD = request.form['rsi_oversold']
    RSI_OVERBOUGHT = request.form['rsi_overbought']
    TRADE_SYMBOL = request.form['rsi_symbol']
    TRADE_QUANTITY = request.form['rsi_quantity']

    def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print("sending order")
            order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print(order)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False

        return True

    def on_open(ws):
        print('opened connection')

    def on_close(ws):
        print('closed connection')

    def on_message(ws, message):
        global closes, in_position

        print('received message')
        json_message = json.loads(message)
        pprint.pprint(json_message)

        candle = json_message['k']

        is_candle_closed = candle['x']
        close = candle['c']

        if is_candle_closed:
            print("candle closed at {}".format(close))
            closes.append(float(close))
            print("closes")
            print(closes)

            if len(closes) > RSI_PERIOD:
                np_closes = numpy.array(closes)
                rsi = talib.RSI(np_closes, RSI_PERIOD)
                print("all rsis calculated so far")
                print(rsi)
                last_rsi = rsi[-1]
                print("the current rsi is {}".format(last_rsi))

                if last_rsi > RSI_OVERBOUGHT:
                    if in_position:
                        print("Overbought! Time to sell.")
                        # sell logic
                        order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = False
                    else:
                        print("It is overbought, but we don't own any. Nothing to do.")

                if last_rsi < RSI_OVERSOLD:
                    if in_position:
                        print("It is oversold, but you already own it, nothing to do.")
                    else:
                        print("Oversold! Time to buy!")
                        # buy order logic
                        order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = True

    ws = websocket.WebSocketApp(vars.TICKER_SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()

    return redirect("/")