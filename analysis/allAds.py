#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
import pandas as pd

tagged = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTACLNmVRNPXzaNpMohWwwQwRM9VEDgCPJRHMAL2yLaZnLRApPfGpBFbJOj7Mmsow0s3yBKxsOk5OoC/pub?output=xlsx', sheet_name='tagged')

#%%

ads = pd.read_csv('ads_by_query.csv')
k = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

def stripChars(row):
	print(row['ad_creative_bodies'])
	if not pd.isnull(row['ad_creative_bodies']):
		print("yeh")
		getVals = list(filter(lambda x: x in k, row['ad_creative_bodies']))
		result = "".join(getVals).lower()
		return(result.strip().lower())
	else:
		return row['ad_creative_bodies']

ads['cleaned_ad'] = ads.apply(stripChars, axis=1)

tagged['cleaned_ad'] = tagged.apply(stripChars, axis=1)

#%%

copy = tagged.copy()

copy['dupes'] = copy.duplicated(subset='cleaned_ad')

#%%
copy = copy[copy['dupes'] != True]

copy = copy.set_index('cleaned_ad')
#%%
tagged_dict = copy.to_dict(orient='index')

cantFind = []
def returnVoice(row):
	if row['cleaned_ad'] in tagged_dict:
		result = tagged_dict[row['cleaned_ad']]
		print(result['voice_ad'])
		return result['voice_ad']
	else:
		cantFind.append(row['cleaned_ad'])
		return None
	
def returnSide(row):
	if row['cleaned_ad'] in tagged_dict:
		result = tagged_dict[row['cleaned_ad']]
		print(result['side'])
		return result['side']
	else:
		cantFind.append(row['cleaned_ad'])
		return None
	

ads['voice_ad'] = ads.apply(returnVoice, axis=1)

ads['side'] = ads.apply(returnSide, axis=1)


#%%
ads = ads.drop_duplicates(subset='concat_text')
ads.to_csv('training-ads.csv', index=False, encoding="utf-8")

#%%

voice_ads = ads[ads['voice_ad'] == 1]
voice_ads['count'] = 1

side_gp = voice_ads[['count', 'side', 'spend_upper']].groupby(['side']).sum()

#%%

page_gp = voice_ads[['count', 'side','page_name', 'spend_upper']].groupby(['page_name', 'side']).sum()

#%%




