# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:41:17 2019

@author: Titus
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

df=pd.read_csv(r"../../58-32_sonic_log_data.csv")
scatter_matrix(df)
plt.show()
