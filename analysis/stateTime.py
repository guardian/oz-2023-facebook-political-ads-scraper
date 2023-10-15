#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import numpy as np

from yachtcharter import yachtCharter

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

states = ['Australian Capital Territory','New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Western Australia']

states_short = ['ACT','NSW','NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
states_excl = ['NSW','QLD', 'SA', 'TAS', 'VIC', 'WA']

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

df.rename(columns=state_keyed, inplace=True)

#%%

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

#%%
def makeTimeSeries(group, state):
	ad_time = df.copy()
	ad_time = ad_time[(ad_time['side'] == group)]
	ad_time.loc[ pd.isna(ad_time['ad_delivery_stop_time']), 'ad_delivery_stop_time'] = datetime.now()
	ad_time['ad_delivery_start_time'] = pd.to_datetime(ad_time['ad_delivery_start_time'], format="%Y-%m-%d")
	ad_time['ad_delivery_stop_time'] = pd.to_datetime(ad_time['ad_delivery_stop_time'], format="%Y-%m-%d")
	ad_time['total_days'] = (ad_time['ad_delivery_stop_time'] - ad_time['ad_delivery_start_time']).dt.days
	
	ad_time['spend_day'] = ((ad_time['spend_lower'] + ad_time['spend_upper']) / 2) / ad_time['total_days']
	ad_time.loc[ ad_time['spend_day'] == np.inf, 'spend_day'] = ((ad_time['spend_lower'] + ad_time['spend_upper']) / 2)
	
	if state:
		ad_time['spend_day'] = ad_time['spend_day'] * ad_time[state]
	ad_time_short = ad_time[['ad_id', 'ad_delivery_start_time', 'ad_delivery_stop_time', 'total_days', 'spend_day']]
	
	dt_index = pd.date_range(start='2023-01-01', end='2023-07-24')
	timeseries = pd.DataFrame(index=dt_index)
	
	for row in ad_time_short.itertuples():
		print(row.ad_delivery_start_time)
		temp_index = pd.date_range(start=row.ad_delivery_start_time, end=row.ad_delivery_stop_time)
		temp_df = pd.DataFrame(index=temp_index)
		temp_df[row.ad_id] = row.spend_day
		timeseries = pd.concat([timeseries, temp_df], axis=1)
	
	timeseries['total'] = timeseries.sum(axis=1)	
	timeseries_final = timeseries[['total']]
	return timeseries_final

# yes_timeseries = makeTimeSeries("Yes")


#%%


state_dfs_no = []
for state in states_excl:
	print(state)
	temp_state_df = makeTimeSeries("No", state)
	temp_state_df['total'] = (temp_state_df['total'] / state_pop[state]) * 1000
	temp_state_df = temp_state_df.rename(columns={"total":state})
	state_dfs_no.append(temp_state_df)

#%%
	
state_dfs_yes = []
for state in states_excl:
	print(state)
	temp_state_df = makeTimeSeries("Yes", state)
	temp_state_df['total'] = (temp_state_df['total'] / state_pop[state]) * 1000
	temp_state_df = temp_state_df.rename(columns={"total":state})
	state_dfs_yes.append(temp_state_df)	
	
# no_timeseries_all = makeTimeSeries("No", None)
# no_timeseries_sa = makeTimeSeries("No", 'South Australia')

# yes_timeseries_all = makeTimeSeries("Yes", None)
# yes_timeseries_sa = makeTimeSeries("Yes", 'South Australia')


#%%
# no_timeseries_all = no_timeseries_all.rename(columns={"total":"No all"})
# no_timeseries_sa = no_timeseries_sa.rename(columns={"total":"No SA"})

# yes_timeseries_all = yes_timeseries_all.rename(columns={"total":"Yes all"})
# yes_timeseries_sa = yes_timeseries_sa.rename(columns={"total":"Yes SA"})

chart_data_no = pd.concat(state_dfs_no, axis=1)

chart_data_no = chart_data_no.reset_index()
chart_data_no = chart_data_no.rename(columns={"index":"Date"})
chart_data_no = chart_data_no[chart_data_no['Date'] >= "2023-01-01"]

chart_data_no_month = chart_data_no.groupby(pd.Grouper(key='Date',freq='MS')).sum()
chart_data_no_month = chart_data_no_month.reset_index()
chart_data_no_month['Date'] = chart_data_no_month['Date'].dt.strftime("%Y-%m-%d")

chart_data_no['Date'] = chart_data_no['Date'].dt.strftime("%Y-%m-%d")


#%%
chart_data_yes = pd.concat(state_dfs_yes, axis=1)

chart_data_yes = chart_data_yes.reset_index()
chart_data_yes = chart_data_yes.rename(columns={"index":"Date"})
chart_data_yes = chart_data_yes[chart_data_yes['Date'] >= "2023-01-01"]

chart_data_yes_month = chart_data_yes.groupby(pd.Grouper(key='Date',freq='MS')).sum()
chart_data_yes_month = chart_data_yes_month.reset_index()
chart_data_yes_month['Date'] = chart_data_yes_month['Date'].dt.strftime("%Y-%m-%d")

chart_data_yes['Date'] = chart_data_yes['Date'].dt.strftime("%Y-%m-%d")

#%%

def makeChart(chart_df):
	
	template = [
			{
				"title": "No campaign Facebook ad spend by state, adjusted for population",
				"subtitle": "Showing the estimated ad spend per month for the no campaign* on Facebook. Facebook publishes ad spend as a range with an upper and lower value. This chart uses the midpoint between these two values, averaged over the number of days the ad ran for, which was then totalled by month and adjusted by the population of each state to get a dollar value per month, per 1000 people",
				"footnote": "",
				"source": "Guardian Australia analysis of Meta ad library. *No campaign pages include: Fair Australia, Not Enough, Not My Voice, Referendum News, Save Aus Day - VOTE NO and Senator Jacinta Nampijinpa Price",
				"dateFormat": "%Y-%m-%d",
				"xAxisLabel": "",
				"yAxisLabel": "",
				# "tooltip":"<strong>Date: </strong>{{#nicedate}}Date{{/nicedate}}<br/><strong>Count: </strong>{{State or territory}}",
				"periodDateFormat":"",
				"margin-left": "35",
				"margin-top": "25",
				"margin-bottom": "22",
				"margin-right": "22",
				"xAxisDateFormat": "%b"
			}
		]
	key = []
	# periods = [{"label":"Data change", "start":"2021-08-16","end":"","textAnchor":"start"}]
	labels = []
	options = [{"lineLabelling":"TRUE"}]
	chartId = [{"type":"linechart"}]
# 	df.fillna('', inplace=True)
	chartData = chart_df.to_dict('records')

	yachtCharter(template=template,options=options, data=chartData, chartId=chartId, chartName="2023-voice-ad-spending-no-campaign-pop-adjusted-month")
	
makeChart(chart_data_no_month)	


#%%

def makeChart(chart_df):
	
	template = [
			{
				"title": "Yes campaign Facebook ad spend by state, adjusted for population",
				"subtitle": "Showing the estimated ad spend per month for the yes campaign* on Facebook. Facebook publishes ad spend as a range with an upper and lower value. This chart uses the midpoint between these two values, averaged over the number of days the ad ran for, which was then totalled by month and adjusted by the population of each state to get a dollar value per month, per 1000 people",
				"footnote": "",
				"source": "Guardian Australia analysis of Meta ad library. *Yes campaign pages include: Yes23, Uluru Statement from the Heart",
				"dateFormat": "%Y-%m-%d",
				"xAxisLabel": "",
				"yAxisLabel": "",
				"timeInterval":"day",
				# "tooltip":"<strong>Date: </strong>{{#nicedate}}Date{{/nicedate}}<br/><strong>Count: </strong>{{State or territory}}",
				"periodDateFormat":"",
				"margin-left": "35",
				"margin-top": "25",
				"margin-bottom": "22",
				"margin-right": "22",
				"xAxisDateFormat": "%b"
			}
		]
	key = []
	# periods = [{"label":"Data change", "start":"2021-08-16","end":"","textAnchor":"start"}]
	labels = []
	options = [{"lineLabelling":"TRUE"}]
	chartId = [{"type":"linechart"}]
# 	df.fillna('', inplace=True)
	chartData = chart_df.to_dict('records')

	yachtCharter(template=template,options=options, data=chartData, chartId=chartId, chartName="2023-voice-ad-spending-yes-campaign-pop-adjusted-month")
	
makeChart(chart_data_yes_month)	


#%%


