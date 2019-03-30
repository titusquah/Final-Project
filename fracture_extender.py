# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 12:04:30 2019

@author: Titus
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
df=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\surface_fractures_group_by_shape.csv",index_col=0)
pts=100

xpts=[]
ypts=[]

for i in range(len(df)):
  x=df['x'][i]
  x=x.replace('[','').replace(']','').replace(' ','').split(',')
  x=[float(hi) for hi in x]
  
  y=df['y'][i]
  
  y=y.replace('[','').replace(']','').replace(' ','').split(',')
  y=[float(hi) for hi in y]
  
  lazy=interp1d(x,y)
  newx=np.linspace(min(x),max(x),pts)
  newy=lazy(newx)
  
  for i in range(len(newx)):
    xpts.append(newx[i])
    ypts.append(newy[i])
new_df=pd.DataFrame({'x':xpts,'y':ypts})