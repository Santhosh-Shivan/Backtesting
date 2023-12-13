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
    nifty_file = pd.read_csv("Indices/MW-NIFTY-50-02-Dec-2023.csv")

    for ticker in nifty_file["SYMBOL \n"].tolist()[1:]:
        IND_list.append(ticker + ".NS")
fast = 50
slow = 200

focus_list = []
for ticker in IND_list:
    df = fetcher.__download_data([ticker], startDate, endDate)

    df[str(fast) + "d"] = np.round(
        indicators.running_average(df["Close"], windowsize=fast), 2
    )
    df[str(slow) + "d"] = np.round(
        indicators.running_average(df["Close"], windowsize=slow), 2
    )
    df = pd.concat([df, TA.MACD(df, period_fast=12, period_slow=26, signal=9)], axis=1)

    if (
        (df[str(fast) + "d"][-1] >= 1.05 * df[str(slow) + "d"][-1])
        & (df[str(fast) + "d"][-1] <= 1.10 * df[str(slow) + "d"][-1])
        & (df["MACD"][-1] < 0)
        & (df["MACD"][-1] < df["SIGNAL"][-1])
    ):
        focus_list.append(ticker)

    # TA.macd(close="Adj close", fast=12, slow=26, signal=9, append=True)


print(df.tail(-100))

print(focus_list)
