#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:40:43 2017

@author: hildeweerts
"""

#%%
import os
import pandas as pd

working_dir = '/Users/hildeweerts/SnoBall/'
os.chdir(working_dir)

authors = pd.read_csv("Execute/Papers/new_authors.csv").sort_index()

#%%
"""
request 8000 - 8356
"""
import requests 

apikey = 'key'

authorids = []
firstnames_orig = []
lastnames_orig = []
affiliations = []
firstnames = []
surnames = []
subjectareas = []
citedbycounts = []
hindexes = []

counter  = 0

for i in authors[8000:len(authors)].iterrows():
    counter += 1
    print(counter)
    authorid = i[1]['id']
    authorids.append(authorid)
    authorname = i[1]['name']
    authornames = [item[::-1] for item in authorname[::-1].split(' ', 1)][::-1]
    if len(authornames) == 2: #if we find a first and last name
        firstname = authornames[0]
        lastname = authornames[1]
        firstnames_orig.append(firstname)
        lastnames_orig.append(lastname)
        
        #define query
        query = 'authlast(' + lastname + ') and authfirst(' + firstname +')'  
        
        #search author
        searchresult = requests.get("http://api.elsevier.com/content/search/author", 
                     params = {'query': query,'apiKey': apikey} 
                     ).json()
        #if we do not find an error, append results
        if 'error' not in searchresult['search-results']['entry'][0]:
            if 'affiliation-current' in searchresult['search-results']['entry'][0]:
                affiliations.append(searchresult['search-results']['entry'][0]['affiliation-current'])
            else:
                affiliations.append(None)
                
            firstnames.append(searchresult['search-results']['entry'][0]['preferred-name']['given-name'])
            surnames.append(searchresult['search-results']['entry'][0]['preferred-name']['surname'])
            
            if 'subject-area' in searchresult['search-results']['entry'][0]:
                subjectareas.append(searchresult['search-results']['entry'][0]['subject-area'])
            else:
                subjectareas.append(None)
            authorid = searchresult['search-results']['entry'][0]['dc:identifier']
            
        #retrieve citation count and h-index
            retrieveresult = requests.get("https://api.elsevier.com/content/author/author_id/" + authorid, 
                                      params = {'apiKey': apikey, 
                                                'view': 'METRICS', 
                                                'httpAccept': 'application/json'
                                                }).json()
            
            if retrieveresult['author-retrieval-response'][0]['@status'] != 'not_found':
                citedbycounts.append(retrieveresult['author-retrieval-response'][0]['coredata']['cited-by-count'])
                hindexes.append(retrieveresult['author-retrieval-response'][0]['h-index'])
            else:
                citedbycounts.append(None)
                hindexes.append(None)
        # if we cannot find an author, retrieve none
        else: 
            affiliations.append(None)
            firstnames.append(None)
            surnames.append(None)
            subjectareas.append(None)
            citedbycounts.append(None)
            hindexes.append(None)
    else:
        firstnames_orig.append(None)
        lastnames_orig.append(None)
        affiliations.append(None)
        firstnames.append(None)
        surnames.append(None)
        subjectareas.append(None)
        citedbycounts.append(None)
        hindexes.append(None)
        
#%%%
import pandas as pd

resultdf = pd.DataFrame({
        'id': authorids,
        'first name (orig)': firstnames_orig,
        'last name (orig)': lastnames_orig,
        'affiliation': affiliations,
        'first name': firstnames,
        'last name': surnames,
        'subject areas': subjectareas,
        'cited by count': citedbycounts,
        'h-index': hindexes
        })
    
    #%%
resultdf.to_csv('8000-8355.csv')