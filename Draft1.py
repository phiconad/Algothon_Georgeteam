#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 14:11:42 2018

@author: andreademarco
"""

import pandas as pd
import numpy as np

path = "mystery_symbol_train.csv"

data = pd.read_csv(path)

data_trail = data.head()
