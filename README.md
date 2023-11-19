# Backtesting
A basic implementation to download historic prices, apply a strategy, and see the strategy performance vis-a-vis the actual stock prices.

Works with newer version of python libraries

The overview is as follows:
- Go to file Demo.py
- Get the historic data for the required script
- Parse this data as a pandas dataframe
- Apply an appropriate strategy that you want to test. The current code includes basic strategies like RSI crossover or Bollinger band.
- Generate trading signals for this strategy.
- Plot graph of portfolio growth , showing the original prices, versus the portfolio value if you trade by the signals.
- Fine-tune the strategy, run the code again, make money, and then make some more !!

A typical plot for Bollinger-band based strategy:

<img src="https://github.com/Santhosh-Shivan/Backtesting/blob/main/images/Figure_1.png">

Signals for the above strategy:

<img src="https://github.com/Santhosh-Shivan/Backtesting/blob/main/images/Figure_2.png">

This uses Pandas, NumPy, MatPlotLib, and a host of other python libraries.


