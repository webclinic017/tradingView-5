This is a basic trading view with live update of Ethereum prices from Binance web sockets, created using python-binance & LightWeight charts and server running with Flask. User can trade right from the interface, run backtests for RSI strategy over a 2 year period and run an automated bot to make trades with the RSI strategy


<br />

0. Install dependencies with

```
$ pip install -r requirements.txt
```

<br />

1. Create a new API with Binance  

next, create a file called `config.py` in the root directory and add thmem in

```
API_SECRET='your_binance_api_secret'
API_KEY='your_binance_api_key'
```

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

4. To try out different backtests, update variables in vars.py

5. Add parameters to HTML page and start the bot for automated trading