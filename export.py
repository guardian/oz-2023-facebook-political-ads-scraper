#%%
import scraperwiki 
import pandas as pd

#%%
queryString = f"* from ads_by_id"
queryResult = scraperwiki.sqlite.select(queryString)
temp = pd.DataFrame(queryResult)
temp.to_csv('analysis/ads_by_id.csv', index=False)
#%%
# queryString = f"* from ads_by_query WHERE SCORE > 50 AND voice_ad_modelled='Not a Voice Ad'"
# queryResult = scraperwiki.sqlite.select(queryString)
# print(len(queryResult), "rows returned")
# temp = pd.DataFrame(queryResult)
# temp.to_excel('temp_ads_classify.xlsx', index=False)


queryString = f"* from ads_by_query WHERE score > 50"
queryResult = scraperwiki.sqlite.select(queryString)
print(len(queryResult), "rows returned")
temp = pd.DataFrame(queryResult)
temp.to_csv('analysis/ads_by_query.csv', index=False)

# queryString = f"* from ads_by_query WHERE score > 50 AND voice_ad_modelled='Is a Voice ad'"
# queryResult = scraperwiki.sqlite.select(queryString)
# print(len(queryResult), "rows returned")
# temp = pd.DataFrame(queryResult)
#%%


#%%
# temp2 = temp.drop_duplicates(subset=['ad_creative_bodies', 'page_name'])
# temp2.to_excel('analysis/voice_ads_unique.xlsx', index=False)
# temp.to_excel('temp_ads_classify2.xlsx', index=False)



# %%

# queryString = f"* from ads_by_query WHERE bylines is NULL AND instr(ad_creative_bodies, 'read') > 0"
# queryResult = scraperwiki.sqlite.select(queryString)
# temp = pd.DataFrame(queryResult)
# #%%
# unique = temp.drop_duplicates(subset=['page_name', 'ad_creative_bodies','ad_creative_link_captions'])
# unique.to_csv('weird-novels.csv', index=False)