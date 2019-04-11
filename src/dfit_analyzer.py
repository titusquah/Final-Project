import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)
flow_df=pd.read_csv(r"..\..\58-32_Phase2B_injection_data_flow.csv")
psi_df=pd.read_csv(r"..\..\58-32_Phase2B_injection_data_pressure.csv")


plt.close('all')
fig,ax=plt.subplots()
#ax.plot(flow_df['Time (hr)'],flow_df['Flow (barrel/min)']*3000)
ax.plot(psi_df['Time (hr)'],psi_df['Pressure (psi)'])
ax.set_xlabel('Time (hr)')
ax.set_ylabel('Pressure (psi)')
ax.grid(True)
plt.show()