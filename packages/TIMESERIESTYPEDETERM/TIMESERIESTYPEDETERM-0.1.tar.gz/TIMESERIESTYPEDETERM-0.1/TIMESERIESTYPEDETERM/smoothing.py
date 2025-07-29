import pandas as pd
import numpy as np

def SMA(df):
    window_size = 5
    df1 = df.rolling(window=window_size).mean()
    df1 = df1.dropna()
    return df1

def EMA(df):
    span = 15
    df1 = df.ewm(span=span, adjust=False).mean()
    return df1

def LWMA(df):
    window_size = 5
    weights = np.arange(1, window_size + 1)
    df1 = df.rolling(window=window_size).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    df1 = df1.dropna()
    return df1
