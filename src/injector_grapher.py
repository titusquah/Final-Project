# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:05:58 2019

@author: Titus
"""

import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r'..\..\58-32_Phase2B_injection_data_pressure.csv')
df1=pd.read_csv(r'..\..\58-32_Phase2B_injection_data_flow.csv')
plt.close('all')
fig,ax=plt.subplots(2)
ax[0].plot(df['Time (hr)'],df['Pressure (MPa)'])
ax[1].plot(df1['Time (hr)'],df1['Flow (Liter/min)'])
plt.show()