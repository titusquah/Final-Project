# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:00:03 2019

@author: Titus
"""

import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn import metrics
from sklearn.cluster import *
from sklearn.metrics import homogeneity_score, homogeneity_completeness_v_measure
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
from sklearn.cluster import DBSCAN

fracts=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\surface_fractures_extended.csv",index_col=0)
forge_outline=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\forge_vertices.csv",index_col=0)


fr_x=fracts['x'].values
fr_y=fracts['y'].values

X=[]
for i in range(len(fr_x)):
  X.append([fr_x[i],fr_y[i]])
X=np.array(X)
#Z = linkage(X, 'ward') # generate the linkage array

plt.close('all')
db_model = DBSCAN(eps=0.5, min_samples=4)
db_model.fit(X)
y_pred = db_model.fit_predict(X)

plt.scatter(X[:, 0], X[:, 1],s=0.1, c=y_pred); 
plt.plot(forge_outline['x'],forge_outline['y'])
plt.show()

#plt.figure(figsize=(25, 10))
#plt.title('Hierarchical Clustering Dendrogram')
#plt.xlabel('sample index')
#plt.ylabel('distance')
#dendrogram(Z,
#    leaf_rotation=90.,  # rotates the x axis labels
#    leaf_font_size=8. # font size for the x axis labels
#)
#plt.show()
