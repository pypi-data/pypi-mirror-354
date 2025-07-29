import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def ADF(data):
    values = np.log(data)
    values = pd.Series(values).replace([np.inf, -np.inf], np.nan).dropna()
    values = values.fillna(values.mean())
    res = adfuller(values)
    return res[1]

def determine_time_series_class(series):
    p_value = ADF(series)
    if p_value < 0.05:
        s = "Тренд-стационарный"
        f = 0
    else:
        diff_series = series.diff().dropna()
        p_value_diff = ADF(diff_series)
        if p_value_diff < 0.05:
            s = "Разностно-стационарный"
            f = 1
        else:
            s = "Не стационарный"
            f = 2
    return f, s

def delete_trend_season(f, data):
    if f == 0:
        df1 = data - data.rolling(window=2).mean()
    elif f == 1:
        df1 = data.diff()
    elif f == 2:
        df_not_trend = data - data.rolling(window=2).mean()
        df1 = df_not_trend.diff()

    df1.dropna(inplace=True)
    plt.plot(data, label='Исходный ВР')
    plt.plot(df1, label='ВР после удаления тренда', linestyle='--')
    plt.legend()
    plt.grid()
    plt.xlabel('Дата')
    plt.ylabel('Температура')
    plt.show()
    return df1
