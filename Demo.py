import datetime
import fetcher
import draw
import strategies
import compute
import indicators


# get , Apply strategy , draw.


def backtest():
    startDate = datetime.date(2017, 1, 1)
    # endDate = datetime.date(2023, 11, 15)
    endDate = datetime.date.today()
    df = fetcher.__download_data(["MU"], startDate, endDate)
    print(df.tail(1))

    # strategies.RSI(df)
    # draw.strategy_results(df, title="RSI strategy")

    # strategies.SMA_Crossover(df)
    # draw.strategy_results(df)

    # strategies.Bollinger_Band(df)
    # draw.strategy_results(df)
    # draw.bollinger_bands_from_df(df)

    strategies.Velocity_SMA(df)
    draw.strategy_results(df)

    # strategies.RSI_MACD(df)
    # draw.strategy_results(df)

    draw.column(
        df, title="Stance", columns=["Stance"]
    )  # buy-sell signals for the strategy.


# To check the stance today and make a trade accordingly
def stanceToday():
    startDate = datetime.date(2023, 1, 1)
    # endDate = datetime.date(2023, 12, 1)
    endDate = datetime.date.today()
    df = fetcher.__download_data(["TITAN.NS"], startDate, endDate)

    strategies.Velocity_SMA(df)
    print(df["Stance"].tail())


if __name__ == "__main__":
    backtest()
    # stanceToday()
