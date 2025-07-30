import pandas as pd
import numpy as np

class Smoothing:
    def __init__(self, data):
        self.data = data

    def sma(self, window_size=5):
        return self.data.rolling(window=window_size).mean().dropna()

    def ema(self, span=15):
        return self.data.ewm(span=span, adjust=False).mean()

    def lwma(self, window_size=5):
        weights = np.arange(1, window_size + 1)
        return self.data.rolling(window=window_size).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).dropna()
