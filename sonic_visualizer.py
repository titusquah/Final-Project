# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:41:17 2019

@author: Titus
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.decomposition import PCA 
#df=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\58-32_sonic_log_data.csv")

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Final-project-data/Data/58-32_main_geophysical_well_log.csv"
abs_file_path = os.path.join(script_dir, rel_path)

df=pd.read_csv(abs_file_path,index_col=0)

plt.show()