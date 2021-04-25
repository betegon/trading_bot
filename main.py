import pandas as pd
import numpy as np
import yfinance
import mplfinance as mpf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from typing import Tuple



def get_ticker_history(ticker: str, time_interval: str, date_start: str,
                       date_end: str) -> pd.DataFrame: 
    ticker = yfinance.Ticker(ticker)
    return ticker.history(interval=time_interval, start=date_start, end=date_end)

def parse_ticker_history(ticker_history: pd.DataFrame) -> pd.DataFrame:
    ticker_history['Date'] = pd.to_datetime(ticker_history.index)
    ticker_history['Date'] = ticker_history['Date'].apply(mpl_dates.date2num)
    return ticker_history.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

def create_levels(df: pd.DataFrame) -> Tuple[dict, list]:
    levels = {"support": [], "resistance": []}
    levels_all = []
    for i in range(2, df.shape[0]-2):
        if isSupport(df, i):
            levels["support"].append((i, df['Low'][i]))
            levels_all.append((i, df['Low'][i]))
        elif isResistance(df, i):
            levels["resistance"].append((i, df['High'][i]))
            levels_all.append((i, df['High'][i]))
    return levels, levels_all

def filter_levels(df: pd.DataFrame) -> Tuple[dict, list]:
    levels = {"support": [], "resistance": []}
    levels_all = []

    price_mean =  np.mean(df['High'] - df['Low'])
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]

            if isFarFromLevel(l, price_mean, levels_all):
                levels["support"].append((i,l))
                levels_all.append((i,l))

        elif isResistance(df,i):
            l = df['High'][i]

            if isFarFromLevel(l, price_mean, levels_all):
                levels["resistance"].append((i,l))
                levels_all.append((i,l))
    return levels, levels_all

def isSupport(df,i):
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
    and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

    return support

def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
    and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

    return resistance

def plot_all(df, levels):
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

def plot_all_new(df, levels):
    # TODO THIS FUNCTION IS INCOMPLETE, AS IT WORKS BAD (LEVELS PLOTTED IN DIFFERENTE FIGURE) 
    # TODO check this!!!!! https://stackoverflow.com/questions/60599812/how-can-i-customize-mplfinance-plot
    fig, ax = plt.subplots()
    ax.xaxis_date()
    mc = mpf.make_marketcolors(up='g',down='r', edge='inherit')
    style  = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(df, type='candlestick', style = style, figscale=1.85)

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

def isFarFromLevel(l, s, levels):
    return np.sum([abs(l-x) < s  for x in levels]) == 0


def main():
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14) 

    #ticker = 'BTC-USD'
    ticker = 'MSFT'
    time_interval = "1d"
    date_start = "2020-01-15"
    date_end = "2021-04-15"
    ticker_history = get_ticker_history(ticker, time_interval, date_start, date_end)
    ticker_history = parse_ticker_history(ticker_history)
    levels, levels_all = create_levels(ticker_history)
    levels, levels_all = filter_levels(ticker_history)
    plot_all(ticker_history, levels)
    

    print(levels)
    plot_all(ticker_history, levels)

    # TODO Round up levels
    # TODO save information of winning and lossing trades (levels, etc), to get statistics from that.

if __name__ == '__main__':
    main()
    # TODO get ticker history for HTF, MTF and LTF 