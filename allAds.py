#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('ads_by_query.csv')
pollies = pd.read_csv('politicians.csv')
pollies = pollies.set_index('page_id')
pollies_dict = pollies.to_dict(orient='index')


#%%

df['politician'] = df.map()