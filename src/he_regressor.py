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
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)

#p2 = Proj(init="epsg:{0}".format(EPSG), proj="utm", zone=12)
he_df=pd.read_excel(r"..\..\He_R_RA_data-soil gas 3.5.18-FORGE.xlsx")
surf_df=pd.read_csv(r"../../land_surface_vertices.csv")


X= np.array([he_df['UTM East'].values, he_df['UTM North'].values]).T
y=he_df['R/Ra'].values


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
he,sigma=gp.predict(Xs, return_std=True)


he=np.reshape(he,(200,200))
#%%
fig, ax = plt.subplots()
ax.plot(fv.x, fv.y, 'red')
CS = ax.contour(X, Y, he,20)
ax.clabel(CS, inline=1, fontsize=16)

ax.grid(True)
#ax.set_title(r'He R/Ra Contour plot')
plt.show()