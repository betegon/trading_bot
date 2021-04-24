import pandas as pd
import numpy as np
import yfinance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt


def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
  and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
  and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

  return resistance

def plot_all(levels):
    fig, ax = plt.subplots()

    candlestick_ohlc(ax,df.values,width=0.6, \
                    colorup='green', colordown='red', alpha=0.8)

    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    for level in levels["support"]:
        plt.hlines(level[1],xmin=df['Date'][level[0]],\
                xmax=max(df['Date']),colors='green')
    for level in levels["resistance"]:
        plt.hlines(level[1],xmin=df['Date'][level[0]],\
                xmax=max(df['Date']),colors='red')
    fig.show()
    plt.show()

def isFarFromLevel(l):
  return np.sum([abs(l-x) < s  for x in levels_all]) == 0

if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14) 

    name = 'BTC-USD'
    time_interval = "1d"
    date_start = "2021-01-15"
    date_end = "2021-04-15"
    ticker = yfinance.Ticker(name)
    df = ticker.history(interval=time_interval,start=date_start, end=date_end)
    # TODO get ticker history for HTF, MTF and LTF 

    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    print(df)


    levels = {"support": [], "resistance": []}
    levels_all = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            levels["support"].append((i,df['Low'][i]))
            levels_all.append((i,df['Low'][i]))
        elif isResistance(df,i):
            levels["resistance"].append((i,df['High'][i]))
            levels_all.append((i,df['High'][i]))
    
    plot_all(levels)
    
    s =  np.mean(df['High'] - df['Low'])
    levels = {"support": [], "resistance": []}
    levels_all = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]

            if isFarFromLevel(l):
                levels["support"].append((i,l))
                levels_all.append((i,l))

        elif isResistance(df,i):
            l = df['High'][i]

            if isFarFromLevel(l):
                levels["resistance"].append((i,l))
                levels_all.append((i,l))
    print(levels)
    plot_all(levels)