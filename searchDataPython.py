import csv
import hashlib
import json
from spellchecker import SpellChecker
import urllib3

fieldnames = ['Search','Corrected','Timestamp','IP',
              'Search Function','Category']

searchFileIn = open('rawDataSampleWithCats.csv', "rt")
reader = csv.DictReader(searchFileIn)

searchFileOut = open('dataSampleFormatted.csv', "wt")
writer = csv.DictWriter(searchFileOut,
                        fieldnames=(fieldnames))
writer.writeheader()
# categoryDict = {}
# need to save these to an external file to pull from

with open("categoryDict.json", "r") as config_file:
    categoryDict = json.load(config_file)

print(categoryDict)

spell = SpellChecker(distance=1)

for row in reader:
    #hashing ip address
    ipAddress = row['IP'] #3

    #print(ipAddress)
    hash_object = hashlib.sha1(ipAddress.encode('utf-8')).hexdigest()
    #print(hash_object)
    row['IP'] = hash_object
    
    #adding keys and values to categories
    term = row['Search'] #0
    category = row['Category'] #5
    
    term = term.lower()
    
    correctedText = spell.correction(term)
    
    row['Corrected'] = correctedText #1
    
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
    
    writer.writerow(row)
    
    #print(term)
    #print(correctedText)
  
    
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
