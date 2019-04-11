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
grav_df=pd.read_csv(r"..\..\gravity_pts.csv")
surf_df=pd.read_csv(r"../../land_surface_vertices.csv")


X= np.array([grav_df['x'].values, grav_df['y'].values]).T
y=grav_df['cbga'].values

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
grav,sigma=gp.predict(Xs, return_std=True)


grav=np.reshape(grav,(200,200))
#%%
fig, ax = plt.subplots()
ax.plot(fv.x, fv.y, 'red')
CS = ax.contour(X, Y, grav)
ax.clabel(CS, inline=1, fontsize=16)
#ax.set_title('Estimated Complete Bouguer gravity anomaly value Contour plot')
ax.grid(True)
plt.show()


