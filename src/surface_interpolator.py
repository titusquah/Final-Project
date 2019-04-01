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
    r"../../well_location_from_earth_model.csv",
#    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\forge_vertices.csv"
    ]

z_names=['granite','land_surf','175c','225c', 'x', 'y']

g_df=pd.read_csv(fnames[0]) #granite
l_df=pd.read_csv(fnames[1]) #land surface
lt_df=pd.read_csv(fnames[2]) #low temp
ut_df=pd.read_csv(fnames[3]) #high temp
well_df=pd.read_csv(fnames[4]) #well location

dfs=[g_df,l_df,lt_df,ut_df]

#%%Interpolator function
def interpolated_sample():
  df_ret = pd.DataFrame(index = np.arange(len(lt_df)), columns = z_names)
  df_wells = pd.DataFrame(index = np.arange(len(well_df)), columns = z_names)
  df_ret['x'], df_ret['y'], df_wells['x'], df_wells['y'] = lt_df['x'], lt_df['y'], well_df['x'], well_df['y']
  for index, df in enumerate(dfs):
    x, y, z = df['x'], df['y'], df['z']
    df_ret[z_names[index]] = interpolate.griddata((x, y), z, (lt_df['x'], lt_df['y']))
    df_wells[z_names[index]] = interpolate.griddata((x, y), z, (well_df['x'], well_df['y']))
  return df_ret.append(df_wells).dropna()
