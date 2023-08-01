#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scraperwiki
import pandas as pd
import re
# lastScraped = "2022-03-31"
queryString = f"* from ads_by_query"
queryResult = scraperwiki.sqlite.select(queryString)
temp = pd.DataFrame(queryResult)
temp.to_csv('temp-query.csv', index=False)

df = pd.read_csv('temp-query.csv')
df['count'] = 1

checkWords = ['parliament', 'canberra', 'constitution', 'canberra voice', 'indigenous', 'aboriginal', 'albanese', "albanese's"]

def contains_word(s, word_list):
    for word in word_list:
        if re.search(f'\b{word}\b', s):
            return True
    return False


#%%

contains_word("the voice to parliament", checkWords)

#%%
def checkVoiceAds(row):
	print(row['ad_creative_bodies'])
	check = contains_word(row['ad_creative_bodies'], checkWords)
	return check

df['voice_ad'] = df.apply(checkVoiceAds, axis=1)