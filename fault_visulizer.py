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
mpl.style.use('classic')
plt.close('all')
fnames=[
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Opal_Mound_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Negro_Mag_Fault_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\top_granitoid_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\land_surface_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\175C_vertices.csv",
    r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\225C_vertices.csv"
    ]

labels=['Opal fault','Negro fault','Granite', 'Surface','175 deg C','225 deg C']
#image_name=r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Geologic_map_no_quaternary.png"
#im = plt.imread(image_name)

c_str="Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r"
cmaps=c_str.replace(' ','').split(',')


fig = plt.figure()
ax = fig.gca(projection='3d')
for ind,fname in enumerate(fnames):
  df=pd.read_csv(fname)
  ax.plot_trisurf([df.x[i] for i in range(0,len(df),100)], [df.y[i] for i in range(0,len(df),100)], [df.z[i] for i in range(0,len(df),100)], linewidth=0.2, antialiased=True,alpha=0.5,label=labels[ind])
ax.legend(loc='best')
#fig,ax=plt.subplots()
##implot = ax.imshow(im,extent=(0,xmax-xshift,0,ymax-yshift))
##ax.scatter([0,0,xmax-xshift,xmax-xshift],[0,ymax-yshift,0,ymax-yshift])
##for fname in fnames:
##  df=pd.read_csv(fname)
##  ax.scatter(df.x-xshift, df.y-yshift)


plt.show()