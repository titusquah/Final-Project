# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 01:28:34 2019

@author: Titus
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import core_photo_analyzer as cpa
d1=7448.1
d2=7449.55

folder="../../58_32_Core_CT_Scans/7448.1-7449.55"
n=len(os.listdir(folder))
dz=(d2-d1)/n
z=d1

xs=[]
ys=[]
zs=[]

for file in os.listdir(folder):
  pts=cpa.white_finder(folder+'/'+file,z)
#  try:
  for i in range(len(pts[0])):
    xs.append(pts[0][i])
    ys.append(pts[1][i])
    zs.append(pts[2][i])
#  except:
#    pass
  z+=dz
    
#%%
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter3D(xs[::1],ys[::1],zs[::1],s=1)
plt.show()