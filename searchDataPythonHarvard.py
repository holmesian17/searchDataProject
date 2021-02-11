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
              'Search Function','Cat1','Cat2','Cat3',
              'Cat4','Cat5','Geo','Genre']

search_file_in = open('rawDataSampleWithCats.csv', "rt")
reader = csv.DictReader(search_file_in)

search_file_out = open('dataSampleFormattedHarvard.csv', "wt")
writer = csv.DictWriter(search_file_out,
                        fieldnames=(fieldnames))
writer.writeheader()
# categoryDict = {}
# need to save these to an external file to pull from
'''
with open("categoryDict.json", "r") as config_file:
    category_dict = json.load(config_file)

print(category_dict)
'''
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
    # category = row['Category'] #5
    
    term = term.lower()
    
    # there's an easier way to add to dict in the readthedocs for pyspellchecker
    corrected_term = spell.correction(term)
    
    row['Corrected'] = corrected_term #1
    
    query = corrected_term
    site= 'https://api.lib.harvard.edu/v2/items?q='+query+'&limit=250'
    # place into their regex
    site = site.replace(" ", "%20")
    site = str(site)

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "xml")
    #print(site)

    subjectText = []
    # first, topics
    subjects = soup.find_all('mods:topic')
    for subject in subjects:
       #print(subject.get_text())
        subjectText.append(subject.get_text())
    
    while 'History' in subjectText: subjectText.remove('History')
    
    regionText = []
    regions = soup.find_all('mods:geographic')
    for region in regions:
       #print(region.get_text())
       regionText.append(region.get_text())
    
    genreText = []
    genres = soup.find_all('mods:genre')
    for genre in genres:
        #print(genre.get_text())
        genreText.append(genre.get_text())
    
    while 'bibliography' in genreText: genreText.remove('bibliography')

    
    # extract x most common phrases   
    most_common_words = [word for word, word_count in Counter(subjectText).most_common(5)]

    most_common_geographic = [word for word, word_count in Counter(regionText).most_common(1)]
    
    most_common_genre = [word for word, word_count in Counter(genreText).most_common(1)]
        
    # combine most common subjects and regions
    # most_common_words= most_common_words+most_common_geographic
    print("Term: " + corrected_term)
    print("Topics: ")
    print(most_common_words)
    print("Geographic: ")
    print(most_common_geographic)
    print("Genre: ")
    print(most_common_genre)
    # open library subjects for keyword result
    # 5 categories are the 5 most common subjects for the keyword search
    # add to dictionary and automatically add categories if that term is searched again
    try:
        if not most_common_words:
            row['Cat1'] = "N/a"
            row['Cat2'] = "N/a"
            row['Cat3'] = "N/a"
            row['Cat4'] = "N/a"
            row['Cat5'] = "N/a"
        else:
            row['Cat1'] = most_common_words[0]
            row['Cat2'] = most_common_words[1]
            row['Cat3'] = most_common_words[2]
            row['Cat4'] = most_common_words[3]
            row['Cat5'] = most_common_words[4]
    except:
        pass
    if not most_common_geographic:
        row['Geo'] = "N/a"
    else:
        row['Geo'] = most_common_geographic[0]
    if not most_common_genre:
        row['Genre'] = "N/a"
    else:
        row['Genre'] = most_common_genre[0]
        
    
    writer.writerow(row)
    time.sleep(1)
    
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
