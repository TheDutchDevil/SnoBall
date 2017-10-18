#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:15:14 2017

@author: hildeweerts
"""
import os
import pandas as pd

working_dir = '/Users/hildeweerts/Desktop/TUe/2IMM15 Web information retrieval and data mining/'
os.chdir(working_dir)

NIPS = pd.read_csv("nips-papers/papers.csv")
authors = pd.read_csv("nips-papers/authors.csv")
paper_authors = pd.read_csv("nips-papers/paper_authors.csv")
paper_authors_cleaned = pd.read_csv("nips-papers/new_paper_authors.csv")

#%%
"""
Find references
"""
import numpy as np
import re
from datetime import datetime
startTime = datetime.now()

library = NIPS 
sub = ["References", "Rererences", "Referenes", "Reference", 
       "REFERENCE", "Referenees", "Referen", "Bibliography", "Refereaces",
       "Literature cited", "Ref erences", "BIBLIOGRAPHY", "Refe ren ces", 
       "Ref eren ces", "R e f er e n ce s", "R e f e re n c e s", "R e fer e nces",
       "R ef erence s", "Refrences", "Iteferences", "Refel~ences" ]

def find_sub(splits, sub):
  indexlist = []
  for idx, s in enumerate(splits):
      for su in sub: # for each subword in the list
          if su in s[0:25]:
              indexlist.append(idx) #append index of split to list
  if len(indexlist) > 0:
 #     print(splits[indexlist[-1]]) #check if it is a reference
      return(max(indexlist)) #return last found 'reference'
  return None  

notfound = []
found = []
refdict = {}

nrrefs = 0
for i in library.iterrows():
    text = i[1]["paper_text"]
    splits = [x + "\n" for x in text.split("\n")] # split after every enter
    index = find_sub(splits, sub)
    if index == None:
        notfound.append(i[0])
    else:
        found.append(i[0])
        references = ''.join(splits[index+1:len(splits)]) 
        splitz = [x for x in references.split(".\n")] # split after every .enter
        splitz2 = [s.replace("\n", "") for s in splitz] # remove linebreaks
        splitz3 = [s for s in splitz2 if len(s) > 30]
        nrrefs += len(splitz3)
        refdict[i[1]['id']] = splitz3 # add to dictionary     
print(datetime.now() - startTime)

#%%
""" 
Request references in DBLP API
"""
import requests
import json
import re
import unicodedata

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def request_title(q):
    params = {
           'q': q,
           'h': 1,
           'format': 'json'}
    response = requests.get("http://dblp.org/search/publ/api", params = params).json()
    if response['result']['hits']['@total'] == '1':
        title = response['result']['hits']['hit'][0]['info']['title'][:-1]
    else: 
        title = None
    return title

nrfound = 0
nrnotfound = 0
keys = refdictNIPS.keys()
x = len(keys)

#refdictNIPS = {}

for key, value in refdict.items():
    if key in keys:
        None
    else:
        print(x)
        print("Document id: " + str(key))
        reference_list = [] # clear reference list of entry
        for i in value:
            iSplit = re.split("\.|\,", i) #split reference on . and ,
            q = max(iSplit, key = len) #find longest and clean
            title = request_title(remove_control_characters(q))
            if title != None: # we found something
                reference_list.append(title)
                nrfound += 1
            else: # we did not find anything
                nrnotfound += 1
        refdictNIPS[key] = reference_list
        x += 1
#%%
"""
Match found titles with NIPS titles
"""
import Levenshtein

citations = {} # dictionary with per paper the paper ids that were cited by this paper
citations_source = []
citations_dest = []

counter = 0
lcounter = 0
for key, value in refdictNIPS.items():
    reference_list_ids = []
    for i in value:
        # find direct matches
        dfslice = NIPS[NIPS['title'] == i] 
        # find entries with levenshtein distance < 5
        candidate = NIPS[NIPS.title.apply(lambda x: int(Levenshtein.distance(i, x)) < 5)].id.tolist()
        if len(dfslice) > 0:
            counter += 1
            reference_list_ids.append(dfslice['id'][dfslice.index[0]])
            citations_source.append(key)
            citations_dest.append(dfslice['id'][dfslice.index[0]])
        elif len(candidate) > 0: 
            lcounter += 1
            reference_list_ids.append(candidate[0])
            citations_source.append(key)
            citations_dest.append(candidate[0])
    if len(reference_list_ids) > 0:
        citations[key] = reference_list_ids

#%%
""" Create and export paper citation graph """
citation_edges = pd.DataFrame(
        {'Source':citations_source, 
         'Target':citations_dest})

print(counter)
print(lcounter)

citation_edges.to_csv('citation_graph.csv', index = False)

#%%
""" Create and export co citation graph """
grouped_citation = citation_edges.groupby(by = 'Source')

target_lists = {}
for name, group in grouped_citation:
    target_lists[name] = group['Target'].tolist()

cocitation_sources = []
cocitation_targets = []
cocitation_ids = []

for name, value in target_lists.items():
    for i in list(itertools.combinations(value, 2)):
        cocitation_ids.append(name)
        cocitation_sources.append(min(i))
        cocitation_targets.append(max(i))

co_citation_edges = pd.DataFrame(
        {'Source':cocitation_sources, 
         'Target':cocitation_targets,
         'Cited by':cocitation_ids})

co_citation_edges.to_csv('co-citation_graph.csv', index = False)

#%%
"""
# Create and export author citation graph 
author_sources = []
author_targets = []
for i in range(0,len(citations_source)):
    source = citations_source[i]
    target = citations_dest[i]
    authors_source = paper_authors[paper_authors['paper_id'] == source].author_id.tolist()
    authors_target = paper_authors[paper_authors['paper_id'] == target].author_id.tolist()
    for s in authors_source:
        for t in authors_target:
            author_sources.append(s)
            author_targets.append(t)
#print("Number of authors regular: " + str(len(set((author_sources + author_targets)))))

citation_authors_edges = pd.DataFrame(
        {'Source':author_sources, 
         'Target':author_targets})
    
citation_authors_edges.to_csv('citation_graph_authors.csv', index = False)

# Create and export author citation graph cleaned author data
author_sources = []
author_targets = []
for i in range(0,len(citations_source)):
    source = citations_source[i]
    target = citations_dest[i]
    authors_source = paper_authors_cleaned[paper_authors_cleaned['paper_id'] == source].author_id.tolist()
    authors_target = paper_authors_cleaned[paper_authors_cleaned['paper_id'] == target].author_id.tolist()
    for s in authors_source:
        for t in authors_target:
            author_sources.append(s)
            author_targets.append(t)
#print("Number of authors cleaned: " + str(len(set((author_sources + author_targets)))))

citation_authors_edges_cleaned = pd.DataFrame(
        {'Source':author_sources, 
         'Target':author_targets})
    
citation_authors_edges_cleaned.to_csv('citation_graph_authors_cleaned.csv', index = False)
"""
#%%
import json
with open('citations-titles.json', 'w') as fp:
    json.dump(refdictNIPS, fp)

#%%
""""
APPROACH
1. Identify the bibliography section; to generalize: could use 
    * wildcard regex expression, 
    * levenshtein distance (need to compute for each word?)
    * k-gram index; but we want precise place so maybe not so useful
2. Extract titles from references: heuristic
3. Find dblp entry based on title from parsed paper: API
4. Match dblp entries with NIPS database entries: Levenshtein distance

Comments
- author citation graph is 4070 versus 3950 distinct authors (= nodes) in not cleaned vs. cleaned

"""