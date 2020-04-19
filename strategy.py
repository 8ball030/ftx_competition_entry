from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import trades

from pyalgotrade import plotter


from accumulator_strategy import Accumulator

def main():
    feed = csvfeed.GenericBarFeed(frequency=Frequency.MINUTE)
    feed.addBarsFromCSV("ETH", "sampledata.csv")

    # Evaluate the strategy with the feed's bars.
    myStrategy = Accumulator(feed, "ETH", buy_offset=0.0017, buy_percent=0.49)
    # myStrategy.run()

    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)


    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot("ETH").addDataSeries("SMA", myStrategy.getSMA())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # Run the strategy.
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

    # Plot the strategy.
    plt.plot()

    print("Final portfolio value: $%.2f" % myStrategy.getResult())


if __name__ == "__main__":
    main()

