import datetime
import fetcher
import draw
import strategies
import compute
import indicators


# get , Apply strategy , draw.
def test_run():
    startDate = datetime.date(2012, 1, 1)
    # endDate = datetime.date(2023, 11, 15)
    endDate = datetime.date.today()
    df = fetcher.__download_data(["INFY.NS"], startDate, endDate)
    print(df.tail(1))
    """indicators.CCI(df, 20)
    print(df["CCI_10"].tail())"""

    # strategies.RSI(df)
    # draw.strategy_results(df, title="RSI strategy")

    # strategies.SMA_Crossover(df)
    # draw.strategy_results(df)

    strategies.Bollinger_Band(df)
    draw.strategy_results(df)
    # draw.bollinger_bands_from_df(df)

    # strategies.Velocity_SMA(df)
    # draw.strategy_results(df)

    draw.column(
        df, title="Stance", columns=["Stance"]
    )  # buy-sell signals for the strategy.


if __name__ == "__main__":
    test_run()
