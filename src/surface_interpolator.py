# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:19:45 2019

@author: Titus
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp2d
from scipy import interpolate
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#%%Load data
fnames=[
#    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Opal_Mound_Fault_vertices.csv",
#    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Negro_Mag_Fault_vertices.csv",
    r"../../top_granitoid_vertices.csv",
    r"../../land_surface_vertices.csv",
    r"../../175C_vertices.csv",
    r"../../225C_vertices.csv",
#    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\forge_vertices.csv"
    ]

z_names=['granite','land_surf','175c','225c' ]


g_df=pd.read_csv(fnames[0]) #granite
l_df=pd.read_csv(fnames[1]) #land surface
lt_df=pd.read_csv(fnames[2]) #low temp
ut_df=pd.read_csv(fnames[3]) #high temp

dfs=[g_df,l_df,lt_df,ut_df]


#%%Interpolator function
def vertices_interp(xi,yi): #takes in x and y value within data bounds and 
#returns data frame with granite,landsurface and temperature z's
  try:
    n=len(xi)
  except:
    try:
      int(xi)
      n=1
    except Exception as e:
      print(e) 
      raise
  
  df_ret = pd.DataFrame(index=np.arange(n),columns=z_names)
  for ind,df in enumerate(dfs):
    x=df['x']
    y=df['y']
    z=df['z']
    vals = interpolate.griddata((x, y), z, (xi,yi))
    df_ret[z_names[ind]]=vals
  return df_ret
  
  
