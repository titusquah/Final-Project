import pandas as pd
import numpy as np
from scipy import interpolate

df=pd.read_excel(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\ut_tg_data.xls")



surf_df=pd.read_csv(r"../../land_surface_vertices.csv")
minx=min(surf_df['x'])
maxx=max(surf_df['x'])

miny=min(surf_df['y'])
maxy=max(surf_df['y'])
#interpolate.griddata((surf_df['x'], surf_df['y']), surf_df['z'], (, ))


water_df=pd.read_excel(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\FORGE_groundwater_tables.xlsx",header=7)
water_df=water_df.set_index('Label1').dropna()[['Easting3', 'Northing','Land Elev (ft)', 'DTW (ft)4', 'Water Elev (ft)']]
water_df=water_df[(water_df['DTW (ft)4']>0)&(water_df['Easting3']>minx)&(water_df['Easting3']<maxx)&\
                  (water_df['Northing']>miny)&(water_df['Northing']<maxy)]

df=df[['UTM_E','UTM_N','DEPTH_M','WAT_TABLE','START_M','END_M','AVGTCU','UCGRAD']]
df=df[(df['DEPTH_M'].notnull())|(df['START_M'].notnull())]
df=df.reset_index(drop=True)
depth=[]
for i in range(len(df)):
  if np.isnan(df['END_M'][i]) or df['END_M'][i]==0:
    depth.append(df['DEPTH_M'][i])
  else:
    depth.append(df['END_M'][i])
    
df['depth']=depth

#h2o=df[['UTM_E','UTM_N','WAT_TABLE']]
#h2o=h2o[(h2o['WAT_TABLE'].notnull())&(h2o['WAT_TABLE']!='Flowing')]
##h2o=h2o[(h2o['UTM_E']>minx)&(h2o['UTM_E']<maxx)&(h2o['UTM_N']>miny)&(h2o['UTM_N']<maxy)]
#h2o=h2o.astype(float).reset_index(drop=True)
##h2o['z']=interpolate.griddata((surf_df['x'], surf_df['y']), surf_df['z'], (h2o['UTM_E'],h2o['UTM_N'] ))-h2o['WAT_TABLE']

atcu=df[['UTM_E','UTM_N','depth','AVGTCU']]
atcu=atcu[(atcu['AVGTCU'].notnull())&(atcu['AVGTCU']!=0)].reset_index(drop=True)
atcu=atcu[(atcu['UTM_E']>minx)&(atcu['UTM_E']<maxx)&(atcu['UTM_N']>miny)&(atcu['UTM_N']<maxy)] #thermal conductivity
atcu['z']=interpolate.griddata((surf_df['x'], surf_df['y']), surf_df['z'], (atcu['UTM_E'],atcu['UTM_N'] ))-atcu['depth']



ucg=df[['UTM_E','UTM_N','depth','UCGRAD']]
ucg=ucg[(ucg['UCGRAD'].notnull())&(ucg['UCGRAD']!=0)].reset_index(drop=True)
ucg=ucg[(ucg['UTM_E']>minx)&(ucg['UTM_E']<maxx)&(ucg['UTM_N']>miny)&(ucg['UTM_N']<maxy)] #thermal gradient
ucg['z']=interpolate.griddata((surf_df['x'], surf_df['y']), surf_df['z'], (ucg['UTM_E'],ucg['UTM_N'] ))-ucg['depth']

save1=pd.DataFrame({'x':water_df['Easting3'],'y':water_df['Northing'],'z':water_df['Water Elev (ft)']}).reset_index(drop=True)
save2=pd.DataFrame({'x':atcu['UTM_E'],'y':atcu['UTM_N'],'z':atcu['z'],'thermal_conductivity':atcu['AVGTCU']}).reset_index(drop=True)
save3=pd.DataFrame({'x':ucg['UTM_E'],'y':ucg['UTM_N'],'z':ucg['z'],'temp_gradient':ucg['UCGRAD']}).reset_index(drop=True)

save1.to_csv('water_table_pts.csv')
save2.to_csv('thermal_conductivity_pts.csv')
save3.to_csv('temp_gradient_pts.csv')

