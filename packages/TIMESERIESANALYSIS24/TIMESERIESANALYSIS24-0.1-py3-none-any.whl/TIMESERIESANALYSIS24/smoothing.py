import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Smoothing:
    def __init__(self, data):
        self.data = data

    def sma(self, window_size=5):
        df1 = self.data.rolling(window=window_size).mean().dropna()
        return df1

    def ema(self, span=15):
        df1 = self.data.ewm(span=span, adjust=False).mean()
        return df1

    def lwma(self, window_size=5):
        weights = np.arange(1, window_size + 1)
        df1 = self.data.rolling(window=window_size).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).dropna()
        return df1
