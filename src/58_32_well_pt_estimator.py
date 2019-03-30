# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:06:02 2019

@author: Titus
"""
import pandas as pd
import numpy as np
pi=np.pi

df=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\well_survey_from_earth_model.csv")
dips=pi/2-df[df['Well ID']=='58-32']['Dip'].values/180*pi
azs=df[df['Well ID']=='58-32']['Azimuth'].values/180*pi
depths=df[df['Well ID']=='58-32']['Depth (m)'].values


max_depth=2296.9

z0=1681.616587
x=[335380.766]
y=[4263040.829]
z=np.append(depths,max_depth)


xys=[(z[i+1]-z[i])*np.tan(dips[i]) for i in range(len(z)-1)]
for ind,xy in enumerate(xys):
  x.append(x[-1]+xy*np.sin(azs[ind]))
  y.append(y[-1]+xy*np.cos(azs[ind]))

z=z0-z
pd.DataFrame({'x':x,'y':y,'z':z}).to_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\58-32_pts.csv")