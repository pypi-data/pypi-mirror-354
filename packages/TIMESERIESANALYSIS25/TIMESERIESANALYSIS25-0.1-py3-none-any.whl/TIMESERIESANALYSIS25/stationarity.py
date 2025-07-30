import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

class Stationarity:
    def __init__(self, data):
        self.data = data

    def adf_test(self):
        result = adfuller(self.data)
        return result[1]

    def determine_class(self):
        p_value = self.adf_test()
        if p_value < 0.05:
            return "Тренд-стационарный", 0
        else:
            diff_series = self.data.diff().dropna()
            p_value_diff = adfuller(diff_series)[1]
            if p_value_diff < 0.05:
                return "Разностно-стационарный", 1
            else:
                return "Не стационарный", 2
