import scraperwiki
import pandas as pd

# lastScraped = "2022-03-31"
queryString = f"* from ads_by_id"
queryResult = scraperwiki.sqlite.select(queryString)
temp = pd.DataFrame(queryResult)
temp.to_csv('temp.csv', index=False)

df = pd.read_csv('temp.csv')
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
pages = ['Yes23','Fair Australia','Not Enough','Senator Jacinta Nampijinpa Price','Referendum News','Linda Burney','The Uluru Statement from the Heart','Not My Voice']

sides = {
	'Yes23':"Yes",
	'The Uluru Statement from the Heart':"Yes",
	'Senator Jacinta Nampijinpa Price':'No',
	'Referendum News':'No',
	'Not My Voice':'No',
	'Fair Australia':'No',
	'Not Enough':'No'
	}

df = df[df['page_name'] != 'Linda Burney']

df['side'] = df['page_name'].map(sides)

impressions_page = df[['page_name', 'impressions_upper']].groupby(['page_name']).sum()

spend_page = df[['page_name', 'spend_lower', 'spend_upper']].groupby(['page_name']).sum()

spend_side = df[['page_name', 'spend_lower', 'spend_upper', 'side']].groupby(['side']).sum()

#%%

price = df[df['page_name'] == 'Senator Jacinta Nampijinpa Price']
price.to_csv("price.csv")

notenough = df[df['page_name'] == 'Not Enough']

#%%

age_df = df.copy()
age_df = age_df[['page_name','impressions_upper','young','middle','old', 'ad_creative_bodies', 'ad_snapshot_url']]
age_df['young_imp'] = age_df['young'] * age_df['impressions_upper']
age_df['middle_imp'] = age_df['middle'] * age_df['impressions_upper'] 
age_df['old_imp'] = age_df['old'] * age_df['impressions_upper'] 

age_imp = age_df[['page_name','young_imp','middle_imp','old_imp']]

age_group = age_imp.groupby(['page_name']).sum()

age_pct = age_group.copy()

age_pct = age_pct.div(age_pct.sum(axis=1), axis=0)
# age_pct = age_pct.round(2)
# age = df[['page_name','young','middle','old']].groupby(['page_name']).mean()

#%%

age_unique = age_df.copy()
age_unique['dupe'] = age_unique['ad_creative_bodies'].duplicated()
age_unique = age_unique[age_unique['dupe'] == False]


#%%

gender_df = df.copy()

gender_df = gender_df[['page_name','impressions_upper','male','female', 'ad_creative_bodies', 'ad_snapshot_url']]
gender_df['male_imp'] = gender_df['male'] * gender_df['impressions_upper']
gender_df['female_imp'] = gender_df['female'] * gender_df['impressions_upper'] 

gender_imp = gender_df[['page_name','male_imp','female_imp']]

gender_group = gender_imp.groupby(['page_name']).sum()

gender_pct = gender_group.copy()

gender_pct = gender_pct.div(gender_pct.sum(axis=1), axis=0)
gender_pct = gender_pct.round(2)

# gender = df[['page_name','male','female']].groupby(['page_name']).mean()

#%%

gender_unique = gender_df.copy()
gender_unique['dupe'] = gender_unique['ad_creative_bodies'].duplicated()
gender_unique = gender_unique[gender_unique['dupe'] == False]

#%%

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

state_tgt = state_tgt[['page_name','impressions_upper','Australian Capital Territory','New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Western Australia']]

state_tgt = state_tgt.dropna()

state_tgt.rename(columns=state_keyed, inplace=True)

for state in states_short:
	state_tgt[state + "_impressions"] = state_tgt[state] * state_tgt['impressions_upper']
	state_tgt[state + "_impressions_per_1000"] = (state_tgt[state + "_impressions"] / state_pop[state]) * 1000

state_tgt.to_csv("test.csv")

#%%

keep_cols = state_tgt.columns



#%%
keep_cols = [d for d in keep_cols if "_impressions" in d or "page_name" in d]
state_tgt_short = state_tgt[keep_cols]

state_grouped = state_tgt_short.groupby(['page_name']).sum()

state_grouped['total'] = state_grouped.sum(axis=1)

for state in states_short:
 	state_grouped[state + "_pct"] = state_grouped[state + "_impressions"] / state_grouped['total'] * 100

keep_cols2 = state_grouped.columns
keep_cols2 = [d for d in keep_cols2 if "_pct" in d or "page_name" in d]

state_final_raw = state_grouped[keep_cols2]
state_final_raw = state_final_raw.round(2)
state_final_raw = state_final_raw.T


#%%

keep_cols = state_tgt.columns

keep_cols = [d for d in keep_cols if "_impressions_per_1000" in d or "page_name" in d]

state_tgt_short = state_tgt[keep_cols]

state_grouped = state_tgt_short.groupby(['page_name']).sum()

state_grouped['total'] = state_grouped.sum(axis=1)

for state in states_short:
	state_grouped[state + "_pct"] = state_grouped[state + "_impressions_per_1000"] / state_grouped['total'] * 100

keep_cols2 = state_grouped.columns
keep_cols2 = [d for d in keep_cols2 if "_pct" in d or "page_name" in d]

state_final = state_grouped[keep_cols2]
state_final = state_final.round(2)
state_final = state_final.T
#%%

uluru = df[df['page_name'] == 'The Uluru Statement from the Heart']

#%%

from datetime import datetime
import numpy as np

def makeTimeSeries(group):
	ad_time = df.copy()
	ad_time = ad_time[(ad_time['side'] == group)]
	ad_time.loc[ pd.isna(ad_time['ad_delivery_stop_time']), 'ad_delivery_stop_time'] = datetime.now()
	ad_time['ad_delivery_start_time'] = pd.to_datetime(ad_time['ad_delivery_start_time'], format="%Y-%m-%d")
	ad_time['ad_delivery_stop_time'] = pd.to_datetime(ad_time['ad_delivery_stop_time'], format="%Y-%m-%d")
	ad_time['total_days'] = (ad_time['ad_delivery_stop_time'] - ad_time['ad_delivery_start_time']).dt.days
	
	ad_time['spend_day'] = ((ad_time['spend_lower'] + ad_time['spend_upper']) / 2) / ad_time['total_days']
	ad_time.loc[ ad_time['spend_day'] == np.inf, 'spend_day'] = ((ad_time['spend_lower'] + ad_time['spend_upper']) / 2)
	
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

yes_timeseries = makeTimeSeries("Yes")
no_timeseries = makeTimeSeries("No")


#%%
yes_timeseries = yes_timeseries.rename(columns={"total":"Yes"})
no_timeseries = no_timeseries.rename(columns={"total":"No"})
chart_data = pd.concat([yes_timeseries, no_timeseries], axis=1)

chart_data = chart_data.reset_index()
chart_data = chart_data.rename(columns={"index":"Date"})
chart_data = chart_data[chart_data['Date'] >= "2023-01-01"]
chart_data['Date'] = chart_data['Date'].dt.strftime("%Y-%m-%d")

#%%

from yachtcharter import yachtCharter

def makeChart(chart_df):
	
	template = [
			{
				"title": "Yes and no campaign Facebook ad spend over time",
				"subtitle": "Showing the estimated ad spend per day for the yes* and no* campaigns on Facebook. Facebook publishes ad spend as a range with an upper and lower value. This chart uses the midpoint between these two values, averaged over the number of days the ad ran for",
				"footnote": "",
				"source": "Guardian Australia analysis of Meta ad library. *Yes campaign pages include: Yes23, Uluru Statement from the Heart. No campaign pages include: Fair Australia, Not Enough, Not My Voice, Referendum News and Senator Jacinta Nampijinpa Price",
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
				"xAxisDateFormat": "%b %d"
			}
		]
	key = []
	# periods = [{"label":"Data change", "start":"2021-08-16","end":"","textAnchor":"start"}]
	labels = []
	options = [{"lineLabelling":"TRUE"}]
	chartId = [{"type":"linechart"}]
# 	df.fillna('', inplace=True)
	chartData = chart_df.to_dict('records')

	yachtCharter(template=template,options=options, data=chartData, chartId=chartId, chartName="2023-voice-ad-spending")
	
makeChart(chart_data)	







