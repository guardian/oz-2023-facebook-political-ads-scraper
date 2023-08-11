import sqlite3
def vaccuum():
	con = sqlite3.connect("scraperwiki.sqlite")
	con.execute("VACUUM")
	con.close()

vaccuum() 

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
	queryString = "* from ads_by_query"
	queryResult = scraperwiki.sqlite.select(queryString)
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
