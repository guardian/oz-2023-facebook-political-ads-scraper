#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import scraperwiki
import pandas as pd

# lastScraped = "2022-03-31"
# queryString = f"* from ads_by_id"
# queryResult = scraperwiki.sqlite.select(queryString)
# temp = pd.DataFrame(queryResult)
# temp.to_csv('temp.csv', index=False)

df = pd.read_csv('ads_by_id.csv')
df['count'] = 1

df['page_name'].replace(to_replace="From the Heart", value="Yes23", inplace=True) 
# df = df[df['page_name'] != 'The Uluru Statement from the Heart']

print(df.columns)

cols = ['ad_id', 'page_id', 'page_name', 'ad_creative_bodies',
       'ad_delivery_start_time', 'bylines', 'ad_snapshot_url',
       'estimated_audience_size_lower', 'male', 'female', 'young', 'middle',
       'old', 'delivery_by_region', 'estimated_audience_size_upper',
       'ad_delivery_stop_time', 'currency', 'spend_lower', 'spend_upper',
       'impressions_lower', 'impressions_upper',
       'Australian Capital Territory', 'New South Wales', 'Northern Territory',
       'Queensland', 'South Australia', 'Tasmania', 'Victoria',
       'Western Australia', 'count']

print(df['page_name'].unique())
pages = ['Yes23','Fair Australia','Not Enough','Senator Jacinta Nampijinpa Price','Referendum News','Linda Burney','The Uluru Statement from the Heart','Not My Voice', 'Save Aus Day - VOTE NO']

sides = {
	'Yes23':"Yes",
	'The Uluru Statement from the Heart':"Yes",
	'Senator Jacinta Nampijinpa Price':'No',
	'Referendum News':'No',
	'Not My Voice':'No',
	'Fair Australia':'No',
	'Not Enough':'No',
	'Save Aus Day - VOTE NO':'No'
	}

df = df[df['page_name'] != 'Linda Burney']

df['side'] = df['page_name'].map(sides)

df = df[df['ad_delivery_start_time'] >= '2023-08-01']


states = ['Australian Capital Territory','New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Western Australia']

states_short = ['ACT','NSW','NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

state_keyed = {
		'Australian Capital Territory':'ACT',
		'New South Wales':'NSW',
		'Northern Territory':'NT',
		'Queensland':'QLD',
		'South Australia':'SA',
		'Tasmania':'TAS',
		'Victoria':'VIC',
		'Western Australia':'WA'
	}


state_pop = {
  "NSW": 8238800,
  "VIC": 6704300,
  "QLD": 5378300,
  "SA": 1834300,
  "WA": 2825200,
  "TAS": 571600,
  "NT": 250100,
  "ACT": 460900
}

state_tgt = df.copy()

state_tgt = state_tgt[['side','spend_upper','Australian Capital Territory','New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Western Australia']]

state_tgt = state_tgt.dropna()

state_tgt.rename(columns=state_keyed, inplace=True)

for state in states_short:
	state_tgt[state + "_spend"] = state_tgt[state] * state_tgt['spend_upper']
	state_tgt[state + "_per_1000"] = (state_tgt[state + "_spend"] / state_pop[state]) * 1000

state_tgt.to_csv("test.csv")



keep_cols = state_tgt.columns

#%%
keep_cols = [d for d in keep_cols if "_spend" in d or "side" in d]

state_tgt_short = state_tgt[keep_cols]

state_grouped = state_tgt_short.groupby(['side']).sum()

state_grouped['total'] = state_grouped.sum(axis=1)

keep_cols2 = state_grouped.columns
keep_cols2 = [d for d in keep_cols2 if"_spend" in d or "side" in d]

state_final_raw = state_grouped[keep_cols2]
state_final_raw = state_final_raw.round(2)
state_final_raw = state_final_raw.T
#%%

keep_cols = [d for d in keep_cols if "_per_1000" in d or "side" in d]

state_tgt_short = state_tgt[keep_cols]

state_grouped = state_tgt_short.groupby(['side']).sum()

state_grouped['total'] = state_grouped.sum(axis=1)

keep_cols2 = state_grouped.columns
keep_cols2 = [d for d in keep_cols2 if "_per_1000" in d or "side" in d]

state_final = state_grouped[keep_cols2]
state_final = state_final.round(2)
state_final = state_final.T