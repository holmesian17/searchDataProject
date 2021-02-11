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


query = 'The Fast and the Furious'
query = query.lower()

site= 'https://api.lib.harvard.edu/v2/items?q='+query+'&limit=250'

# if search by title
#titleSearch = 'https://api.lib.harvard.edu/v2/items?titleInfo='+query+'&limit=250'

# if search by author
#authorSearch = 'https://api.lib.harvard.edu/v2/items?subject.name='+query+'&limit=250'


# place into their regex
site = site.replace(" ", "%20")
site = str(site)

hdr = {'User-Agent': 'Mozilla/5.0'} # for Harvard
req = urllib2.Request(site,headers=hdr) #for Harvard
page = urllib2.urlopen(req) #for Harvard
soup = BeautifulSoup(page, "xml")
print(site)
from collections import Counter

subjectText = []
# first, topics
subjects = soup.find_all('mods:topic')
for subject in subjects:
   #print(subject.get_text())
   subjectLower = subject.get_text().lower() 
   subjectText.append(subjectLower)

while 'history' in subjectText: subjectText.remove('history')
while 'history and criticism' in subjectText: subjectText.remove('history and criticism')
    


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

most_common_subject = [word for word, word_count in Counter(subjectText).most_common(5)]

# most_common_title = [word for word, word_count in Counter(titleText).most_common(5)]

fullText = subjectText + regionText

most_common= [word for word, word_count in Counter(fullText).most_common(5)]

print(most_common)

#print(most_common)
