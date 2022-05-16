This is a basic trading view with live update of Bitcoin prices from Binance web sockets, created using python-binance and server running with Flask.

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
$ export FLASK_ENV=development <br />
$ flask run
```


<br />

3. To get feed from a different ticker update the `ticker` variable in the `history` function in `app.py`