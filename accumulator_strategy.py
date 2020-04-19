from __future__ import print_function

from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed, csvfeed
from pyalgotrade.technical import ma


class Accumulator(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, buy_offset, buy_percent):
        super(Accumulator, self).__init__(feed, 10000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.

        # self.setUseAdjustedValues(False)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), 60)
        self.offset = buy_offset
        self.buy_percent = buy_percent

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
#        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
#        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        # print(bars)
        bar = bars[self.__instrument]
       # self.info(bar.getClose())
       # self.info(self.__sma[-1])

        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a
        # long position.
        shares = (self.getBroker().getCash() / bars[self.__instrument].getPrice())


        if self.__position is None:
            if (bar.getPrice() * (1 + self.offset) < self.__sma[-1]):
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive():
            if (bar.getPrice() * (1 - self.offset) > self.__sma[-1]):
                # Enter a buy market order. The order is good till canceled.
                self.__position.exitMarket()


    def getSMA(self):
        return self.__sma



