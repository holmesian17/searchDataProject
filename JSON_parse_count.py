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
