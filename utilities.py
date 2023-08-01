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