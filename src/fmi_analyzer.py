# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:36:25 2019

@author: Titus
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplstereonet
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)

psi_df=pd.read_csv(r"..\..\FMI_log.csv")
psi_df = psi_df.loc[:, (psi_df != -9999).any(axis=0)].replace(-9999,np.nan)
cols=psi_df.columns
new_cols=[ x for x in cols if "APERTURE" not in x ]
new_cols=[ x for x in new_cols if "Info" not in x ]
psi_df = psi_df[new_cols]
cols=psi_df.columns
new_cols=[]

for ind,col in enumerate(cols):
  new_cols.append(col.replace(' ','').replace(':','').replace('\'','').replace('{F}','').replace('{S}',''))
psi_df.columns=new_cols

azimuth=psi_df[(psi_df[new_cols[18]].notnull())&(psi_df[new_cols[0]]>7445)&(psi_df[new_cols[0]]<7544)][new_cols[2]]
dips=psi_df[(psi_df[new_cols[19]].notnull())&(psi_df[new_cols[0]]>7445)&(psi_df[new_cols[0]]<7544)][new_cols[10]]

bin_edges = np.arange(-5, 366, 10)
number_of_azimuth, bin_edges = np.histogram(azimuth, bin_edges)
number_of_azimuth[0] += number_of_azimuth[-1]
half = np.sum(np.split(number_of_azimuth[:-1], 2), 0)
two_halves = np.concatenate([half, half]) 
two_halves=two_halves/sum(two_halves)
fig = plt.figure(figsize=(16,8))

ax = fig.add_subplot(121, projection='stereonet')

ax.pole(azimuth, dips, c='k', label='Pole of the Planes')
ax.density_contourf(azimuth, dips, measurement='poles', cmap='Reds')
#ax.set_title('Density contour of the Poles', y=1.10, fontsize=15)
ax.grid()

ax = fig.add_subplot(122, projection='polar')

ax.bar(np.deg2rad(np.arange(0, 360, 10)), two_halves, 
       width=np.deg2rad(10), bottom=0.0, color='.8', edgecolor='k')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_thetagrids(np.arange(0, 360, 10), labels=np.arange(0, 360, 10))
#ax.set_rgrids(np.arange(1, two_halves.max() + 1, 2), angle=0, weight= 'black')
#ax.set_title('Rose Diagram of the "Fault System"', y=1.10, fontsize=15)
