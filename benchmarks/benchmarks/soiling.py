"""
ASV benchmarks for soiling.py
"""
import pandas as pd
import numpy as np
from pvlib import soiling

class Soiling:
    params = [1, 365, 365*5]
    param_names = ['ndays']

    def setup(self, ndays):
        self.time = pd.date_range(start='20200808', freq='1h', periods=24*ndays)
        self.rainfall = pd.Series(np.zeros(ndays*24), index=self.time)
        self.pm2_5 = pd.Series(np.random.rand(ndays*24), index=self.time)
        self.pm10 = pd.Series(np.random.rand(ndays*24), index=self.time)
        self.tilt = 30

    def time_hsu(self, ndays):
        cleaningthreshold = 0.5
        soiling.hsu(self.rainfall, cleaningthreshold,
                    self.tilt, self.pm2_5, self.pm10)

    def time_test(self, nadys):
        soiling.hsu(self.rainfall)

    def time_kimber(self, ndays):
        cleaningthreshold = 25
        soiling.kimber(self.rainfall, cleaningthreshold)