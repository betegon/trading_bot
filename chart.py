from level import Level, LevelType
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance
# TODO a chart should contain:
#      - Levels
#      - time frames
#      - current trend (HTF, MTF, LTF)

class Chart():

    def __init__(self, ticker, timeframe, date_start, date_end):
        self.ticker = ticker
        self.timeframe = timeframe
        self.date_start = date_start
        self.date_end = date_end
        self.ticker_history = self._get_ticker_history()
        self.levels = self._create_levels()


    def _get_ticker_history(self) -> pd.DataFrame:
        ticker = yfinance.Ticker(self.ticker)
        ticker_history = ticker.history(
                                interval=self.timeframe,
                                start=self.date_start, end=self.date_end)
        return self.__parse_ticker_history(ticker_history)

    def __parse_ticker_history(self, ticker_history: pd.DataFrame) -> pd.DataFrame:
        ticker_history['Date'] = pd.to_datetime(ticker_history.index)
        ticker_history['Date'] = ticker_history['Date'].apply(mpl_dates.date2num)
        return ticker_history.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    def _create_levels(self) -> list:
        """Create support and resistance levels from ticker history.

        Returns:
            list: list of Level objects.
        """
        levels = []
        price_mean = np.mean(self.ticker_history['High'] - self.ticker_history['Low'])
        for i in range(2, self.ticker_history.shape[0]-2):
            if self.__is_support(i):
                l = self.ticker_history['Low'][i]
                if self.__is_far_from_level(l, price_mean, levels): # remove this line if you want to check all levels 
                    levels.append(Level(LevelType.SUPPORT, (i, l)))
            elif self.__is_resistance(i):
                l = self.ticker_history['High'][i]
                if self.__is_far_from_level(l, price_mean, levels): # remove this line if you want to check all levels 
                    levels.append(Level(LevelType.RESISTANCE, (i, l)))
        return levels

    def __is_support(self, i):
        support = self.ticker_history['Low'][i] < self.ticker_history['Low'][i-1]  and self.ticker_history['Low'][i] < self.ticker_history['Low'][i+1] \
        and self.ticker_history['Low'][i+1] < self.ticker_history['Low'][i+2] and self.ticker_history['Low'][i-1] < self.ticker_history['Low'][i-2]

        return support

    def __is_resistance(self, i):
        resistance = self.ticker_history['High'][i] > self.ticker_history['High'][i-1]  and self.ticker_history['High'][i] > self.ticker_history['High'][i+1] \
        and self.ticker_history['High'][i+1] > self.ticker_history['High'][i+2] and self.ticker_history['High'][i-1] > self.ticker_history['High'][i-2] 

        return resistance

    def __is_far_from_level(self, l, s, levels):
        return np.sum([abs(l-level.value) < s for level in levels]) == 0



    def plot(self):
        # plt params
        plt.rcParams['figure.figsize'] = [12, 7]
        plt.rc('font', size=14) 
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, self.ticker_history.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        date_format = mpl_dates.DateFormatter('%d %b %Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()
        for level in self.levels:
            if level.type == LevelType.SUPPORT:
                color = 'green' # draw green level if support
            elif level.type == LevelType.RESISTANCE:
                color = 'red' # draw red level if resistance
            ax.hlines(level.value[1], xmin=self.ticker_history['Date'][level.value[0]],
                xmax=max(self.ticker_history['Date']), colors=color)
        fig.show()
        plt.show()
