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
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)
plt.close('all')
fnames=[
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Opal_Mound_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Negro_Mag_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\land_surface_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\top_granitoid_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\175C_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\225C_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\forge_vertices.csv"
    ]
temps=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\well_based_temperature.csv")
pts=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\58-32_pts.csv")
wells_df=pd.read_excel(r"..\..\proposed_well_site.xlsx")
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
names=['Opal Fault','Negro fault','Land surface','Top of Granite Surface',r'Top of 175 $^o$C surface',r'Top of 225 $^o$C surface']
colors=['b','b','g','k','r','b','m']
#step=1
es=100
fig = plt.figure()
ax = fig.gca(projection='3d')
for ind,fname in enumerate(fnames):
  
  df=pd.read_csv(fname)
#  print(fname,min(df.x),max(df.x),min(df.y),max(df.y),min(df.z),max(df.z),len(df))
  if len(df)>1000:
    step=100
    alpha=0.6
  elif len(df>100000):
    step=1000
    alpha=0.6
  else:
    step=1
    alpha=1
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
#  x=df['x']
#  y=df['y']
#  z=df['z']
#  ax.plot_trisurf([df.x[i] for i in range(0,len(df),step)], [df.y[i] for i in range(0,len(df),step)], [df.z[i] for i in range(0,len(df),step)], linewidth=0.2, antialiased=True,alpha=alpha)
  if len(x)>1000:
    step=80
  elif len(x)>10000:
    step=1000
  else:
    step=1
#  print(len(x[::step]))
  try:
    if ind!=len(fnames)-1:
      ax.plot_trisurf(x[::step],y[::step],z[::step] ,linewidth=0.2, antialiased=True,alpha=0.5)#,label=names[ind])
      fake2Dline = mpl.lines.Line2D([332852.6298-es],[4261250.737-es], linestyle="none", marker = 'o',label=names[ind])
      ax.legend([fake2Dline], [names[ind]], numpoints = 1)
  except:
    pass
x_bot=[]
y_bot=[]
z_bot=[]
for i in range(len(x)):
  x_bot.append(x[i])
  y_bot.append(y[i])
  z_bot.append(-2606)
ax.plot3D(x, y, z, 'red',label='Forge footprint')
#ax.plot3D(x_bot, y_bot, z_bot, 'red',label='')
#for i in range(len(x)):
#  ax.plot3D([x[i],x_bot[i]], [y[i],y_bot[i]], [z[i],z_bot[i]], 'red',label='')
ax.plot3D(pts['x'],pts['y'],pts['z'],label='Well 58-32')
ax.plot3D([wells_df['x'][0],wells_df['x'][0]],[wells_df['y'][0],wells_df['y'][0]],[1702.80849777,-615],label='Injection well')
ax.plot3D([wells_df['x'][2],wells_df['x'][2]],[wells_df['y'][2],wells_df['y'][2]],[1702.80849777,-615],label='Production well')
ax.legend()
#pts=ax.scatter3D(temps[(temps['T']>=175)&(temps['T']<=225)]['x'],
#                   temps[(temps['T']>=175)&(temps['T']<=225)]['y'],
#                   temps['z'][(temps['T']>=175)&(temps['T']<=225)],
#                   c=temps['T'][(temps['T']>=175)&(temps['T']<=225)],
#                   cmap='inferno')
#pts=ax.scatter3D(temps['x'],
#                   temps['y'],
#                   temps['z'],
#                   c=temps['T'],
#                   cmap='inferno')
#fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()