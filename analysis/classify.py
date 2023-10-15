#%%

import scraperwiki
import pandas as pd 
from sudulunu.helpers import pp, make_num, dumper
import numpy as np 

from collections import Counter
import os 
import time
import spacy
import re

nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher
voice_matcher = PhraseMatcher(nlp.vocab)
associated_matcher = PhraseMatcher(nlp.vocab)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

os.environ["TOKENIZERS_PARALLELISM"] = "false"
from transformers import pipeline

classifier = pipeline("text-classification", model="Joshnicholas/ad-classifier")

data = pd.read_excel("../process/inter/labelled.xlsx", sheet_name='Sheet1')

stance_dicto = {}

no_stance_taken = []
no_campaign = []
yes_campaign = []
other = []

copier = data.copy()
copier = copier.loc[copier['voice_ad'] == 1].copy()
advertisers = copier['page_name'].unique().tolist()

print(len(advertisers))

for addo in advertisers:
    # print(countess)
    # countess += 1

    # addo = '350.org Australia'

    try:

        inter = data.loc[data['page_name'] == addo].copy()
        inter = inter.loc[inter['voice_ad'] == 1].copy()
        side = inter['side'].tolist()

        # counter = Counter(side)
        # siddo = counter.most_common(1)
        side_set = list(set(side))

        if (len(side_set) == 0) or (side_set[0] == np.nan) or (side_set[0] == "nan"):
            no_stance_taken.append(addo)
            stance_dicto[addo] = 'neutral'   

        elif "neutral" in side_set:
            no_stance_taken.append(addo)     
            stance_dicto[addo] = 'neutral' 

        elif "no" in side_set:
            no_campaign.append(addo)
            stance_dicto[addo] = 'no'   
        
        elif "yes" in side_set:
            yes_campaign.append(addo)
            stance_dicto[addo] = 'yes'   
        else:
            other.append(addo)
            stance_dicto[addo] = 'other'

    except Exception as e:
        other.append(addo)
        stance_dicto[addo] = 'other'   

#%%
def prep_words(phrase_matcher, lister):
    ## Ensure strings
    words = [str(x).lower() for x in lister]
    # print(words)

    ## Create phrase list for searching

    patterns = [nlp(x) for x in words]
    print(patterns)

    phrase_matcher.add('AI', None, *patterns)

    ### Read in the scraped data

    return phrase_matcher

#%%
def matcher(matcher_matcher, texto):

    matches = []

    matched_phrases = matcher_matcher(texto)

    if len(matched_phrases) > 0:

        matches = []
        for match_id, start, end in matched_phrases:

            span = texto[start:end]    

            matches.append(span.text)
        
        matches = list(set(matches))

    else:
        sents = False
        matches = None
    
    # return sents
    return matches
    # print(matches)

keywords_voice = [
	'voice to parliament', 
	'canberra voice', 
	'voice referendum',
	'referendum on the voice',
	'yes23',
	'uluru voice',
	'voteyes',
	'yes campaign',
	'no campaign'
	]

keywords_associated = [
              'constitution',
			  'Australia Day',
			  'vote',
			  'yes',
			  'the voice',
			  'no', 
              'indigenous',
              'aborigin',
              'albo',
              'referendum',
              'treaty',
              'recognition',
              'thomas mayo', # supports yes, but in no attack ads
              'mayo',
              'teela reid', # supports yes, but in no attack ads
              'reid',
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
              'uluru',
			   'risky',
			   'divide',
			   'divisive',
			   'executive government',
			   'runforthevoice',
			   'UluruStatement'
              ]

voice_matcher = prep_words(voice_matcher, keywords_voice)
keyword_matcher = prep_words(associated_matcher, keywords_associated)

fromPages = [102329728050606, # yes23
             104180525925926, # fair australia
             117806591312470, # not enough
             1622506634677043, # Senator Jacinta Nampijinpa Price
             113998151684022, # referendum news
             363375540400009, #linda burney
             102292348146435, # The Uluru Statement from the Heart
             103072892843066, # not my voice
             112239124719864, # gen united
             109657605474040, # multicultural voices against the voice
             # 131283957610666, # AJA
             117058357932949, # constitutional equality
             1407150000000000, # empowered communities
             102330000000000 # From the heart
             ]

excludes = [
	196790584582115, # SA Parliament
    425488000000000, # First Peoples' Assembly of Victoria will show up with our classifier but ads relate to Vic-specific treaty negotiations
    103260000000000, # SA government ads are about state voice
    113083000000000 # About SA voice
]

#%%

def checkPages(page_id):
    result = None
    if page_id in fromPages:
        result = True
    return result    

def classifyAd(text):
	# text = tokenizer(text, truncation=True)
    text = text[:512]
    classification = classifier(text)[0]['label']
    return classification
#%%
def checkVoiceKeywords(text):
    body = text.encode("ascii", "ignore")
    body = body.decode(encoding='utf-8')
    body = body.lower()
    body_nlped = nlp(body)
    result = matcher(voice_matcher, body_nlped)
    return result

def checkOtherKeywords(text):
    body = text.encode("ascii", "ignore")
    body = body.decode(encoding='utf-8')
    body = body.lower()
    body_nlped = nlp(body)
    result = matcher(associated_matcher, body_nlped)
    return result

#%%

df = pd.read_csv('training-ads.csv')

df = df[df['page_name'] == "Yes23"]

#%%
def addCheckPages(row):
	result = checkPages(row['page_id'])
	return result

df['known_advertisers'] = df.apply(addCheckPages, axis=1)
#%%
def classifyAds(row):
# 	print(row['concat_text'])
	if pd.notnull(row['concat_text']):
		result = classifyAd(row['concat_text'])
		return result
	else:
		return None

df['voice_ad_classified'] = df.apply(classifyAds, axis=1)
	
#%%	
def addVoiceKeywords(row):
	if pd.notnull(row['concat_text']):
		result = checkVoiceKeywords(row['concat_text'])
		return result 

df['voice_keywords'] = df.apply(addVoiceKeywords, axis=1)

#%%

def addOtherKeywords(row):
	if pd.notnull(row['concat_text']):
		result = checkOtherKeywords(row['concat_text'])
		return result 

df['other_keywords'] = df.apply(addOtherKeywords, axis=1)


#%%

# keywords but not voice ads

# def checkKeys(row):
# 	keys = row['keywords']

# 	if keys and row['voice_ad'] == 1:
# 		return "Matched"
# 	elif keys and row['voice_ad'] == 0:
# 		return "Keys not ad"
# 	elif not keys and row['voice_ad'] == 1:
# 		return "Ad not keys"
# 	else:
# 		return  "Other"	

# df['check_keys'] = df.apply(checkKeys, axis=1)	
import ast

def scoreCounter(score, addition):
	new_score = score + addition
	if new_score >= 100:
		new_score = 100
		return new_score
	else:
		return new_score

def algo(voice_ad_classified, voice_keywords, page_id, other_keywords, concat_text):
	
	# Generate a score out of 100 for voice ad confidence	
	
	score = 0
	
	classified = False
	
	if voice_ad_classified == 'Is a Voice ad':
		classified = True

	is_known_page = False
	if page_id in fromPages:
		is_known_page = True
		
	is_excluded_page = False
	if page_id in excludes:
		is_excluded_page = True
	
	if pd.notnull(concat_text):
		print(concat_text)
		if "Voice" in concat_text:
			score = scoreCounter(score, 10)
	
	if is_known_page:
		score = scoreCounter(score, 90)
	
	if classified:
		score = scoreCounter(score, 50)
	
	if other_keywords:
		if (type(other_keywords) is not list):			
			other_keywords = ast.literal_eval(other_keywords)
		words = len(other_keywords)
		score = scoreCounter(score, words * 10)
		
	if voice_keywords:
		print(voice_keywords)
		score = scoreCounter(score, 70)	
	
	if is_excluded_page:
		score = 0
	print(score)	
	return score	


def addScore(row):
	score = algo(row['voice_ad_classified'], row['voice_keywords'], row['page_id'], row['other_keywords'], row['concat_text'])
	return score



df['score'] = df.apply(addScore, axis=1)


#%%

df['algo'] = False
df.loc[df['score'] > 50, 'algo'] = True
df['count'] = 1
algo_rating = df[['voice_ad', 'algo', 'count']].groupby(['voice_ad', 'algo']).sum()
algo_rating['pct'] = algo_rating['count'] / algo_rating.groupby('voice_ad')['count'].transform('sum')

remainder = df[(df['voice_ad'] == 1) & (df['algo'] == False)].to_csv('remainder.csv')
pickups = df[(df['voice_ad'] == 0) & (df['algo'] == True)].to_csv('pickups.csv')

#%%

model_rating = df[['voice_ad', 'voice_ad_classified', 'count']].groupby(['voice_ad', 'voice_ad_classified']).sum()
model_rating['pct'] = model_rating['count'] / model_rating.groupby('voice_ad')['count'].transform('sum')


#%%




#%%


# Run the classifier and keyword matcher over the database

# queryString = "* from ads_by_query"
# queryResult = scraperwiki.sqlite.select(queryString)

# for row in queryResult:
#     if row['concat_text']:
#         body = row['concat_text'].encode("ascii", "ignore")
#         body = body.decode(encoding='utf-8')
#         print(row['ad_id'])
#         classification = classifier(row['concat_text'][:512])[0]['label']

#         print(classification)

#         body = body.lower()

#         body_nlped = nlp(body)

#         # print(body_nlped)

#         result = matcher(phrase_matcher, body_nlped)

#         print(result)

#         if row['page_name'] in advertisers:
#             stance = stance_dicto[row['page_name']]
#         else: 
#             stance = None

#         row['voice_ad_modelled'] = classification
#         row['side_inferred'] = stance
#         row['voice_ad_keywords'] = str(result)
#         voice_advertiser = False
#         if row['page_id'] in fromPages:
#             voice_advertiser = True
#         row['voice_advertiser'] = voice_advertiser
#         scraperwiki.sqlite.save(unique_keys=["ad_id"], data=row, table_name="ads_by_query")
#         time.sleep(0.1)

# %%
