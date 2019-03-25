# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:33:50 2019

@author: Titus
"""
import numpy as np
import shapefile
from matplotlib.path import Path
import matplotlib.pyplot as plt
from matplotlib import patches
import pandas as pd

shpFilePath = r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Roosevelt Hot Springs FORGE Site Outline\FORGE_Outline.shp"
listx=[]
listy=[]
test = shapefile.Reader(shpFilePath)
for sr in test.shapeRecords():
    for xNew,yNew in sr.shape.points:
        listx.append(xNew)
        listy.append(yNew)
        
xlist=np.array(listx)
ylist=np.array(listy)
tupVerts=[]
for ind,xval in enumerate(xlist):
  tupVerts.append((xval,ylist[ind]))


x, y = np.meshgrid(np.linspace(min(xlist),max(xlist),1000), np.linspace(min(ylist),max(ylist),1000)) # make a canvas with coordinates
x, y = x.flatten(), y.flatten()
#points = np.vstack((x,y)).T 
points=np.array([[333594,4264000]])

p = Path(tupVerts) # make a polygon
grid = p.contains_points(points)
#mask = grid.reshape(1000,1000) # now you have a mask with points inside a polygon
#
#grid=np.array(grid)
#grid=grid.astype(int)
#
#forge_classifier=pd.DataFrame({'x':points[:,0],'y':points[:,1],'in':grid})
#forge_classifier.to_csv('forge_classifier.csv',index=False)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#patch = patches.PathPatch(p, facecolor='orange', lw=2)
#ax.add_patch(patch)
#ax.set_xlim(min(xlist),max(xlist))
#ax.set_ylim(min(ylist),max(ylist))
#plt.show()

#plt.figure()
#plt.scatter(points[:,0],points[:,1],c=grid)
#plt.show()