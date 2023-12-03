import pandas as pd
import datetime
import numpy as np


def accumulated_close(df):
    # requires a column Stance and Adj close

    diff_LastSoldPrice_CurrAdj = 0.00

    for index, row in df.iterrows():
        if row["Stance"] > 0:
            df.loc[index, "Accumulated Close"] = (
                df.loc[index, "Adj Close"] + diff_LastSoldPrice_CurrAdj
            )
            pointer = index
            # print 'Buy and hold'
        elif row["Stance"] < 0:
            df.loc[index, "Accumulated Close"] = df.loc[pointer, "Accumulated Close"]
            diff_LastSoldPrice_CurrAdj = (
                df.loc[index, "Accumulated Close"] - df.loc[index, "Adj Close"]
            )
            # print 'Sell and hold'
        else:
            df.loc[index, "Accumulated Close"] = df.loc[index, "Adj Close"]
            # print 'Waiting...'


def accumulated_close_after_fees(df):
    # requires a column Stance and Adj close

    diff_LastSoldPrice_CurrAdj = 0.00
    last_stance = 0
    total_fees = 0
    for index, row in df.iterrows():
        if row["Stance"] > 0:
            if row["Stance"] != last_stance:
                # STT = 0.1% of trading price
                fees_buy_side = 0.001 * df.loc[index, "Adj Close"]
                total_fees += fees_buy_side
                last_stance = row["Stance"]

            df.loc[index, "Accumulated Close"] = (
                df.loc[index, "Adj Close"] + diff_LastSoldPrice_CurrAdj - fees_buy_side
            )
            pointer = index
            # print 'Buy and hold'
        elif row["Stance"] < 0:
            if row["Stance"] != last_stance:
                # STT = 0.1% of trading price
                fees_sell_side = 0.001 * df.loc[index, "Adj Close"]
                total_fees += fees_sell_side
                last_stance = row["Stance"]
            df.loc[index, "Accumulated Close"] = df.loc[pointer, "Accumulated Close"]
            diff_LastSoldPrice_CurrAdj = (
                df.loc[pointer, "Accumulated Close"]
                - df.loc[index, "Adj Close"]
                - fees_sell_side
            )
            # print 'Sell and hold'
        else:
            df.loc[index, "Accumulated Close"] = df.loc[index, "Adj Close"]
            # print 'Waiting...'

    # print(total_fees)
