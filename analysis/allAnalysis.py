#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('ads_by_query.csv')

#%%

# Add in manual corrections from tagged ad data

# Make ad copy into only alphanumeric chars

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

df['cleaned_ad'] = df.apply(stripChars, axis=1)

#%%

# Get tagged ad data

tagged = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRfYVhzyOYEt2Oz4tO1Kp5cIeuok7bPOOilKBzTOi6Rc_2WXTBLgNeIR1Kcq9XDFIJD1UNnRLpShkDv/pub?output=xlsx', sheet_name='ads')
tagged = tagged.dropna(subset=['cleaned_ad'])
tagged = tagged.drop_duplicates(subset=['cleaned_ad'])
tagged = tagged.set_index('cleaned_ad')
tagged_dict = tagged.to_dict(orient='index')

#%%

# Match tagged data to database output

cantFind = []

def returnVoice(row):
	if row['cleaned_ad'] in tagged_dict:
		result = tagged_dict[row['cleaned_ad']]
		print(result['voice_ad_tag'])
		return result['voice_ad_tag']
	else:
		cantFind.append(row['ad_id'])
		return None

df['voice_ad_tag'] = df.apply(returnVoice, axis=1)


#%%
# Remove ads that aren't voice ads

df = df[df['voice_ad_tag'] != 0]

#%%

# Add sides from tagged data


sides = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRfYVhzyOYEt2Oz4tO1Kp5cIeuok7bPOOilKBzTOi6Rc_2WXTBLgNeIR1Kcq9XDFIJD1UNnRLpShkDv/pub?output=xlsx', sheet_name='sides')
sides = sides.set_index('page_id')
sides_dict = sides.to_dict(orient='index')

#%%
cantFindSides = []
def returnSide(row):
	if row['page_id'] in sides_dict:
		result = sides_dict[row['page_id']]
		print(result['side_inferred'])
		return result['side_inferred']
	else:
		cantFindSides.append(row['ad_id'])
		return None

df['side_inferred'] = df.apply(returnSide, axis=1)


#%%

# Add info about politicians

pollies = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRfYVhzyOYEt2Oz4tO1Kp5cIeuok7bPOOilKBzTOi6Rc_2WXTBLgNeIR1Kcq9XDFIJD1UNnRLpShkDv/pub?output=xlsx', sheet_name='politicians')
pollies = pollies.set_index('page_id')
pollies_dict = pollies.to_dict(orient='index')

#%%


def govLevel(row):
	if row['page_id'] in pollies_dict:
		return pollies_dict[row['page_id']]['gov_level']
	else:
		return None
	
	
df['gov_level'] = df.apply(govLevel, axis=1)

#%%

def addParty(row):
	if row['page_id'] in pollies_dict:
		return pollies_dict[row['page_id']]['party_group']
	else:
		return None

df['party_group'] = df.apply(addParty, axis=1)
#%%
df.to_excel('voice-ads.xlsx')
# check = df[df['page_name'] == "Senator Jacinta Nampijinpa Price"]
# check2 = pollies[pollies['page_id'] == 1622506634677043]
#%%

pol_df = df[pd.notnull(df['party_group'])]

feds = pol_df[pol_df['gov_level'] == 'Federal']

fed_spend = feds[['party_group', 'spend_lower', 'spend_upper']].groupby(['party_group']).sum()

fed_spend_side = feds[['party_group', 'side_inferred', 'spend_lower', 'spend_upper']].groupby(['party_group', 'side_inferred']).sum()

fed_spend.sort_values('spend_upper', ascending=False, inplace=True)

pol_spend = pol_df[['page_name','party_group', 'spend_lower', 'spend_upper', 'side_inferred']].groupby(['page_name','party_group', 'side_inferred']).sum()

pol_spend.sort_values('spend_upper', ascending=False, inplace=True)

pol_side_spend = feds[['side_inferred', 'spend_lower', 'spend_upper']].groupby(['side_inferred']).sum()

pol_side_spend.sort_values('spend_upper', ascending=False, inplace=True)

#%%

print(list(df.columns))

cols = ['ad_id', 'page_id', 'query', 'page_name', 'ad_creative_bodies', 'ad_delivery_start_time', 'bylines', 'currency', 'spend_lower', 'spend_upper', 'impressions_lower', 'impressions_upper', 'ad_snapshot_url', 'male', 'female', 'young', 'middle', 'old', 'delivery_by_region', 'Australian Capital Territory', 'New South Wales', 'Northern Territory', 'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia', 'ad_creative_link_captions', 'ad_creative_link_titles', 'ad_delivery_stop_time', 'ad_creative_link_descriptions', 'concat_text', 'score', 'side_inferred', 'voice_ad_modelled', 'cleaned_ad', 'voice_ad_tag', 'side_inferred2', 'gov_level', 'party']
#%%
side_spend = df[['side_inferred', 'spend_lower', 'spend_upper']].groupby(['side_inferred']).sum()
side_spend.sort_values('spend_upper', ascending=False, inplace=True)

all_spend = df[['page_name', 'spend_lower', 'spend_upper', 'side_inferred']].groupby(['page_name', 'side_inferred']).sum()
all_spend.sort_values('spend_upper', ascending=False, inplace=True)

with pd.ExcelWriter("spending-results.xlsx") as writer:
	pol_spend.to_excel(writer, sheet_name="politician_spend") 
	pol_side_spend.to_excel(writer, sheet_name="politician_spend_side")
	fed_spend.to_excel(writer, sheet_name="party_spend")
	side_spend.to_excel(writer, sheet_name="side_spend")
	all_spend.to_excel(writer, sheet_name="all_spend")

