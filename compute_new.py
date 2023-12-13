import pandas as pd
import datetime
import numpy as np


def accumulated_close(df):
    # requires a column Stance and Adj close

    fund = 1200
    stock = 0
    last_stance = 0
    for index, row in df.iterrows():
        if row["Stance"] > 0:
            if row["Stance"] != last_stance:
                fees_buy_side = 0.001 * df.loc[index, "Close"]
                fund = fund - df.loc[index, "Close"] - fees_buy_side
                last_stance = row["Stance"]
            stock = df.loc[index, "Close"]

            # print 'Buy and hold'
        elif row["Stance"] < 0:
            if row["Stance"] != last_stance:
                fees_sell_side = 0.001 * df.loc[index, "Close"]
                fund = fund + df.loc[index, "Close"] - fees_sell_side
                last_stance = row["Stance"]
            stock = 0
            # print 'Sell and hold'
        df.loc[index, "Wealth"] = fund + stock
        df.loc[index, "fund"] = fund
        df.loc[index, "stock"] = stock
        # print 'Waiting...'
