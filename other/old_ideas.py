# old ideas
'''
    # this drastically slows things down - maybe not show off at first but talk out
    # with Tova
    http = urllib3.PoolManager()
    # make the API search for whatever the search term was
    # this API also seems to have subjects and other fun stuff
    # could be useful in the categories thing
    # for example, most common subject of results = the category???
    # only works for books currently, how to handle dvds, etc.?
    term = term.split()
    term = '+'.join(term)
    apiURL = str("http://openlibrary.org/search.json?title=" + term)
    # for multiple words it needs to split them and add a + between
    books = http.request('GET', apiURL)
    bookDict = json.loads(books.data.decode('UTF-8'))

    # ALT: harvard library api - api.harvard.edu/v2/items?q=peanuts - returns XML
    # harvard library api - api.harvard.edu/v2/items.json?q=peanuts - returns JSON
    # 5 most common topics in the XML for the five
    # add to dictionary and automatically add categories if that term is searched again
    # wiki.harvard.edu/confluence/display/LibraryStaffDoc/LibraryCloud+APIs
    
'''


    
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

site= 'https://api.lib.harvard.edu/v2/items?q=Kentucky'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "xml")

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

#Program to find most frequent  
# element in a list

totalText = subjectText + regionText

def most_frequent(List):
    return max(set(List), key = List.count)
    

print(most_frequent(totalText)) 
# print(most_frequent(regionText))
