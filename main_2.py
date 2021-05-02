from chart import Chart

def main():
    ticker = 'MSFT'
    timeframe = "1d"
    date_start = "2020-05-15"
    date_end = "2021-05-15"
    chart = Chart(ticker, timeframe, date_start, date_end)
    chart.plot()

    # TODO Round up levels
    # TODO save information of winning and lossing trades (levels, etc), to get statistics from that.

if __name__ == '__main__':
    main()
    # TODO get ticker history for HTF, MTF and LTF 