import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    df = yf.download(symbol, period="1y")

    if df.empty:
        return df

    df.reset_index(inplace=True)
    return df


def process_data(df):
    df.dropna(inplace=True)

    # Fix column issue
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df['Daily Return'] = (df['Close'] - df['Open']) / df['Open']
    df['MA7'] = df['Close'].rolling(window=7).mean()

    return df, df['High'].max(), df['Low'].min()