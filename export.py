#%%
import scraperwiki 
import pandas as pd
queryString = f"* from ads_by_id"
queryResult = scraperwiki.sqlite.select(queryString)
temp = pd.DataFrame(queryResult)
temp.to_csv('analysis/ads_by_id.csv', index=False)

queryString = f"* from ads_by_query"
queryResult = scraperwiki.sqlite.select(queryString)
temp = pd.DataFrame(queryResult)
temp.to_csv('analysis/ads_by_query.csv', index=False)
# %%
