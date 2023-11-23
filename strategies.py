import pandas as pd
import numpy as np
import math
import compute
import indicators
import pandas_ta as ta


# Create column Stance


def SMA_Crossover(df, fast=42, slow=252):
    # create the moving average values and
    # simultaneously append them to new columns in our existing DataFrame.
    df[str(fast) + "d"] = np.round(
        indicators.running_average(df["Adj Close"], windowsize=fast), 2
    )
    df[str(slow) + "d"] = np.round(
        indicators.running_average(df["Adj Close"], windowsize=slow), 2
    )

    # Generate stance: 0, -1, 1.
    df[str(fast) + "-" + str(slow)] = df[str(fast) + "d"] - df[str(slow) + "d"]

    offset = 0
    # add condition to ensure first stance change is never -1.
    df["Stance"] = np.where(df[str(fast) + "-" + str(slow)] > offset, 1, 0)
    df["Stance"] = np.where(df[str(fast) + "-" + str(slow)] < offset, -1, df["Stance"])

    # Generate accumulated closing price
    compute.accumulated_close(df)


def RSI(df, lowerCutoff=30, upperCutoff=70, period=14):
    df["RSI"] = pd.Series(indicators.RSI(df["Adj Close"], period=period))
    df["Stance"] = 0
    offset = 0
    last_stance = 0
    upper_cutoff_set_once = False

    for index, row in df.iterrows():
        if row["RSI"] > upperCutoff:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row["RSI"] < lowerCutoff:
            last_stance = -1

        df.at[index, "Stance"] = last_stance

    compute.accumulated_close(df)


def Bollinger_Band(df):
    # 1. Compute rolling mean
    rolling_mean = indicators.rolling_std_mean(df["Adj Close"], window=10)

    # 2. Compute rolling standard deviation
    rolling_std = indicators.rolling_std(df["Adj Close"], window=10)

    # 3. Compute upper and lower bands
    upper_band, lower_band = indicators.bollinger_bands(rolling_mean, rolling_std)

    df["Stance"] = 0
    last_stance = 0
    upper_cutoff_set_once = False

    upper_band.fillna(method="backfill", inplace=True)
    lower_band.fillna(method="backfill", inplace=True)

    df["Upper Band"] = upper_band
    df["Lower Band"] = lower_band

    for index, row in df.iterrows():
        if row["Adj Close"] > row["Upper Band"]:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row["Adj Close"] < row["Lower Band"]:
            last_stance = -1

        df.at[index, "Stance"] = last_stance

    compute.accumulated_close(df)


def Velocity_SMA(df):
    df["SMA"] = np.round(indicators.running_average(df["Adj Close"], windowsize=20), 2)

    df["Velocity"] = df["SMA"].diff()

    df["Velocity"].fillna(method="backfill", inplace=True)

    df["Stance"] = 0
    last_stance = 0
    bought_set_once = False

    for index, row in df.iterrows():
        if row["Adj Close"] > row["SMA"] and row["Velocity"] > 0:
            bought_set_once = True
            last_stance = 1
        elif bought_set_once and row["Adj Close"] < row["SMA"] and row["Velocity"] < 0:
            last_stance = -1

        df.at[index, "Stance"] = last_stance

    compute.accumulated_close_after_fees(df)


# Should be improved
# If RSI <= 50 and MACD > MACDs :
#   buy
# elif RSI >= 60 aNd MACD < MACDs:
#   sell
def RSI_MACD(df):
    # RSI - pandas TA
    df["RSI_10"] = ta.rsi(df["Adj Close"], length=10)

    # MACD - pandas TA
    df.ta.macd(close="Adj close", fast=8, slow=21, signal=5, append=True)

    # Buy and Sell Strategy

    buy_signal = False
    sell_signal = False

    df["Stance"] = 0
    last_stance = 0
    flag = 0

    for i in range(len(df)):
        df.iloc[i, 10] = last_stance

        ## Buy
        # Buy signal
        if df.RSI_10[i] <= 50 and buy_signal == False:
            buy_signal = True
            sell_signal = False

        # Buy Confirmation
        if buy_signal == True:
            if df.MACD_8_21_5[i] > df.MACDs_8_21_5[i]:
                df.iloc[i, 10] = 1
                last_stance = 1
                flag = 1

        ## Sell
        # Sell signal
        if df.RSI_10[i] >= 60 and flag == 1 and sell_signal == False:
            sell_signal = True
            buy_signal = False

        # Sell confirmation
        if sell_signal == True:
            if df.MACD_8_21_5[i] < df.MACDs_8_21_5[i]:
                df.iloc[i, 10] = -1
                last_stance = -1

    compute.accumulated_close_after_fees(df)
