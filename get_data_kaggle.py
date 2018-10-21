# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:13:00 2018

@author: Philip
"""

#import packages
import pandas as pd

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt



#%%
#chunk size and frequency

c_size = 460000

os.chdir( "\\path")

csv_url = 'mystery_symbol_train.csv'
#%%
sample_ts = pd.DataFrame()
samples_ts = {}

gm_chunk_resamp = pd.DataFrame()
#i=0
for gm_chunk in pd.read_csv(csv_url,chunksize = c_size):
    #i=i+1
    #print(gm_chunk)
    gm_chunk.index = gm_chunk['time']
    gm_chunk.index = pd.to_datetime(gm_chunk.index)
    gm_chunk.index = gm_chunk.index.to_datetime()
    #gm_chunk_temp = gm_chunk(['bid'] + gm_chunk['ask'])/2
    gm_chunk_resampled = gm_chunk.resample("1h").mean()
    #gm_chunk_resampled = gm_chunk.resample("1h").mean()
    
    gm_chunk_resamp = gm_chunk_resamp.append(gm_chunk_resampled) 
    

data_clean = gm_chunk_resamp.dropna()
#data_clean = gm_chunk_resamp.drop_duplicates(keep='first')
data_clean_d = data_clean.resample("1d").mean()

data_clean_mthly = data_clean.resample("M").mean()

#%%
#do some simple analysis
#choose data
data = data_clean_mthly




#%%
#export:
data_clean.to_csv('algothon_kaggle_hourly.csv')
data_clean.to_csv('algothon_kaggle_daily.csv')



