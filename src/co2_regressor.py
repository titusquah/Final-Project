# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:06:40 2019

@author: Titus
"""

from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as ker
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fault_visulizer as fv
import utm
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)

EPSG=26912

co2_df=pd.read_excel(r"..\..\UtahFORGE_CO2_statistics2018\UtahFORGE_CO2_statistics2018.xlsx")
surf_df=pd.read_csv(r"../../land_surface_vertices.csv")

x=[]
y=[]
zones=[]
letters=[]
for i in range(len(co2_df)):
  easting,northing,zone,letter=utm.from_latlon(co2_df['latitude'][i],co2_df['longitude'][i])
  x.append(easting)
  y.append(northing)
  zones.append(zone)
  letters.append(letter)
co2_df['x']=x
co2_df['y']=y

X= np.array([co2_df['x'].values, co2_df['y'].values]).T
y=co2_df['fluxperday'].values


#%% KRIGING

kernel =   ker.ConstantKernel()+ker.RBF()+ker.RationalQuadratic()


gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,normalize_y=True)
gp.fit(X, y)

print(gp.score(X, y))
#%%
x = np.linspace(min(surf_df['x']),max(surf_df['x']),200)
y = np.linspace(min(surf_df['y']),max(surf_df['y']),200)
X, Y = np.meshgrid(x, y)
x_flatten=X.flatten()
y_flatten=Y.flatten()
Xs=np.column_stack([x_flatten,y_flatten])
co2,sigma=gp.predict(Xs, return_std=True)


co2=np.reshape(co2,(200,200))
#%%
fig, ax = plt.subplots()
ax.plot(fv.x, fv.y, 'red')
CS = ax.contour(X, Y, co2,30)
ax.clabel(CS, inline=1, fontsize=10)
#ax.set_title(r'$CO_2$ flux Contour plot')
ax.grid(True)
plt.show()