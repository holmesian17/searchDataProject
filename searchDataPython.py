import csv
import hashlib
import json
from spellchecker import SpellChecker
import urllib3
from bs4 import BeautifulSoup
import requests

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

    # open library subjects for keyword result
    # 5 categories are the 5 most common subjects for the keyword search
    # add to dictionary and automatically add categories if that term is searched again
    
    # ALT: harvard library api - api.harvard.edu/v2/items?q=peanuts - returns XML
    # harvard library api - api.harvard.edu/v2/items.json?q=peanuts - returns JSON
    # 5 most common topics in the XML for the five
    # add to dictionary and automatically add categories if that term is searched again
    # wiki.harvard.edu/confluence/display/LibraryStaffDoc/LibraryCloud+APIs
    
    http = urllib3.PoolManager()
    API_URL = str("https://api.lib.harvard.edu/v2/items?q=" + term)
    topicJSON = http.request('GET', API_URL)
    soup = BeautifulSoup(topicJSON, 'html.parser')
    site_json=json.loads(soup.text)

    print([d.get('topic') for d in site_json['subject'] if d.get('topic')])
    
    writer.writerow(row)
    
    print(term)
    print(corrected_text)
  
    
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
