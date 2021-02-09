try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import csv
import hashlib
import json
from spellchecker import SpellChecker
import os,sys
import pickle
from bs4 import BeautifulSoup
import pandas as pd    
from collections import Counter
import time

# CSV header names
fieldnames = ['Search','Corrected','Timestamp','IP',
              'Search Function','Category']

search_file_in = open('rawDataSampleWithCats.csv', "rt")
reader = csv.DictReader(search_file_in)

search_file_out = open('dataSampleFormatted.csv', "wt")
writer = csv.DictWriter(search_file_out,
                        fieldnames=(fieldnames))
writer.writeheader()
# categoryDict = {}
# need to save these to an external file to pull from

with open("categoryDict.json", "r") as config_file:
    category_dict = json.load(config_file)

print(category_dict)

spell = SpellChecker(distance=1)
       

for row in reader:
    #hashing ip address
    ip_address = row['IP'] #3

    #print(ipAddress)
    hash_object = hashlib.sha1(ip_address.encode('utf-8')).hexdigest()
    #print(hash_object)
    row['IP'] = hash_object
    
    #adding keys and values to categories
    term = row['Search'] #0
    category = row['Category'] #5
    
    term = term.lower()
    
    # there's an easier way to add to dict in the readthedocs for pyspellchecker
    corrected_text = spell.correction(term)
    
    row['Corrected'] = corrected_text #1
    
    query = corrected_text
    site= 'https://api.lib.harvard.edu/v2/items?q='+query+'&limit=50'
    # place into their regex
    site = site.replace(" ", "%20")
    site = str(site)

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "xml")
    print(site)

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

    # extract x most common phrases   
    most_common_words = [word for word, word_count in Counter(subjectText).most_common(5)]

    most_common_geographic = [word for word, word_count in Counter(regionText).most_common(1)]

    # combine most common subjects and regions
    # most_common_words= most_common_words+most_common_geographic
    print(most_common_words) 
    # open library subjects for keyword result
    # 5 categories are the 5 most common subjects for the keyword search
    # add to dictionary and automatically add categories if that term is searched again
    
    writer.writerow(row)
    
    #print(term)
    #print(corrected_text)
  
    
'''
    # search the JSON file to see if the term has a category
    # if so, add 
    if term in categoryDict:
        #add category to csv file in category column for the existing term
        continue
    else:
        categoryDict[term] = category      
        
'''
    
   #print(categoryDict)
'''    
with open("categoryDict.json", "w") as f:
                f.write(json.dumps(categoryDict))
                # use `json.loads` to do the reverse
                f.close()
print(categoryDict)
'''
