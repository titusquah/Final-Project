# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:29:52 2019

@author: Titus
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

main_df=pd.read_csv(r"../../58-32_main_geophysical_well_log.csv")

for col in main_df.columns:
  main_df=main_df[main_df[col]!=1950]

sonic_df=pd.read_csv(r"../../58-32_sonic_log_data.csv")
for col in sonic_df.columns:
  sonic_df=sonic_df[sonic_df[col]>-500]

litho_df=pd.read_csv("../../58-32_xray_diffraction_data.csv")
litho_df=litho_df.replace('tr',0.1)
litho_df=litho_df.replace('t',0.1)
litho_df['% chlorite in C/S']=litho_df['% chlorite in C/S'].str.replace(r'%', r'.0').astype('float') / 100.0
litho_df=litho_df.fillna(0)

for col in litho_df.columns:
  litho_df[col]=litho_df[col].astype('float')
litho_cols=litho_df.columns

fmi=np.genfromtxt(r"..\..\58-32_logs\Logs\University_of_Utah_MU_ESW1_FMI_HD_7440_7550ft_Dip_Final_2ndRun_DFC.las",skip_header=150)
fmi_cols='''TDEP               .ft                                     :  {F}
Breakout_Flag      .unitless                               :  {F}
Conductive_Continuous_Fracture_COUNT .unitless                               :  {F}
Conductive_Fracture_Count_Summation .unitless                               :  {F}
Conductive_Part_Resistive_Fracture_COUNT .unitless                               :  {F}
Count_SUM          .unitless                               :  {F}
Longitudinal_Induced_Fracture_Flag .unitless                               :  {F}
P10_Conductive_Continuous_Fracture .1/ft                                   :  {F}
P10_Conductive_Continuous_Fracture_C .1/ft                                   :  {F}
P10_Conductive_Part_Resistive_Fracture .1/ft                                   :  {F}
P10_Conductive_Part_Resistive_Fracture_C .1/ft                                   :  {F}
P10_SUM            .1/ft                                   :  {F}
P10_SUM_C          .1/ft                                   :  {F}
P21_Conductive_Continuous_Fracture .1/ft                                   :  {F}
P21_Conductive_Continuous_Fracture_Trace .1/ft                                   :  {F}
P21_Conductive_Fracture .1/ft                                   :  {F}
P21_Conductive_Fracture_Integration .1/ft                                   :  {F}
P21_Conductive_Part_Resistive_Fracture .1/ft                                   :  {F}
P21_Conductive_Part_Resistive_Fracture_Trace .1/ft                                   :  {F}
P21_Resistive_Fracture .1/ft                                   :  {F}
P21_Resistive_Fracture_Integration .1/ft                                   :  {F}
P21_SUM            .1/ft                                   :  {F}
P21_Trace_SUM      .1/ft                                   :  {F}
P32_Conductive_Continuous_Fracture .1/ft                                   :  {F}
P32_Conductive_Continuous_Fracture_Trace .1/ft                                   :  {F}
P32_Conductive_Part_Resistive_Fracture .1/ft                                   :  {F}
P32_Conductive_Part_Resistive_Fracture_Trace .1/ft                                   :  {F}
P32_SUM            .1/ft                                   :  {F}
P32_Trace_SUM      .1/ft                                   :  {F}
P33_Conductive_Continuous_Fracture_Trace .v/v                                    :  {F}
P33_Conductive_Fracture_Trace .v/v                                    :  {F}
P33_Conductive_Fracture_Trace_Integration .v/v                                    :  {F}
P33_Conductive_Part_Resistive_Fracture_Trace .v/v                                    :  {F}
P33_Trace_SUM      .v/v                                    :  {F}
Resistive_Fracture_Count_Summation .unitless                               :  {F}
Shear_Induced_Fracture_Flag .unitless                               :  {F}
Tensile_Induced_Fracture_Flag .unitless                               :  {F}'''
fmi_cols=fmi_cols.replace(' ','').replace(':','').replace('{F}','').split('\n')
fmi_df=pd.DataFrame()
for ind,col in enumerate(fmi_cols):
  fmi_df[col]=fmi[:,ind]
hi=fmi_df.describe()
col_float=hi.loc['max'].values!=hi.loc['max'].astype(int).values
col_float=np.where(col_float==True)[0].tolist()
rara=[fmi_cols[i] for i in col_float]

fmi_df.plot(rara[0],[
 'P10_Conductive_Continuous_Fracture_C.1/ft',
 'P10_Conductive_Part_Resistive_Fracture_C.1/ft',
 'P10_SUM_C.1/ft',
 'P21_Conductive_Continuous_Fracture.1/ft',
 'P21_Conductive_Continuous_Fracture_Trace.1/ft',
 'P21_Conductive_Fracture.1/ft',
 'P21_Conductive_Part_Resistive_Fracture.1/ft',
 'P21_Conductive_Part_Resistive_Fracture_Trace.1/ft',
 'P21_SUM.1/ft',
 'P21_Trace_SUM.1/ft',
 'P32_Conductive_Continuous_Fracture.1/ft',
 'P32_Conductive_Continuous_Fracture_Trace.1/ft',
 'P32_Conductive_Part_Resistive_Fracture.1/ft',
 'P32_Conductive_Part_Resistive_Fracture_Trace.1/ft',
 'P32_SUM.1/ft',
 'P32_Trace_SUM.1/ft',
 'P33_Conductive_Continuous_Fracture_Trace.v/v',
 'P33_Conductive_Fracture_Trace.v/v',
 'P33_Conductive_Fracture_Trace_Integration.v/v',
 'P33_Conductive_Part_Resistive_Fracture_Trace.v/v',
 'P33_Trace_SUM.v/v'])
plt.show()
#%%
start=0
j=0
cols=main_df.columns
plt.close('all')
fig,ax=plt.subplots(nrows=4,ncols=5)


for colno in range(start,start+20):
  if (colno-start)%5==0 and colno-start!=0:
    j+=1
  
  
  ax[j,(colno-start)%5].plot(main_df[cols[0]],main_df[cols[colno]].rolling(100).mean(),label='{0}'.format(cols[colno]))
  ax[j,(colno-start)%5].legend(loc=2)
  
    
plt.show()
#%%
start=6
j=0

#plt.close('all')
fig,ax=plt.subplots(nrows=4,ncols=5)
cols=sonic_df.columns
for colno in range(start,start+20):
  if (colno-start)%5==0 and colno-start!=0:
    j+=1
  
  
  ax[j,(colno-start)%5].plot(sonic_df[cols[0]],sonic_df[cols[colno]].rolling(100).mean(),label='{0}'.format(cols[colno]))
  ax[j,(colno-start)%5].legend(loc=2)
  
    
plt.show()
#%%
plt.close('all')
litho_df.plot(x='Lower Depth Range (m)',y=['Plagioclase', 'K-feldspar', 'Quartz'])
plt.plot(sonic_df['Depth (m)'],sonic_df['SPHI'].rolling(50).mean()*60,label='Sonic Poro')
plt.plot(sonic_df['Depth (m)'],sonic_df['PR'].rolling(50).mean()*60,label='poisson')
plt.plot(main_df['Depth (m)'],main_df['HGR']/10+70,label='Gamma')
plt.legend(loc=2)
plt.show()
#%%