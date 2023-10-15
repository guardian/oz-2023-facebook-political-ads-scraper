#%%
import sqlite3
def vaccuum():
	con = sqlite3.connect("scraperwiki.sqlite")
	con.execute("VACUUM")
	con.close()

# vaccuum() 

def drop_table():
	con = sqlite3.connect("scraperwiki.sqlite")
	con.execute("DROP TABLE ads_by_query")
	con.close()

# drop_table()
#%%
import scraperwiki
import time

def fixadURLS():
	queryString = "* from ads_by_query"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		print(row['ad_id'])
		row['ad_snapshot_url'] = f"https://www.facebook.com/ads/library/?id={row['ad_id']}"
		scraperwiki.sqlite.save(unique_keys=["ad_id"], data=row, table_name="ads_by_query")
		time.sleep(0.1)

# fixadURLS()
#%%

import ast
import scraperwiki
def concatText():
	queryString = "* from ads_by_query WHERE concat_text is NULL"
	queryResult = scraperwiki.sqlite.select(queryString)
	print(len(queryResult), "rows")
	for row in queryResult:
		
		print(row['ad_id'])
		# print(row['ad_creative_link_titles'])
		concat_text = []
		if row['ad_creative_bodies']:
			concat_text.append(row['ad_creative_bodies'])
		if row['ad_creative_link_titles']:
			ad_titles = ast.literal_eval(row['ad_creative_link_titles'])
			concat_text.extend(ad_titles)
		if row['ad_creative_link_captions']:	
			ad_captions= ast.literal_eval(row['ad_creative_link_captions'])
			concat_text.extend(ad_captions)
		if row['ad_creative_link_descriptions']:
			ad_descriptions = ast.literal_eval(row['ad_creative_link_descriptions'])
			concat_text.extend(ad_descriptions)
		if concat_text:
			row['concat_text'] = " ".join(concat_text)
			print(row['concat_text'])
			scraperwiki.sqlite.save(unique_keys=["ad_id"], data=row, table_name="ads_by_query")
			time.sleep(0.1)

concatText()


#%%

def corrections():
	checked = pd.read_excel('temp_ads_classify-24_08_2023.xlsx')
	checked_list = list(checked['ad_id'])
	checked = checked.set_index('ad_id')
	checked_dict = checked.to_dict(orient='index')
	
	import time
	queryString = "* from ads_by_query"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		if int(row['ad_id']) in checked_list:
			print(row['ad_id'])
			row['score'] = checked_dict[int(row['ad_id'])]['score']
			scraperwiki.sqlite.save(unique_keys=["ad_id"], data=row, table_name="ads_by_query")
			time.sleep(0.1)

# corrections()		


#%%

# blah = pd.read_excel('temp_ads_classify-24_08_2023.xlsx')

# k = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

# def stripChars(row):
# 	print(row['ad_creative_bodies'])
# 	if not pd.isnull(row['ad_creative_bodies']):
# 		print("yeh")
# 		getVals = list(filter(lambda x: x in k, row['ad_creative_bodies']))
# 		result = "".join(getVals).lower()
# 		return(result.strip().lower())
# 	else:
# 		return row['ad_creative_bodies']

# blah['cleaned_ad'] = blah.apply(stripChars, axis=1)

# blah = blah.drop_duplicates(subset=['ad_creative_bodies', 'page_name'])
# blah.to_excel('blah.xlsx')


