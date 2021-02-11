# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:23:15 2016

@author: chase
"""
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import os,sys
import pickle
from bs4 import BeautifulSoup
import pandas as pd    
from collections import Counter
import json
import requests
import pprint


query = 'Kentucky'
query = query.lower()

site = 'https://openlibrary.org/search.json?q='+query+'&limit=250'

# if search by title
#titleSearch = 'https://openlibrary.org/search.json?title='+query+'&limit=250'

# if search by author
#authorSearch = 'https://openlibrary.org/search.json?author='+query+'&limit=250'

# place into their regex

site = site.replace(" ", "+") # for OpenLibrary
site = str(site)
print(site)


response = requests.get(site)
siteData = json.loads(response.text)
#print(siteData)

data = siteData['docs']
subjects = [item.get('subject') for item in data]

removeNoneType = [i for i in subjects if i] 

flat_list = [item for sublist in removeNoneType for item in sublist]

#print('Original List: ',subjects)
#print('Flattened list: ',flat_list)
       

from collections import Counter

subjectText = []

for subject in flat_list:
   #print(subject.get_text())
   subjectLower = subject.lower() 
   subjectText.append(subjectLower)

# may end up wanting this to be an external document
stopwords = ['accessible book', 'protected daisy',
             'juvenile literature', 'juvenile nonfiction',
             'juvenile fiction']

for stopword in stopwords:
    while stopword in subjectText:
        subjectText.remove(stopword)
        
print('Cleaned Subject List: ', subjectText)

'''
regionText = []
regions = soup.find_all('mods:geographic')
for region in regions:
   #print(region.get_text())
   regionText.append(region.get_text())

titleText = []
titles = soup.find_all('mods:titleInfo')
for title in titles:
    titleWords = title.get_text()
    titleSplit = titleWords.split() #prolly need to remove stopwords
    stopwords = ['for', 'a', 'of', 'the', 'and', 'to', 'in', '&', '/',';',
                'with', 'series']
    for word in titleSplit:
        titleText.append(word)
        if word in stopwords:
            titleText.remove(word)
            
        #print(title.get_text())

most_common_title = [word for word, word_count in Counter(titleText).most_common(1)]

#print(most_common_title)

most_common_geographic = [word for word, word_count in Counter(regionText).most_common(1)]
'''

most_common_subject = [word for word, word_count in Counter(subjectText).most_common(5)]

# most_common_title = [word for word, word_count in Counter(titleText).most_common(5)]



print(most_common_subject)

#print(most_common)
''