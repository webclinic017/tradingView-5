This is a basic trading view with live update of Bitcoin prices from Binance web sockets, created using python-binance & LightWeight charts and server running with Flask.

<br />

0. Install dependencies with

```
$ pip install -r requirements.txt
```

<br />

1. Create an API key with Binance and update the `API_SECRET` and `API_KEY` in `config.py`

<br />

2. Run the app 

``` 
$ export FLASK_APP=app
$ flask run 
```

<br />
- For debug mode

```
$ export FLASK_ENV=development
$ flask run
```


<br />

3. To get feed from a different ticker update the `ticker` variable in the `history` function in `app.py`

and

update `binanceSocket` variable in static/chart.js with the new ticker you want updated prices of.

4. To try out the parameters, first get some historical data

```commandline
$ python get_data.py  
```

then 
```commandline
$ cd backtest/
$ python backtest.py
```

Change parameters of RSI in the `backtest.py` script

5. Add parameters to HTML page and start the bot for automated trading