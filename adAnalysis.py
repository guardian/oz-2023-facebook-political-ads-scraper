#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scraperwiki
import pandas as pd
import re
# lastScraped = "2022-03-31"
# queryString = f"* from ads_by_query"
# queryResult = scraperwiki.sqlite.select(queryString)
# temp = pd.DataFrame(queryResult)
# temp.to_csv('temp-query.csv', index=False)

# df = pd.read_csv('temp-query.csv')
# df['count'] = 1

# word stems to score presence of

checkWords = ['parliament', 
              'canberra', 
              'constitution', 
              'indigenous',
              'aborigin',
              'albanese',
              'albo',
              'referendum',
              'treaty',
              'recognition',
              'yes23',
              'thomas mayo', # supports yes, but in no attack ads
              'mayo',
              'teela reid', # supports yes, but in no attack ads
              'reid',
              'labor',
              'first nations',
              'voice'
              'voteno',
              'voteyes',
              'noel pearson',
              'jacinta', # no, jacinta price
              'jacinta price', # no
              'mundine', # no, warren mundine
              'warren mundine', # no
              "Kerry O'Brien", # yes
              'Shireen Morris', # yes
              'Linda Burney', # yes
              'tom calma', # yes
              'Marcus Stewart', # yes
              'Eddie Synot', # yes
              'Megan Davis', # yes 
              'racist',
              'uluru'
              ]



fromPages = ['102329728050606', # yes23
             '104180525925926', # fair australia
             '117806591312470', # not enough
             '1622506634677043', # Senator Jacinta Nampijinpa Price
             '113998151684022', # referendum news
             '363375540400009', #linda burney
             '102292348146435', # The Uluru Statement from the Heart
             '103072892843066', # not my voice
             '112239124719864', # gen united
             '109657605474040', # multicultural voices against the voice
             '131283957610666', # AJA
             '117058357932949', # constitutional equality
             '1407150000000000', # empowered communities
             '102330000000000' # From the heart
             ]

# News and other pages that are by definition 'neutral'

neutralPages = [
     '8013404017', # Crikey
     '110627000000000' # Australian government
]

# Yes pages


# No pages

# Exclude entirely

excludes = [
    '425488000000000', # First Peoples' Assembly of Victoria will show up with our classifier but ads relate to Vic-specific treaty negotiations
]

# Page name is actually the easiest identifier for whether an ad will be yes, no or neutral on the voice




# def contains_word(s, word_list):
#     for word in word_list:
#         if re.search(f'\b{word}\b', s):
#             return True
#     return False


# #%%

# contains_word("the voice to parliament", checkWords)

# #%%
# def checkVoiceAds(row):
# 	print(row['ad_creative_bodies'])
# 	check = contains_word(row['ad_creative_bodies'], checkWords)
# 	return check

# df['voice_ad'] = df.apply(checkVoiceAds, axis=1)