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


step=1
fig = plt.figure()
ax = fig.gca(projection='3d')
for ind,fname in enumerate(fnames):
  df=pd.read_csv(fname)
  if len(df)>100:
    step=100
    alpha=0.6
  else:
    step=1
    alpha=1
  ax.plot_trisurf([df.x[i] for i in range(0,len(df),step)], [df.y[i] for i in range(0,len(df),step)], [df.z[i] for i in range(0,len(df),step)], linewidth=0.2, antialiased=True,alpha=alpha)


plt.show()