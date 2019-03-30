# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:08:43 2019

@author: Titus
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from matplotlib import cm
import matplotlib as mpl
import shapefile
mpl.style.use('default')
plt.close('all')
fnames=[
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Opal_Mound_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Negro_Mag_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\top_granitoid_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\land_surface_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\175C_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\225C_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\forge_vertices.csv"
    ]
temps=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\well_based_temperature.csv")
pts=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\58-32_pts.csv")
#data={}
#rara=1e9
#for ind,fname in enumerate(fnames):
#    df=pd.read_csv(fname)
#    data['df{0}'.format(ind)]=df
#    if min(df.z)<rara:
#      rara=min(df.z)


#shpFilePath = r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Roosevelt Hot Springs FORGE Site Outline\FORGE_Outline.shp"
#listx=[]
#listy=[]
#test = shapefile.Reader(shpFilePath)
#for sr in test.shapeRecords():
#    for xNew,yNew in sr.shape.points:
#        listx.append(xNew)
#        listy.append(yNew)
#listz=[rara]*len(listx)
#
#for ind,val in enumerate(listx):
#  z_ind=np.argmin((val-data['df3'].x)**2+(listy[ind]-data['df3'].y)**2)
#  listz.append(data['df3'].z[z_ind])
#listx*=2
#listy*=2
#
#forge=pd.DataFrame({'x':listx,'y':listy,'z':listz})
#forge.to_csv('forge_vertices.csv')


#step=1
es=1000
fig = plt.figure()
ax = fig.gca(projection='3d')
for ind,fname in enumerate(fnames):
  
  df=pd.read_csv(fname)
  print(fname,min(df.x),max(df.x),min(df.y),max(df.y),min(df.z),max(df.z),len(df))
#  if len(df)>1000:
#    step=100
#    alpha=0.6
#  elif len(df>100000):
#    step=1000
#    alpha=0.6
#  else:
#    step=1
#    alpha=1
  x=df[(df['x']>=332852.6298-es)&
       (df['x']<=336116.8469+es)&
       (df['y']>=4261250.737-es)&
       (df['y']<=4264610.018+es)]['x']
  y=df[(df['x']>=332852.6298-es)&
       (df['x']<=336116.8469+es)&
       (df['y']>=4261250.737-es)&
       (df['y']<=4264610.018+es)]['y']
  z=df[(df['x']>=332852.6298-es)&
       (df['x']<=336116.8469+es)&
       (df['y']>=4261250.737-es)&
       (df['y']<=4264610.018+es)]['z']
#  ax.plot_trisurf([df.x[i] for i in range(0,len(df),step)], [df.y[i] for i in range(0,len(df),step)], [df.z[i] for i in range(0,len(df),step)], linewidth=0.2, antialiased=True,alpha=alpha)
  if len(x)>1000:
    step=80
  else:
    step=1
  print(len(x[::step]))
  try:
    if ind!=len(fnames)-1:
      ax.plot_trisurf(x[::step],y[::step],z[::step] ,linewidth=0.2, antialiased=True,alpha=0.5)
  except:
    pass
x_bot=[]
y_bot=[]
z_bot=[]
for i in range(len(x)):
  x_bot.append(x[i])
  y_bot.append(y[i])
  z_bot.append(-2606)
ax.plot3D(x, y, z, 'red')
ax.plot3D(x_bot, y_bot, z_bot, 'red')
for i in range(len(x)):
  ax.plot3D([x[i],x_bot[i]], [y[i],y_bot[i]], [z[i],z_bot[i]], 'red')
ax.plot3D(pts['x'],pts['y'],pts['z'])
pts=ax.scatter3D(temps[(temps['T']>=175)&(temps['T']<=225)]['x'],
                   temps[(temps['T']>=175)&(temps['T']<=225)]['y'],
                   temps['z'][(temps['T']>=175)&(temps['T']<=225)],
                   c=temps['T'][(temps['T']>=175)&(temps['T']<=225)],
                   cmap='inferno')
fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()