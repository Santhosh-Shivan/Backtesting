import pandas as pd
import numpy as np
import math
import compute
import indicators


# Create column Stance
# Create column Accumulated Close


def SMA_Crossover(df, fast=42, slow=252):
    # create the moving average values and
    # simultaneously append them to new columns in our existing DataFrame.
    df["42d"] = np.round(indicators.running_average(df["Adj Close"], windowsize=42), 2)
    df["252d"] = np.round(
        indicators.running_average(df["Adj Close"], windowsize=252), 2
    )

    # Generate stance: 0, -1, 1.
    df["42-252"] = df["42d"] - df["252d"]

    offset = 0
    # add condition to ensure first stance change is never -1.
    df["Stance"] = np.where(
        df["42-252"] > offset, 1, 0
    )  # 42ma being offset amount above 252 value.
    df["Stance"] = np.where(df["42-252"] < offset, -1, df["Stance"])

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

    print(df["Velocity"])

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

    compute.accumulated_close(df)


def MACD(df):
    print("Pending.")
