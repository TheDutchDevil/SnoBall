# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 07:49:56 2017

@author: s134277
"""
import pandas as pd
import networkx as nx
import datetime
import math
import numpy as np

import os


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
    allTimePR = nx.pagerank_scipy(multiG)
    PRScore = [None] * len(authors)
    for index, row in authors.iterrows():
        PRScore[index] = allTimePR.get(authors.loc[index, 'id'])
    return PRScore 

""" set working directory such that the updated author and author_paper table are retrieved"""
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Execute\Papers\ '
os.chdir(working_dir)

"""import files"""
papers = pd.read_csv("papers.csv", engine='python')
paperAuthorOriginal = pd.read_csv('new_paper_authors.csv')
authors = pd.read_csv('new_authors.csv')
authorList = authors['id'].tolist()

""" set working directory such that the updated author and author_paper table are retrieved"""
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Athena\References\ '
os.chdir(working_dir)

"""import files"""
citationGraph= pd.read_csv("citation_graph.csv", engine='python')


alpha = 0.15 #age parameter
year = datetime.datetime.now().year
age = [None] * len(papers)
weight = [None] * len(papers)
for n in range(0,(len(papers))):
    age[n] = year - papers.year[n]
    weight[n] = math.exp(-alpha*age[n])
papers['weight'] = weight

#%%
"Calculate PageRank over coauthor graph"
paperAuthorDf = paperAuthorOriginal.merge(papers[['id', 'year','weight']], left_on = 'paper_id', right_on = 'id', how = 'left')[['paper_id','author_id','year','weight']]

authorList = authors['id'].tolist()


authors['PageRankScore'] = pageRank(authorList, paperAuthorDf, 1987, 2016)

"""Calculate average PR per paper"""
paperPageRankLst = []
unique_papers=paperAuthorOriginal.paper_id.unique()

for paperNum in unique_papers:
    paperDf=paperAuthorOriginal[paperAuthorOriginal.paper_id==paperNum].author_id
    PRAuthorLst = []
    for i, author in paperDf.iteritems():
        PRAuthorLst.append(authors[authors['id']==author].PageRankScore.iloc[0])
    PRpaper = sum(PRAuthorLst)/len(PRAuthorLst)
    paperPageRankLst.append((paperNum, PRpaper))

    
""" save to file """   
paperPageRankDf = pd.DataFrame(paperPageRankLst, columns=['paper_id', 'coauthorPRscore'])

#%%
"""PageRank over citationgraph"""
edgeList = citationGraph.values.tolist()

papersList = papers['id'].tolist()
citationDG = nx.DiGraph()
citationDG.add_nodes_from(papersList)

weightedEdgeList = []
for item in edgeList:
#    weight = papers[papers['id']==item[0]].weight.tolist()[0]
    weight = 1
    weightedEdgeList.append((item[0], item[1], weight))

citationDG.add_weighted_edges_from(weightedEdgeList)
pageRankDict = nx.pagerank(citationDG)
PRScore = [None] * len(paperPageRankDf)
for index, row in paperPageRankDf.iterrows():
    PRScore[index] = pageRankDict.get(paperPageRankDf.loc[index, 'paper_id'])
   
paperPageRankDf['citationPRscore'] = PRScore

#%%
"""Combined"""
combScore = [0] * len(paperPageRankDf)
sumCoAuthorPR = sum(paperPageRankDf['coauthorPRscore'])

for index, row in paperPageRankDf.iterrows():
    combScore[index]= 0.85*(row['coauthorPRscore'])/sumCoAuthorPR+0.15*row['citationPRscore']
paperPageRankDf['combScore'] = combScore    

print(np.corrcoef(paperPageRankDf['coauthorPRscore'], paperPageRankDf['combScore']))
print(np.corrcoef(paperPageRankDf['citationPRscore'], paperPageRankDf['combScore']))

#%%
"""Add ranking and save to file """
paperPageRankDf = paperPageRankDf.sort_values(by = 'coauthorPRscore', ascending = False)
paperPageRankDf['coauthorPRrank'] = list(range(1,len(paperPageRankDf)+1))

paperPageRankDf = paperPageRankDf.sort_values(by = 'citationPRscore', ascending = False)
paperPageRankDf['citationPRrank'] = list(range(1,len(paperPageRankDf)+1))

paperPageRankDf = paperPageRankDf.sort_values(by = 'combScore', ascending = False)
paperPageRankDf['combRank'] = list(range(1,len(paperPageRankDf)+1))

columnList = ['paper_id', 'combScore', 'combRank']

paperPageRankFinal = paperPageRankDf[columnList]
paperPageRankFinal.to_csv('PaperPageRank.csv', index = False)


#%%
"""calculate correlation""" 
test = np.corrcoef(paperPageRankDf['coauthorPRscore'], paperPageRankDf['citationPRscore'])
np.std(paperPageRankDf['coauthorPRscore'])
np.std(paperPageRankDf['citationPRscore'])
np.mean(paperPageRankDf['coauthorPRscore'])
np.mean(paperPageRankDf['citationPRscore'])
sum(paperPageRankDf['coauthorPRscore'])
sum(paperPageRankDf['citationPRscore'])

#%%
"""Analysis of sparsity of citation graph"""
isolatesCitationDG = nx.isolates(citationDG) #3754
numberNodesCitationDG = nx.number_of_nodes(citationDG) #6560
portionIsolates = len(isolatesCitationDG)/numberNodesCitationDG #0.57

numIsolatesTop1000 = 0
for index, row in paperPageRankDf.iterrows():
    if (row['paper_id'] in isolatesCitationDG) and (row['coauthorPRrank']<=1000):
        numIsolatesTop1000 = numIsolatesTop1000 + 1

"""
in top 100: 36 authors are isolates
in top 500: 203 authors are isolates
in top 1000: 444 authors are isolates
"""    
