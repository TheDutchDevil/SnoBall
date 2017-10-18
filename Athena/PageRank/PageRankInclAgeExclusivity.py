# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 07:49:56 2017

@author: s134277
"""
import pandas as pd
import networkx as nx
import datetime
import math

import os

""" set working directory such that the updated author and author_paper table are retrieved"""
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Execute\Papers\ '
os.chdir(working_dir)

"""import files"""
papers = pd.read_csv("papers.csv", engine='python')

alpha = 0.15 #age parameter
year = datetime.datetime.now().year
age = [None] * len(papers)
weight = [None] * len(papers)
for n in range(0,(len(papers))):
    age[n] = year - papers.year[n]
    weight[n] = math.exp(-alpha*age[n])
papers['weight'] = weight

paperAuthorOriginal = pd.read_csv('new_paper_authors.csv')
paperAuthorDf = paperAuthorOriginal.merge(papers[['id', 'year','weight']], left_on = 'paper_id', right_on = 'id', how = 'left')[['paper_id','author_id','year','weight']]

authors = pd.read_csv('new_authors.csv')
authorList = authors['id'].tolist()

def pageRank (authorLst, paperAuthorDf, firstYear, lastYear):
    paperAuthorTemp = paperAuthorDf[(paperAuthorDf['year']>=firstYear) & (paperAuthorDf['year']<=lastYear)]
    coAuthorsLst=[]                                     #empty list in which edges of CoAuthor graph will be saved
    unique_papers=paperAuthorTemp.paper_id.unique()
    
    for paperNum in unique_papers:                      #iterate over every paper
        paperDf=paperAuthorTemp[paperAuthorTemp.paper_id==paperNum]
        weight = paperDf.weight.iloc[0]/len(paperDf) #weight decreases linearly with amount of authors
        for n in range(0,(len(paperDf)-1)):             #iterate over every row, apart from the last one
            i=n+1
            j=1
            while i<len(paperDf):                       #make a row in coAuthors for every combination of row n with the rows underneath it
                coAuthorsLst.append((paperDf.author_id.iloc[n],paperDf.author_id.iloc[n+j], weight))
                i=i+1
                j=j+1

    """ create multigraph """
    multiG = nx.MultiGraph()
    multiG.add_nodes_from(authorLst)
    multiG.add_weighted_edges_from(coAuthorsLst)

    return nx.pagerank_scipy(multiG)


"""Add PageRank Score to author table"""
allTimePR = pageRank(authorList, paperAuthorDf, 1987, 2016)
PRScore = [None] * len(authors)
for index, row in authors.iterrows():
    PRScore[index] = allTimePR.get(authors.loc[index, 'id'])
authors['PageRankScore'] = PRScore

""""Add ranking based on PageRank score"""
authors = authors.sort_values(by = 'PageRankScore', ascending = False)
authors['PageRankRank'] = list(range(1,len(authors)+1))

working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Athena\PageRank\ '
os.chdir(working_dir)
overallPageRank = authors[['id', 'PageRankRank']]
overallPageRank.to_csv('PageRank.csv', index = False)
