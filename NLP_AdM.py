#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 14:11:42 2018

@author: andreademarco
"""

import pandas as pd
import datetime
#import requests
#from bs4 import BeautifulSoup
import re
import string
from textblob import TextBlob as tb

# Initialising Data Frames
df = pd.DataFrame(columns=['title'])
df_t = pd.DataFrame(columns=['timeStamp'])
df_t_1 = pd.DataFrame(columns=['timeStamp'])
df_t_2 = pd.DataFrame(columns=['timeStamp'])
df_1 = pd.DataFrame(columns=['title'])
df_3 = pd.DataFrame(columns=['Date', 'Score'])

# Change path by day increments from 2014 to 2017 using a for loop
date_start =  datetime.datetime(2014,1,1,0)
date_end = datetime.datetime(2017,12,31,0)
date_range = (date_end - date_start).days
date = datetime.datetime(2014,1,1,0)
for k in range(date_range): #subsitute for date_range
    
    date_path = date.strftime("%Y%m%d")
    
    path = "reuters/%s.pkl" %date_path
    print(path)

    dict_a = pd.read_pickle(path)
    dict_l = len(dict_a)

    i = 0
    for i in range(dict_l): 
        dict_b = dict_a[i]
        title = dict_b["title"]
        timeStamp = dict_b["ts"]
        df_t.loc[i] =  timeStamp
        df.loc[i] = title

    # Next we must preprocess this data - Remove punctuations, make lower case.    
    def clean_text_round1(text):
        '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
        text = text.lower() # small letters
        text = re.sub('\[.*?\]', ' ', text) #Removing text within the square brackets
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text) #Removing punctuation
        text = re.sub('\w*\d\w*', ' ', text) # Numbers and any characters associated with the digits
        text = re.sub('[‘’“”…]', ' ', text) # remove more punctuation
        text = re.sub('\n', ' ', text) # remove \n
        return text
        
    # Clean 
    def clean_text_round2(text):
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #Removing punctuation
        return text
    
    j = 0
    for j in range(dict_l): 
        x = df.loc[j]
        round1 = lambda x: clean_text_round1(x)
        df_1.loc[j] = df.loc[j].transform(round1)
        # For each hour in the timestamp
        ts_str = df_t.loc[j].str
        if ts_str.contains('P').bool() == True:
            df_t_1.loc[j] = ts_str[9:11]
            round2 = lambda x: clean_text_round2(x)
            df_t_2.loc[j] = int(df_t_1.loc[j].transform(round2))+12
        else:
            df_t_1.loc[j] = ts_str[9:11]
            round2 = lambda x: clean_text_round2(x)
            df_t_2.loc[j] = int(df_t_1.loc[j].transform(round2))
    
        # Add this column to df_1
        df_1['hour'] = df_t_2
    
    # Get a sentiment score on average of every day
    # This is where we must remove the rows which are irrelevent to our problem.
    # Add dictionary from Loughran and MacDonald and Custom
    dict_fin = pd.read_csv('lm_md.csv')
    list_fin_1 = dict_fin['Word'].values.tolist()
    list_fin_1 = [x for x in list_fin_1 if str(x) != 'nan']
    list_fin_2 = ['dollar', 'increase', 'ex', 'tech', 'decrease', 'yield', 'capital', 'fin', 'crisis',
                  'share', 'stock', 'long', 'short', 'buy', 'sell', 'invest', 'inflat', 'tax']
    list_fin = list_fin_1 + list_fin_2
    df_2 = df_1[df_1.title.str.contains('|'.join(list_fin))]

    print(dict_l)
    print(len(df_2))
    
    # Using textblob    
    pol = lambda x: tb(x).sentiment.polarity
    #sub = lambda x: tb(x).sentiment.subjectivity
    
    df_2['polarity'] = df_2['title'].apply(pol)
    #df_2['subjectivity'] = df_2['title'].apply(sub)
    
    # Using pysentiment
    #import pysentiment as ps
    #model = ps.lm()
    #tokens = model.tokenize(df_2.loc[0])
    #df_2['score'] = model.get_score(tokens)
    #pysentiment library --> Loughran and MacDonald   
    
    # Save score for every day.
    #score = df_2['polarity'].mean()
    #df_3.loc[k] = [date,  score]
    #date += datetime.timedelta(days=1)
    #m=1
    for m in range(24):
        # Score group by hour
        score = df_2.groupby(['hour'])['polarity'].mean()
        if score.get(m) == None:
            df_3.loc[m] = [date, 0]
        else:
            df_3.loc[m] = [date, score[m]]
        date += datetime.timedelta(hours=1)
    
    # Reseting title DataFrames
    df = pd.DataFrame(columns=['title'])
    df_1 = pd.DataFrame(columns=['title'])
    df_t = pd.DataFrame(columns=['timeStamp'])
    df_t_1 = pd.DataFrame(columns=['timeStamp'])
    df_t_2 = pd.DataFrame(columns=['timeStamp'])
    
    # Convert df_3 to a csv
    my_csv = pd.DataFrame({'Date': df_3.Date, 'Score': df_3.Score})
    # you could use any filename. We choose submission here
    #my_csv.to_csv('ReutersSentiment.csv', index=False)
    with open('ReutersSentiment_hour.csv', 'a') as f:
        my_csv.to_csv(f, header=False, index=False)

