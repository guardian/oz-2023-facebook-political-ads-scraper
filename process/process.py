# %%
import sqlite3
import pandas as pd 
from sudulunu.helpers import pp, make_num, dumper
import numpy as np 

from collections import Counter
import os 
import pathlib
pathos = pathlib.Path(__file__).parent.parent
os.chdir(pathos)
print(os.getcwd())

import spacy
import re

nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher
phrase_matcher = PhraseMatcher(nlp.vocab)

from transformers import pipeline
## Zero shot classifer
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

# %%
### Need to infer the yes/no stances from the labelled data

# urlo = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTACLNmVRNPXzaNpMohWwwQwRM9VEDgCPJRHMAL2yLaZnLRApPfGpBFbJOj7Mmsow0s3yBKxsOk5OoC/pub?output=xlsx'
# data = pd.read_excel(urlo, sheet_name='tagged-ads.csv')
# data.to_excel('process/inter/labelled.xlsx', engine='xlsxwriter')

data = pd.read_excel("process/inter/labelled.xlsx", sheet_name='Sheet1')
# 'Unnamed: 0', 'voice_ad', 'side', 'ad_id', 'page_id', 'query', 'page_name', 
# 'ad_creative_bodies', 'ad_creative_link_titles', 'ad_creative_link_captions', 
# 'ad_creative_link_descriptions', 'ad_snapshot_url'

stance_dicto = {}

no_stance_taken = []
no_campaign = []
yes_campaign = []
other = []

copier = data.copy()
copier = copier.loc[copier['voice_ad'] == 1].copy()
advertisers = copier['page_name'].unique().tolist()

print(len(advertisers))

# addo = 'Advance Australia'

# print(advertisers[372])



countess = 0
for addo in advertisers:
    # print(countess)
    # countess += 1

    # addo = '350.org Australia'

    try:

        inter = data.loc[data['page_name'] == addo].copy()
        inter = inter.loc[inter['voice_ad'] == 1].copy()
        side = inter['side'].tolist()

        counter = Counter(side)
        siddo = counter.most_common(1)

        if (len(side) == 0) or (siddo[0][0] == np.nan) or (siddo[0][0] == "nan"):
            no_stance_taken.append(addo)
            stance_dicto[addo] = 'neutral'   
        # else:
        #     print(siddo[0][0])

        elif siddo[0][0].lower() == "neutral":
            no_stance_taken.append(addo)     
            stance_dicto[addo] = 'neutral'   

        elif siddo[0][0].lower() == "no":
            no_campaign.append(addo)
            stance_dicto[addo] = 'no'   
        
        elif siddo[0][0].lower() == "yes":
            yes_campaign.append(addo)
            stance_dicto[addo] = 'yes'   

        else:
            other.append(addo)
            stance_dicto[addo] = 'other'

    except Exception as e:
        other.append(addo)
        stance_dicto[addo] = 'other'   

# print("yes_campaign = ", yes_campaign)
# print("no_campaign = ", no_campaign)
# print("no_stance_taken = ", no_stance_taken)
# print("other = ", other)

# print("len(yes_campaign): ", len(yes_campaign))
# print("len(no_campaign): ", len(no_campaign))
# print("len(no_stance_taken): ", len(no_stance_taken))
# print("len(other): ", len(other))


# yes_campaign =  ['Amanda Rishworth MP', 'Andrea Michaels MP', 'Andrew Charlton MP', 'Andrew Leigh MP', 'Anika Wells MP', 'ANTAR', 'Australian Unions', 'Bathurst For Yes', 'Bill Shorten', 'Brian Mitchell MP - Federal Member for Lyons', 'Brittany Lauga MP', 'Central Land Council', 'ChangeMakers', 'City of Sydney', 'Corrine McMillan MP - State Member for Mansfield', 'Councillor Jared Cassidy', 'Daniel Mulino', 'Dr Katrina Stratton MLA', 'Dr Michelle Ananda-Rajah MP', 'Dr Monique Ryan', 'Ed Husic MP', 'Edmond Atalla MP', 'Empowered Communities', 'First Nations LGBTQ Elders Coalition', 'From the Heart', 'Gen united', 'GetUp!', 'Independent Education Union of Australia NSW / ACT Branch', 'Indian Link', 'Instagram User 233713112', 'Jason Yat-sen Li MP', 'Jennifer Howard MP', 'Jerome Laxale MP', 'Justine Elliot MP', 'Kristy McBain', 'Matt Keogh', 'Murray Watt - Senator for Queensland', 'Nathan Lambert MP', 'Newcastle Greens', 'Northern Land Council', 'NSW Nationals for Murray', 'Oxfam', 'Patrick Gorman MP', 'Peta Murphy MP Federal Member for Dunkley', 'Reconciliation NSW', 'Russell Broadbent MP', 'Sam Lim MP', 'Senator Anne Urquhart', 'Senator Anthony Chisholm', 'Senator Jess Walsh', 'Sheena Watt MP', 'South Australian Labor', 'Yes23']
# no_campaign =  ['Advance Australia', 'Alex Hawke MP', 'Andrew Hastie', 'Andrew Laming', 'Andrew Willcox MP', 'Angus Taylor MP', 'Australian Borders for a better future. Australia First', 'Australian Christian Lobby', 'Australian Jewish Association - AJA', 'BOX4', 'Church And State', 'Clynton Hawks', 'Colin Boyce MP', 'Collins 4 Community', 'Constitutional Equality', 'CPAC Australia', 'David Littleproud MP', 'Dr David Honey MLA', 'Fair Australia', 'FamilyVoice Australia', 'FreeMarketGarden', 'Garth Hamilton MP', 'Henry Pike MP', 'Institute of Public Affairs', 'Jason Wood MP', 'Kerrynne Liddle - Liberal Senator for SA', 'Linda Champion', 'Multicultural Voices Against the Voice', 'National Party of Australia', 'Not Enough', 'Not My Voice', "Pauline Hanson's One Nation Party", 'Phillip Thompson OAM MP - Serving Our Community', 'Recognise a Better Way', 'Referendum News', 'Rick Wilson', 'Senator Babet', 'Senator Bridget McKenzie', 'Senator Jonno Duniam', "Senator Matt O'Sullivan", 'Senator Michaelia Cash', 'Senator Paul Scarr', 'Senator Perin Davey']
# no_stance_taken =  ['Alicia Payne MP', 'Allegra Spender', 'Australian Government', 'Australian Indian Radio', 'Blak Wattle Coaching and Consulting', 'Catherine Hutchesson MP', 'Councillor John Stamolis', 'Cr Ashleigh Vandenberg - City of Melton - Coburn Ward', 'Crikey', 'Dave Kelly MP', 'David Pocock', 'Dr Sophie Scamps', 'Ethnic Communities Council of WA', 'Goodstart Early Learning Cockburn Central', 'LNP - Liberal National Party', 'Matt Thistlethwaite MP', 'Senator Sue Lines', 'The Australian National University', 'The University of Melbourne']
# other =  ['National Poll', 'OZ Arab Media', 'Peter Khalil']

# len(yes_campaign):  53
# len(no_campaign):  43
# len(no_stance_taken):  19
# len(other):  3


# %%


# %%

def prep_words(lister):
    ## Ensure strings
    words = [str(x).lower() for x in lister]
    # print(words)

    ## Create phrase list for searching

    patterns = [nlp(x) for x in words]
    # print(patterns)

    phrase_matcher.add('AI', None, *patterns)

    ### Read in the scraped data

    return phrase_matcher


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
        matches = ''
    
    # return sents
    return matches
    # print(matches)


# %%

keywords = ['parliament', 
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

phrase_matcher = prep_words(keywords)


# %%

db = 'scraperwiki.sqlite'
con = sqlite3.connect(db)

cur = con.cursor()

entries = [x for x in cur.execute('SELECT * FROM ads_by_query')]
# entries = [x for x in cur.execute('SELECT * FROM ads_by_id')]

con.close()

# %%

records = []

for entry in entries[:2]:
    print(entry)

    ad_id = entry[0]
    advertiser_id = entry[1]
    name = entry[3]
    texto = entry[4]

    body = texto.encode("ascii", "ignore")
    body = body.decode(encoding='utf-8')
    body = body.lower()

    body_nlped = nlp(body)

    print(body_nlped)

    result = matcher(phrase_matcher, body_nlped)

    print(result)

    if name in advertisers:
        stance = stance_dicto[name]
    else: 
        stance = ''

    records.append({"Ad_id": ad_id, "Advertiser": advertiser_id,"Name": name, "Keywords": result, "Advertiser_stance": stance, "Text": texto})

# %%

cat = pd.DataFrame.from_records(records)

pp(cat)
# %%
