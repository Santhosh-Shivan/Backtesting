import pandas as pd
import datetime
import numpy as np


def daily_returns(df):
    # how to read/interpret this ?
    print(df.head())
    # (tomorrow price/today price) - 1
    daily_return = (df / df.shift(1)) - 1
    print(daily_return.head())
    daily_return.ix[0, :] = 0
    return daily_return


def normalize(df, column="Adj Close"):
    # take column, normalize from earliest available date.
    print("pending normalize")


# ---------------------------------------------


def accumulated_close(df):
    # requires a column Stance, and Adj close

    pointer = df.iloc[0]  # first date as index.
    booked_profit = 0.00

    for index, row in df.iterrows():
        if row["Stance"] > 0:
            df.loc[index, "Accumulated Close"] = (
                df.loc[index, "Adj Close"] + booked_profit
            )
            pointer = index
            # print 'Buy and hold'
        elif row["Stance"] < 0:
            df.loc[index, "Accumulated Close"] = df.loc[pointer, "Accumulated Close"]
            booked_profit = (
                df.loc[pointer, "Accumulated Close"] - df.loc[index, "Adj Close"]
            )
            # print 'Sell and hold'
        else:
            df.loc[index, "Accumulated Close"] = df.loc[index, "Adj Close"]
            # print 'Waiting...'
