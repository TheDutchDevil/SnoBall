# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 07:49:56 2017

@author: s134277
"""

import pandas as pd
import os


""" set working directory such that the updated author and author_paper table are retrieved"""
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Execute\Papers\ '
os.chdir(working_dir)
authors = pd.read_csv('new_authors.csv')
paperAuthorOriginal = pd.read_csv('new_paper_authors.csv')
papers = pd.read_csv("papers.csv", engine='python')

paperAuthorDf = paperAuthorOriginal.merge(papers[['id', 'year']], left_on = 'paper_id', right_on = 'id', how = 'left')[['paper_id','author_id','year']]


lenAuthors = len(authors)

numArticles = [None] * lenAuthors
minYear = [None] * lenAuthors
maxYear = [None] * lenAuthors


for index, row in authors.iterrows():

    authorDf = paperAuthorDf[paperAuthorDf.author_id == row.id]
    numArticles[index] = len(authorDf)
    minYear[index] = int(min(authorDf.year))
    maxYear[index] = int(max(authorDf.year))

authors['numArticles'] = numArticles
authors['minYear'] = minYear
authors['maxYear'] = maxYear

authors.to_csv('new_authors.csv', index = False)
