import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

class Stationarity:
    def __init__(self, data):
        self.data = data

    def adf_test(self):
        values = np.log(self.data)
        values = pd.Series(values).replace([np.inf, -np.inf], np.nan).dropna()
        values = values.fillna(values.mean())
        res = adfuller(values)
        return res[1]

    def determine_time_series_class(self):
        p_value = self.adf_test()
        if p_value < 0.05:
            s = "Тренд-стационарный"
            f = 0
        else:
            diff_series = self.data.diff().dropna()
            p_value_diff = self.adf_test()
            if p_value_diff < 0.05:
                s = "Разностно-стационарный"
                f = 1
            else:
                s = "Не стационарный"
                f = 2
        return f, s

    def delete_trend_season(self, f):
        if f == 0:
            df1 = self.data - self.data.rolling(window=2).mean()
        elif f == 1:
            df1 = self.data.diff()
        elif f == 2:
            df_not_trend = self.data - self.data.rolling(window=2).mean()
            df1 = df_not_trend.diff()

        df1.dropna(inplace=True)
        plt.plot(self.data, label='Исходный ВР')
        plt.plot(df1, label='ВР после удаления тренда', linestyle='--')
        plt.legend()
        plt.grid()
        plt.xlabel('Дата')
        plt.ylabel('Температура')
        plt.show()

        return df1
