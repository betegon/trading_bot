# trading_bot

## TODO


### TODO system design
1. How is the system going to work?
   1. What strategies?
   2. What are the actionables --> set of rules to enter a trade


### TODO Trend

1. Stablish the trend.
   1. different methods to stablish trend (maybe the implement the pooling of various methods 3/5 to consider it a trend)
   2. Add the trend (like LevelType) to the chart.

### TODO support & resistance

1. round up levels (check notes on TRADING/BUILDING A TRADING BOT.md)

2. identify whethere a level is a resistance or a support right now (TODAY). Now support or resistance is based in the time it formed, but it could have been broken from then until now. To know if a level is support or resistance, take the level and compare it to current price, then we could know if it is support or resistance (if above price, it is resistance, if level is below currente price, then support)

3. Note when a level stopped being relevant (many broken times, many candles, etc). sometimes we maybe are taking into account a level that is irrelevant as it was from a year ago and now it is nothing.

### TODO executor/manager

1. Manager/executor uses 3 charts (3 timeframes)
2. it knows the set of rules to execute a trade and execute it if conditions are met.

### TODO backtester

1. object to backtest strategies and get metrics.
2. It should record what trades went bad/good so I can finetune the strategy.