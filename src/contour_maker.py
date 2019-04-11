import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from matplotlib import cm
import matplotlib as mpl
from scipy import interpolate
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)
#mpl.style.use('default')
plt.close('all')
fnames=[
    r"..\..\Opal_Mound_Fault_vertices.csv",
    r"..\..\Negro_Mag_Fault_vertices.csv",
    r"..\..\top_granitoid_vertices.csv",
    r"..\..\land_surface_vertices.csv",
    r"..\..\175C_vertices.csv",
    r"..\..\225C_vertices.csv",
    r"..\..\forge_vertices.csv"
    ]
temps=pd.read_csv(r"..\..\well_based_temperature.csv")
pts=pd.read_csv(r"..\..\58-32_pts.csv")

wells_df=pd.read_excel(r"..\..\proposed_well_site.xlsx")

fault1=pd.read_csv(fnames[0])
fault2=pd.read_csv(fnames[1])
granite=pd.read_csv(fnames[2])
surf_df=pd.read_csv(fnames[3])
low=pd.read_csv(fnames[4])
high=pd.read_csv(fnames[5])
vert=pd.read_csv(fnames[6])

n=500
x = np.linspace(min(surf_df['x']),max(surf_df['x']),n)
y = np.linspace(min(surf_df['y']),max(surf_df['y']),n)
X, Y = np.meshgrid(x, y)
x_flatten=X.flatten()
y_flatten=Y.flatten()
Xs=np.column_stack([x_flatten,y_flatten])

#gzs=interpolate.griddata((granite['x'], granite['y']), granite['z'], (x_flatten, y_flatten))
#gzs=np.reshape(gzs,(n,n))
#
#lzs=interpolate.griddata((low['x'], low['y']), low['z'], (x_flatten, y_flatten))
#lzs=np.reshape(lzs,(n,n))
#
#hzs=interpolate.griddata((high['x'], high['y']), high['z'], (x_flatten, y_flatten))
#hzs=np.reshape(hzs,(n,n))

fig,ax=plt.subplots()
ax.plot(fault1['x'],fault1['y'],'kx',label='Opal Fault')
ax.plot(fault2['x'],fault2['y'],'k^',label='Negro Fault')
ax.plot(vert['x'],vert['y'],'k-',label='FORGE footprint')
ax.legend(loc=1)
ax.grid(True)

#gs=ax.contour(X,Y,gzs,colors='green')
#ax.clabel(gs, inline=1, fontsize=10)
#
#ls=ax.contour(X,Y,lzs,colors='blue')
#ax.clabel(ls, inline=1, fontsize=10)
#
#hs=ax.contour(X,Y,hzs,colors='red')
#ax.clabel(hs, inline=1, fontsize=10)
plt.show()
#%%
#wellx=np.array([wells_df['x'][0],wells_df['x'][2]])
#welly=np.array([wells_df['y'][0],wells_df['y'][2]])
#
#
#szs=interpolate.griddata((surf_df['x'], surf_df['y']), surf_df['z'], (wellx,welly))
#gzs=interpolate.griddata((granite['x'], granite['y']), granite['z'], (wellx,welly))
#
#lzs=interpolate.griddata((low['x'], low['y']), low['z'], (wellx,welly))
#
#
#hzs=interpolate.griddata((high['x'], high['y']), high['z'], (wellx,welly))

