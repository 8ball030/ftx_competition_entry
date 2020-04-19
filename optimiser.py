import itertools
from pyalgotrade.optimizer import local
from accumulator_strategy import Accumulator
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import csvfeed

def parameters_generator():
    instrument = ["BTC"]
    offset = [f / 1000 for f in range(0, 1000)][:100]
    percentage = [f / 100 for f in range(0, 50)]
    return itertools.product(instrument, offset, percentage)

def main():
    feed = csvfeed.GenericBarFeed(frequency=Frequency.MINUTE)
    feed.addBarsFromCSV("BTC", "sampledata.csv")

    # Plot the strategy.
    local.run(Accumulator, feed, parameters_generator())


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the bar feed from the CSV files.
    main()
