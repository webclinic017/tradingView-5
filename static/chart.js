const chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 1000,
  	height: 500,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});
const candlestickSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000',
});

fetch('http://localhost:5000/history')
    .then((e) => e.json())
    .then((res) => {
        candlestickSeries.setData(res);
    })

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1d");
binanceSocket.onmessage = function (event) {
	var message = JSON.parse(event.data);
	var candlestick = message.k;

	candlestickSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}

chart.timeScale().fitContent();