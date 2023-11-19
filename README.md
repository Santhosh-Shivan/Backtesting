# Backtesting
If you are into positional trading and want to backtest some pre-implemented strategies or if you want to checkout your custom strategy, this is the right place.

A basic but robust implementation for backtesting and analyse the strategy performance and can be used for any market(Here implemented for NSE stocks)

Works with newer version of python libraries

The flow to follow is:
- Run Demo.py with your desired stock and dates for backtesting
- Apply an appropriate strategy that you want to test. The current code includes some common strategies like RSI, SMA crossover, etc.
- 2 plots will be shown as a result
    * First one shows the comparison of accumulated price of the stock if you follow the strategy to the original stock price over the specified time period
    * Second one shows the signals over the same time period
        - +1 - buy and hold
        - -1 - sell and hold
- Play with the parameters of the strategy!

A typical plot for Bollinger-band based strategy:

<img src="https://github.com/Santhosh-Shivan/Backtesting/blob/main/images/Figure_1.png">

Signals for the above strategy:

<img src="https://github.com/Santhosh-Shivan/Backtesting/blob/main/images/Figure_2.png">

This program uses Pandas, NumPy, MatPlotLib, and a host of other python libraries.


