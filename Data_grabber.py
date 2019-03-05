# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 07:45:15 2019

@author: Titus
"""
import pandas as pd
import numpy as np
import quandl
import sys
sys.path.insert(0, 'secret_stuff')

from quandl_config import *  

quandl.ApiConfig.api_key = api_key

folder_name='Data/'

stock_query='MULTPL/SP500_REAL_PRICE_MONTH'
fed_rate_query='FRED/FEDFUNDS'

housing_index_query='https://opendata.utah.gov/resource/y7tj-utpv.json'
bldg_permits_query='https://opendata.utah.gov/resource/xcbw-jmby.json'
housing_starts_query='https://opendata.utah.gov/resource/us49-7efj.json'
migration_query='https://opendata.utah.gov/resource/u74u-ydvn.json'

employment_fname='Data/employment_data.xlsx'
income_fname='Data/income_data.csv'

index_df=pd.read_json(housing_index_query)
permits_df=pd.read_json(bldg_permits_query)
starts_df=pd.read_json(housing_starts_query)
migration_df=pd.read_json(migration_query)
employment_df=pd.read_excel(employment_fname)
income_df=pd.read_csv(income_fname)

stock_df=quandl.get(stock_query)

fed_rate_df=quandl.get(fed_rate_query)

names=['index','permits','starts','migration','stock','fed_rate','income']

df_names=[index_df,permits_df,starts_df,migration_df,stock_df,fed_rate_df,income_df]

for i,df in enumerate(df_names):
  df.to_excel('{0}{1}_data.xlsx'.format(folder_name,names[i]))

