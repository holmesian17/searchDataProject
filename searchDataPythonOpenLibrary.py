import csv
import hashlib
import json
from spellchecker import SpellChecker
import os,sys
import requests
from collections import Counter
import time
from langdetect import detect

# CSV header names
fieldnames = ['Search','Corrected','Timestamp','IP',
              'Search Function','Cat1','Cat2','Cat3',
              'Cat4','Cat5',"Custom Cat1", "Custom Cat2", "Language"]

search_file_in = open('rawDataSampleWithCats.csv', "rt")
reader = csv.DictReader(search_file_in)

search_file_out = open('dataSampleFormattedOpenLibrary.csv', "wt")
writer = csv.DictWriter(search_file_out,
                        fieldnames=(fieldnames))
writer.writeheader()


spell = SpellChecker(distance=1)

# needs to be able to handle and record JSON exceptions that
# randomly pop up

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
    corrected_term = spell.correction(term)

    '''
    # have it determine if it's closest to spanish or english
    # exclude other languages to minimize the junk we were getting
    try:
        language = detect(term)
        if term == 'en':
            corrected_term = spell.correction(term)
        else:
            corrected_term = term
            row['Language'] = language
    except:
        continue
    row['Corrected'] = corrected_term #1
    '''
    query = corrected_term.lower()
    site = 'https://openlibrary.org/search.json?q='+query+'&limit=100'

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
    # combine most common subjects and regions
    # most_common_words= most_common_words+most_common_geographic
    print("Term: " + corrected_term)
    print("Topics: ")
    
    from collections import Counter

    subjectText = []

    for subject in flat_list:
       #print(subject.get_text())
       subjectLower = subject.lower() 
       subjectText.append(subjectLower)

    # may end up wanting this to be an external document
    stopwords = ['accessible book', 'protected daisy',
                 'juvenile literature', 'juvenile nonfiction',
                 'juvenile fiction', 'fiction']

    for stopword in stopwords:
        while stopword in subjectText:
            subjectText.remove(stopword)
            
    print('Cleaned Subject List: ', subjectText)
    
    # open library subjects for keyword result
    # 5 categories are the 5 most common subjects for the keyword search
    # add to dictionary and automatically add categories if that term is searched again

    most_common_subject = [word for word, word_count in Counter(subjectText).most_common(5)]

    print(most_common_subject)
    try:
        if not most_common_subject:
            row['Cat1'] = "N/a"
            row['Cat2'] = "N/a"
            row['Cat3'] = "N/a"
            row['Cat4'] = "N/a"
            row['Cat5'] = "N/a"
        else:
            row['Cat1'] = most_common_subject[0]
            row['Cat2'] = most_common_subject[1]
            row['Cat3'] = most_common_subject[2]
            row['Cat4'] = most_common_subject[3]
            row['Cat5'] = most_common_subject[4]
    except:
        pass
    
    custom_categories = {"fort collins":"fort collins", "dog":"pets", "dogs":"pets",
                         "unicorns":"children"}
    
    if query in custom_categories:
        row["Custom Cat1"] = custom_categories.get(query)
        print("Custom: ", custom_categories.get(query))
    else:
        row["Custom Cat1"] = ""

    '''
    if query == "fort collins":
        row["Custom Cat1"] = "fort collins"
    else:
        row["Custom Cat1"] = ""
    '''
# needs to handle if there isn't a 5th term, 4th term, etc.
        
    
    writer.writerow(row)
    #time.sleep(1)
    
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

