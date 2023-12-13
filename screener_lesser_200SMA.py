import datetime
import fetcher
import draw
import strategies
import compute
import indicators
import pandas as pd
import pandas_ta as ta
import os
import numpy as np
from finta import TA

startDate = datetime.date(2022, 1, 1)
# endDate = datetime.date(2019, 12, 15)
endDate = datetime.date.today()
flag = "IND"
IND_list = []

# Retrieving Indian tickers from a file
if flag == "IND":
    nifty_file = pd.read_csv("Indices/ind_nifty500list.csv")

    for ticker in nifty_file["Symbol"].tolist()[1:]:
        IND_list.append(ticker + ".NS")
fast = 50
slow = 200

focus_list = []
for ticker in IND_list:
    df = fetcher.__download_data([ticker], startDate, endDate)

    df["EMA50"] = TA.SMA(df, period=50)
    df["EMA200"] = TA.EMA(df, period=200)

    df = pd.concat(
        [df, TA.MACD(df, period_fast=12, period_slow=26, signal=9, column="close")],
        axis=1,
    )

    if (  # df["Close"][-1] >= df["EMA200"][-1]) & (
        # df["Close"][-1]
        # <= 1.02 * df["EMA200"][-1]
        (df["MACD"][-1] < 0)
        & (df["MACD"][-1] < df["SIGNAL"][-1])
    ):
        focus_list.append(ticker)

    # TA.macd(close="Adj close", fast=12, slow=26, signal=9, append=True)


print(df.tail(-100))

print(focus_list)
