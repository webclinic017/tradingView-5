from flask import Flask, render_template, request, flash, redirect, jsonify
import config
from binance.client import Client
from binance.enums import *
from flask_cors import CORS

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


@app.route("/settings")
def settings():
    return 'settings'

@app.route("/history")
def history():
    ticker = "BTCUSDT"
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