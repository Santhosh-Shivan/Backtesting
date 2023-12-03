import datetime
import fetcher
import draw
import strategies
import compute
import indicators
import pandas as pd
import os


# get , Apply strategy , draw.
def basket_backtest():
    startDate = datetime.date(2017, 1, 1)
    # endDate = datetime.date(2019, 12, 15)
    endDate = datetime.date.today()
    flag = "IND"
    IND_list = []

    # Retrieving Indian tickers from a file
    if flag == "IND":
        nifty_file = pd.read_csv("Indices/Nifty Smallcap 50.csv")

        for ticker in nifty_file["Symbol"].tolist()[1:]:
            IND_list.append(ticker + ".NS")
    US_list = [
        "AAPL",
        "MSFT",
        "GOOG",
        "NVDA",
        "TSLA",
        "AMZN",
        "META",
        "ORCL",
        "UNH",
        "AVGO",
        "AMD",
        "TMO",
        "INTC",
        "QCOM",
        "IBM",
        "RTX",
        "LMT",
    ]

    US_results = {}
    IND_results = {}

    market_dict = {
        "US": [US_list, US_results, "US_results"],
        "IND": [IND_list, IND_results, "IND_results"],
    }

    for ticker in market_dict[flag][0]:
        df = fetcher.__download_data([ticker], startDate, endDate)

        # strategies.RSI(df)

        # strategies.SMA_Crossover(df)

        # strategies.Bollinger_Band(df)

        strategies.Velocity_SMA(df)
        # draw.strategy_results(df)

        # strategies.RSI_MACD(df)
        last_row = df.tail(1)
        first_row = df.head(1)
        times_increased_Acc = (
            last_row["Accumulated Close"].values[0]
            / first_row["Accumulated Close"].values[0]
        )
        times_increased_Adj = (
            last_row["Adj Close"].values[0] / first_row["Adj Close"].values[0]
        )
        market_dict[flag][1][ticker] = [times_increased_Acc, times_increased_Adj]

        df = pd.DataFrame.from_dict(market_dict[flag][1], orient="index")
        df.columns = ["Acc close", "Adj Close"]
        directory = "Results"
        if not os.path.exists(directory):
            os.makedirs(directory)

        fileName = (
            directory
            + "/"
            + market_dict[flag][2]
            + str(startDate)
            + str(endDate)
            + ".csv"
        )
        df.to_csv(fileName)


if __name__ == "__main__":
    basket_backtest()
