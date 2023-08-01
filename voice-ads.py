import requests
import scraperwiki
from datetime import datetime
from datetime import timedelta
import json
import time
import os
import pandas as pd

key = os.environ['fb_ad_token']

delay = 18.5

#%%
dateScraped = datetime.strftime(datetime.now(), '%Y-%m-%d')

queryCount = 0

def getDemos(jsonBlob):
	temp = pd.DataFrame(jsonBlob)
	temp['percentage'] = pd.to_numeric(temp['percentage'])
	gender = temp.groupby(['gender']).sum()
	male = 0
	if 'male' in gender.index:
		male = gender.loc['male'][0]
	female = 0
	if 'female' in gender.index:
		female = gender.loc['female'][0]
	age = temp.groupby(['age']).sum()
	young_keys = ['13-17','18-24','25-34']
	young = 0
	for young_key in young_keys:
		if young_key in age.index:
			young = young + age.loc[young_key][0]
	
	middle = 0
	middle_keys = ['35-44','45-54','55-64']
	for middle_key in middle_keys:
		if middle_key in age.index:
			middle = middle + age.loc[middle_key][0]
	
	old = 0
	if '65+' in age.index:		
		old = age.loc['65+'][0] 
	return {"male": male, "female":female,"young":young,"middle":middle,"old":old}

#%%

test_states1 = [{'percentage': '0.033134', 'region': 'Australian Capital Territory'}, {'percentage': '0.273881', 'region': 'New South Wales'}, {'percentage': '0.014328', 'region': 'Northern Territory'}, {'percentage': '0.131791', 'region': 'Queensland'}, {'percentage': '0.078507', 'region': 'South Australia'}, {'percentage': '0.015075', 'region': 'Tasmania'}, {'percentage': '0.25791', 'region': 'Victoria'}, {'percentage': '0.195373', 'region': 'Western Australia'}]

test_states2 =  [
            {
               "percentage": "1",
               "region": "South Australia"
            }
         ]

state_template = [
	{'percentage': '0', 'region': 'Australian Capital Territory'},
	{'percentage': '0', 'region': 'New South Wales'},
	{'percentage': '0', 'region': 'Northern Territory'},
	{'percentage': '0', 'region': 'Queensland'},
	{'percentage': '0', 'region': 'South Australia'},
	{'percentage': '0', 'region': 'Tasmania'},
	{'percentage': '0', 'region': 'Victoria'},
	{'percentage': '0', 'region': 'Western Australia'}
	]

states = ['Australian Capital Territory','New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Western Australia']

def mergeStates(state_list):
	result = []
	for row in state_template:
		match = [d for d in state_list if d.get('region') == row['region']]
		if match:
			result.append(match[0])
		else:
			result.append(row)
	return result		

def dictiFy(state_list):
	result = {}
	for row in state_list:
		result[row['region']] = row['percentage']
	return result	

# merged = mergeStates(test_states1)
# blah = dictiFy(merged)
# print(blah)
		
#%%

def savePosts(resultsJson, query):
	for result in resultsJson['data']:
# 		print(result)
		
		data = {}
		
		data['ad_id'] = result['id']
		data['page_id'] = result['page_id']
		data['query'] = query
		data['page_name'] = result['page_name']

		if 'ad_creative_bodies' in result:
			data['ad_creative_bodies'] = ' '.join(result['ad_creative_bodies'])

		if 'ad_creative_link_captions' in result:
			data['ad_creative_link_captions'] = str(result['ad_creative_link_captions'])

		if 'ad_creative_link_descriptions' in result:
			data['ad_creative_link_descriptions'] = str(result['ad_creative_link_descriptions'])

		if 'ad_creative_link_titles' in result:
			data['ad_creative_link_titles'] = str(result['ad_creative_link_titles'])

		if 'ad_delivery_start_time' in result:
			data['ad_delivery_start_time'] = result['ad_delivery_start_time']
		
		if 'ad_delivery_stop_time' in result:
			data['ad_delivery_stop_time'] = result['ad_delivery_stop_time']

		if 'bylines' in result:
			data['bylines'] = result['bylines']
		
		if 'currency' in result:	
			data['currency'] = result['currency']
		if 'spend' in result:
			data['spend_lower'] = result['spend']['lower_bound']
			data['spend_upper'] = result['spend']['upper_bound']
		if 'impressions' in result:
			if 'lower_bound' in result['impressions']:
				data['impressions_lower'] = result['impressions']['lower_bound']
			if 'upper_bound' in result['impressions']: 	
				data['impressions_upper'] = result['impressions']['upper_bound']

		data['ad_snapshot_url'] = f"https://www.facebook.com/ads/library/?id={result['id']}"
	
		if 'demographic_distribution' in result:
			demos = getDemos(result['demographic_distribution'])
			data['male'] = demos['male']
			data['female'] = demos['female']
			data['young'] = demos['young']
			data['middle'] = demos['middle']
			data['old'] = demos['old']

		if 'delivery_by_region' in result:
			data['delivery_by_region'] = str(result['delivery_by_region'])
			merged = mergeStates(result['delivery_by_region'])
			keyed = dictiFy(merged)
			for state in states:
				data[state] = keyed[state]

		if 'estimated_audience_size' in result:
			if 'lower_bound' in result['estimated_audience_size']:
				data['estimated_audience_size_lower'] = result['estimated_audience_size']['lower_bound']
			if 'upper_bound' in result['estimated_audience_size']:
				data['estimated_audience_size_upper'] = result['estimated_audience_size']['upper_bound']

		print(data)	

		scraperwiki.sqlite.save(unique_keys=["ad_id"], data=data, table_name='ads_by_query')
	
		time.sleep(0.2)

def getPosts(query,since):
	print(f"Getting ads related to {query}")

	url = f"https://graph.facebook.com/v17.0/ads_archive?access_token={key}&fields=id,page_id,page_name,ad_creative_bodies,ad_creative_link_captions,ad_creative_link_descriptions,ad_creative_link_titles,ad_delivery_start_time,ad_delivery_stop_time,bylines,demographic_distribution,spend,currency,delivery_by_region,impressions,ad_snapshot_url&aad_type=POLITICAL_AND_ISSUE_ADS&ad_reached_countries=[%27AU%27]&limit=200&ad_delivery_date_min={since}&search_terms='{query}'"

	print(url)
	global queryCount
	queryCount += 1
	results = requests.get(url)
	resultsJson = results.json()
	# handle errors
	
	if 'error' in resultsJson:
		
		print(resultsJson['error'])
	
	# no errors, so save data from first page of results
	
	else:
		# print resultsJson
		# save the data
		savePosts(resultsJson, query)
		# Space out API calls to avoid rate limit
		
		print("Waiting...")
		time.sleep(delay)	
	# check if more pages
	
		if len(resultsJson['data']) > 0:
			
			while 'paging' in resultsJson:
			
				print("Next page:", resultsJson['paging']['next'])
				results = requests.get(resultsJson['paging']['next'])
				queryCount += 1
				resultsJson = results.json()
				# print resultsJson
				
				savePosts(resultsJson, query)
				
				# Space out API calls to avoid rate limit
				print("Waiting...")
				time.sleep(delay)

#%%

upto = 0
initialSinceDate = "2023-01-01"

# 331204223675563 - United Australia Party
# 316480331783930 - Australian Unions

# 292602604891 - Josh Frydenberg

queries = ["the voice"]

for query in queries:
	getPosts(query, initialSinceDate)

