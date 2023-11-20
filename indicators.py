import pandas as pd
import datetime
import numpy as np
import compute


# https://github.com/nlsdfnbch/pandas-technical-indicators/blob/master/technical_indicators.py


# moving average.
def running_average(df, windowsize):
    return df.rolling(windowsize).mean()


def exponential_moving_average(df, windowsize=60):
    pd.ewma(df["Adj Close"], span=windowsize, freq="D")


def rolling_std_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    # take df, column name option, default value for window too.
    return values.rolling(window=window).mean()


def rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return values.rolling(window=window).std()


def bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band = rm + rstd * 2  # pd.rolling_std(values, window=window)
    lower_band = rm - rstd * 2  # pd.rolling_std(values, window=window)
    return upper_band, lower_band


def RSI(Series, period):
    # print Series.size
    delta = Series.diff().dropna()
    # print 'size after drop is '
    # print delta.size
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
    u = u.drop(u.index[: (period - 1)])
    d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
    d = d.drop(d.index[: (period - 1)])
    rs = (
        u.ewm(com=period - 1, adjust=False).mean()
        / d.ewm(com=period - 1, adjust=False).mean()
    )
    df = pd.DataFrame(100 - 100 / (1 + rs))

    # slice first period dates, create Series with 50 as value, per date. then concat.
    prefixed_values = pd.Series(50, index=Series.index.values[0:period])
    return pd.concat([prefixed_values, df.iloc[:, 0]])


def MACD(df, fast_ma=26, slow_ma=12, signal_period=9):
    df["30 mavg"] = pd.rolling_mean(df["Close"], 30)
    df["26 ema"] = pd.ewma(df["Close"], span=fast_ma)
    df["12 ema"] = pd.ewma(df["Close"], span=slow_ma)
    df["MACD"] = df["12 ema"] - df["26 ema"]
    df["Signal"] = pd.ewma(df["MACD"], span=signal_period)
    df["Crossover"] = df["MACD"] - df["Signal"]
    return df


# to be tested...
def stochastic_oscillator_k(df, k_window=14, d_window=3):
    # Create the "L14" column in the DataFrame
    df["Low_K"] = df["Low"].rolling(window=k_window).min()

    # Create the "H14" column in the DataFrame
    df["High_K"] = df["High"].rolling(window=k_window).max()

    # Create the "%K" column in the DataFrame
    df["%K"] = 100 * ((df["Close"] - df["Low_K"]) / (df["High_K"] - df["Low_K"]))

    # Create the "%D" column in the DataFrame
    df["%D"] = df["%K"].rolling(window=d_window).mean()


def ROC(df, n):
    M = df.diff(n - 1)
    N = df.shift(n - 1)
    ROC = pd.Series(((M / N) * 100), name="ROC_" + str(n))
    return ROC


def vortex_indicator(df, n):
    """Calculate the Vortex Indicator for given data.

    Vortex Indicator described here:
        http://www.vortexindicator.com/VFX_VORTEX.PDF
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df.get_value(i + 1, "High"), df.get_value(i, "Close")) - min(
            df.get_value(i + 1, "Low"), df.get_value(i, "Close")
        )
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df.get_value(i + 1, "High") - df.get_value(i, "Low")) - abs(
            df.get_value(i + 1, "Low") - df.get_value(i, "High")
        )
        VM.append(Range)
        i = i + 1
    VI = pd.Series(
        pd.rolling_sum(pd.Series(VM), n) / pd.rolling_sum(pd.Series(TR), n),
        name="Vortex_" + str(n),
    )
    df = df.join(VI)
    return df


def money_flow_index(df, n):
    """Calculate Money Flow Index and Ratio for given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    # Compute Typical Price
    df["PP"] = (df["High"] + df["Low"] + df["Close"]) / 3

    # Money flow direction (0-Neg, 1-Pos)
    i = 0
    MF = [1]

    while i < len(df) - 1:
        if df.iloc[i + 1]["PP"] > df.iloc[i]["PP"]:
            MF.append(1)
        else:
            MF.append(0)

        i += 1

    # Compute Pos and Neg flow
    i = 0
    PosMF = [0]
    NegMF = [0]
    while i < len(df) - 1:
        if MF[i + 1] == 1:
            PosMF.append(df.iloc[i + 1]["PP"] * df.iloc[i + 1]["Volume"])
            NegMF.append(0)
        else:
            PosMF.append(0)
            NegMF.append(df.iloc[i + 1]["PP"] * df.iloc[i + 1]["Volume"])

        i += 1

    PosMF = pd.Series(PosMF)
    NegMF = pd.Series(NegMF)

    # Compute n-day rolling average for Pos & Neg MFs
    ndPosMFSMA = pd.Series(np.round(running_average(PosMF, windowsize=n), 2))
    ndNegMFSMA = pd.Series(np.round(running_average(NegMF, windowsize=n), 2))

    ndPosMFSMA.fillna(method="backfill", inplace=True)
    ndNegMFSMA.fillna(method="backfill", inplace=True)

    # Compute Money Flow Ratio
    MFR = ndPosMFSMA / ndNegMFSMA

    # Compute Money Flow Index
    MFI = pd.Series(100 - 100 / (1 + MFR))
    MFI.index = df.index

    df["MFI"] = MFI
    return df


# Not getting same values as in TradingView
def CCI(df, n):
    """Calculate Commodity Channel Index for given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    TP = (df["High"] + df["Low"] + df["Close"]) / 3
    # TPSMA = pd.Series(np.round(running_average(TP, windowsize=n), 2))
    TPSMA = pd.Series(np.round(running_average(TP, windowsize=n), 2))
    temp = (TP - TPSMA).abs()
    print(temp.tail())
    meanDeviation = pd.Series(np.round(running_average(temp, windowsize=n), 2))
    CCI = (TP - TPSMA) / (0.015 * meanDeviation)
    CCI.index = df.index
    df["CCI_10"] = CCI
    return df


def Williams_percent_r(df):
    print("pending")
