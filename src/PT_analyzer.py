# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:11:25 2019

@author: Titus
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Depth        T          LSPD       DTEMP        PRES       DPRES    
data=np.genfromtxt(r"..\..\58-32_Temp_Pres_11_08_18\UOFU_MU-ESW1_PT118.txt",skip_header=70)
names=['Depth','T','LSPD','DTEMP','PRES','DPRES']
dic={}
for ind,name in enumerate(names):
  dic[name]=data[:,ind]
df=pd.DataFrame(dic)
for name in names:
  df=df[df[name]!=-999.25]

i=1


fig,ax=plt.subplots(len(data[0])-1)
for i in range(len(data[0])-1):
  ax[i].plot(df['Depth'],df[names[i+1]])
  ax[i].set_ylabel(names[i+1])
plt.show()
  