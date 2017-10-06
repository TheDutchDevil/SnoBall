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

#%%
NIPS_noabstr = NIPS[NIPS['abstract'] == 'Abstract Missing'].reset_index()
NIPS_abstr = NIPS[NIPS['abstract'] != 'Abstract Missing'].reset_index()

#%%
"""

"""
import numpy as np
import re
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_sub(splits, sub):
  for idx, s in enumerate(splits):
      if sub.lower() in s.lower():
          return idx
  return None

sub = 'abstract'
cutoffratio = 0.08
library = NIPS

regex = re.compile(r"\s*{0}\s*".format(sub), flags=re.I) #define regex to find sub
similarities = [None] * len(library)
abstracts = [None] * len(library)
no_abstracts = []
cutoff = []

for i in library.iterrows():
    text = i[1]["paper_text"]
    abstract_real = i[1]["abstract"]
    splits = [x + ".\n" for x in text.split(".\n")]
    index = find_sub(splits, sub)
    if index == None: # if there was no match
        abstract = None
        similarity = np.nan
        no_abstracts.append(i[0])
    else: # if there was a match
        noproblem = True
        idx = index + 1
        abstract = regex.split(splits[index])[1].replace('\n', ' ') # find initial abstract
        while noproblem and idx < len(splits):
            extension = splits[idx].replace('\n', ' ')
            check_intro = extension.split()
            for w in check_intro[0:5]:
                if '1' in w:
                    noproblem = False
                if 'introduction' in w.lower(): # check if we arrived at the introduction paragraph
                    noproblem = False
            if noproblem and (len(abstract + extension)/len(text) > cutoffratio):
                noproblem = False
                cutoff.append(i[0])
            if noproblem:
                abstract = abstract + extension
            idx = idx + 1
        similarity = similar(abstract_real, abstract)
    similarities[i[0]] = similarity
    abstracts[i[0]] = abstract
    
print("Number of papers cut off: " + str(len(cutoff)))
print("Number of abstracts not found: " +str(len(no_abstracts)))
#%%
""" 
------------------------
     Average similarity
------------------------
"""
similarities_cutoff = [similarities[i] for i in cutoff]
similarities_nocutoff = [similarities[i] for i in np.delete(range(0,len(similarities)), cutoff, 0)]

print("Average similarity: " + str(np.nanmean(similarities)))
print("Average similarity (no cutoff): " + str(np.nanmean(similarities_nocutoff)))
print("Average similarity (only cutoff): " + str(np.nanmean(similarities_cutoff)))

#%%
""" 
------------------------
     Ratio analysis
------------------------
"""
ratio_abstxt = [None] * len(NIPS_abstr)
ratios_genabstxt = [None] * len(NIPS_abstr)
text_lengths = [None] * len(NIPS_abstr)
abstract_lengths = [None] * len(NIPS_abstr)

for i in NIPS_abstr.iterrows():
    text = len(i[1]["paper_text"].replace('\n', ' '))
    abstract_real = len(i[1]["abstract"].replace('\n', ' '))
    ratio_abstxt[i[0]] = abstract_real/text
    abstract = abstracts[i[0]]
    if abstract == None:
        ratios_genabstxt[i[0]] = None
    else:
        ratios_genabstxt[i[0]] = len(abstract)/text
    text_lengths[i[0]] = text
    abstract_lengths[i[0]] = abstract_real

NIPS_abstr["ratio"] = ratio_abstxt
NIPS_abstr["ratio gen"] = ratios_genabstxt
NIPS_abstr["text length"] = text_lengths
NIPS_abstr["abstract length"] = abstract_lengths

eventgroups = NIPS_abstr.groupby('event_type')
means = eventgroups.mean()
stds = eventgroups.std()
medians =  eventgroups.median()
mins =  eventgroups.min()
maxs =  eventgroups.max()

print('\n mean:')
print(means[['ratio', 'ratio gen', 'text length', 'abstract length']])
print('\n standard deviation:')
print(stds[['ratio', 'ratio gen', 'text length', 'abstract length']])
print('\n median:')
print(medians[['ratio', 'ratio gen', 'text length', 'abstract length']])
print('\n min:')
print(mins[['ratio', 'ratio gen', 'text length', 'abstract length']])
print('\n max:')
print(maxs[['ratio', 'ratio gen', 'text length', 'abstract length']])

#%%
"""
------------------------
     Conclusions
------------------------

Conclusions of the heuristic approach
* DATA CLEANING
  Smaller text lengths can indicate that the parsing of a text is not valid;
  -> filter papers for which text < 1000 or even 3500
  
* CUT OFF RATIO
  Maximum real_abstract/text ratio < 1 is 0.40, second max is 0.072, average/median is 0.03
  -> cut off ratio at most 0.10 
          CO 0.10
          Average similarity: 0.870471151441
          Average similarity (no cutoff): 0.875457993394
          Average similarity (only cutoff): 0.371786956166
          # cutoffs: 32
          
          CO 0.08
          Average similarity: 0.871522097687
          Average similarity (no cutoff): 0.877210062901
          Average similarity (only cutoff): 0.449686724008
          # cutoffs: 43
          -> manual inspection shows that for these papers it is indeed hard 
          to find the abstract i.e. no new paragraph at all;
          
          CO 0.05
          Average similarity: 0.872464491635
          Average similarity (no cutoff): 0.878238445146
          Average similarity (only cutoff): 0.582025465004
          # cutoffs: 105
          
          CO 0.03
          Average similarity: 0.814610841166
          Average similarity (no cutoff): 0.879015974083
          Average similarity (only cutoff): 0.57733859787
          # cutoffs: 690
          
          CO 0.01
          Average similarity: 0.75792445607
          Average similarity (no cutoff): 0.881125221434
          Average similarity (only cutoff): 0.539041996643
          # cutoffs: 1164
          
* There does not seem to be a difference wrt text length and abstract/text
  ratio between different event types. only standard deviation of poster is higher
  but there is one outlier in this case. So this information cannot be used to 
  improve the cutoff ratio; 
* We can fairly accurate determine the abstract; especially if we do not have to use a cutoff

"""