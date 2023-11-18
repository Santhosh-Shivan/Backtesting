import yfinance as yf
import pandas as pd
import os
import datetime


# get from yahoo/google
# search symbols here: https://finance.yahoo.com/lookup
def __download_data(ticker, start, end, write_to_file=True):
    directory = "yahoo_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = directory + "/" + ticker[0] + ".csv"

    allow_reading_file = True
    if os.path.isfile(fileName) and allow_reading_file:
        # check symbol_date.csv, if present, read and return it
        print("reading from file:  " + fileName)
        df = pd.read_csv(
            fileName, index_col="Date", parse_dates=True, na_values=["nan"]
        )

        return df
    else:
        print("fetching data from API for " + ticker[0])
        df = yf.download(ticker[0], start=start, end=end)

        if write_to_file:
            df.to_csv(fileName)

    print("df from Yahoo is:")
    print(df.shape)
    print(df.head())

    return df


def list_available_symbols():
    print("pending listAvailableSymbols")
    # list as table NSE symbol and matching Yahoo symbol.
    # possiblly save to file as well.


def update_data_for_symbol(symbol):
    print("pending")
    # read file, get data from last date to current date
    # append data to file.


if __name__ == "__main__":
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date.today()
    print(__download_data(["RELIANCE.NS"], startDate, endDate).head())
    # get_data_for_symbol('RELIANCE', 'RELIANCE.NS', startDate, endDate)
