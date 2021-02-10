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
from gensim import corpora
import pprint
import re

query = 'unicorns'
site= 'https://api.lib.harvard.edu/v2/items?q='+query+'&limit=50'
# place into their regex
site = site.replace(" ", "%20")
site = str(site)

hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "xml")
print(site)
from collections import Counter

subjectText = []
# first, topics
subjects = soup.find_all('mods:topic')
for subject in subjects:
   #print(subject.get_text())
   subjectText.append(subject.get_text())

regionText = []
regions = soup.find_all('mods:geographic')
for region in regions:
   #print(region.get_text())
   regionText.append(region.get_text())

most_common_geographic = [word for word, word_count in Counter(regionText).most_common(5)]

full_list = subjectText + most_common_geographic

# removes the ( ) characters from the list items
table = str.maketrans(dict.fromkeys("()"))

text_corpus = []

for item in full_list:
    item = item.translate(table)
    text_corpus.append(item)
    
# Create a set of frequent words
stoplist = set('for a of the and to in & /'.split(' '))
# Lowercase each document, split it by white space and filter out stopwords
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in text_corpus]
# Count word frequencies
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
pprint.pprint(processed_corpus)

dictionary = corpora.Dictionary(processed_corpus)

print(dictionary)

pprint.pprint(dictionary.token2id)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)



'''
# extract x most common phrases   
most_common_words = [word for word, word_count in Counter(subjectText).most_common(2)]

most_common_geographic = [word for word, word_count in Counter(regionText).most_common(1)]

# combine most common subjects and regions
# most_common_words= most_common_words+most_common_geographic
print(most_common_words)
'''