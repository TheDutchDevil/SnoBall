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
papers = paperAuthorOriginal = pd.read_csv('new_paper_authors.csv')
authors = pd.read_csv('new_authors.csv')
authorList = authors['id'].tolist()

""" set working directory such that the updated author and author_paper table are retrieved"""
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Athena\References\ '
os.chdir(working_dir)

"""import files"""
citationGraph= pd.read_csv("citation_graph.csv", engine='python')

#%%
"Calculate PageRank over coauthor graph"
alpha = 0.15 #age parameter
year = datetime.datetime.now().year
age = [None] * len(papers)
weight = [None] * len(papers)
for n in range(0,(len(papers))):
    age[n] = year - papers.year[n]
    weight[n] = math.exp(-alpha*age[n])
papers['weight'] = weight

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

paperPageRankDf = paperPageRankDf.sort_values(by = 'coauthorPRscore', ascending = False)
paperPageRankDf['coauthorPRrank'] = list(range(1,len(paperPageRankDf)+1))

#%%
"""PageRank over citationgraph"""
edgeList = citationGraph.values.tolist()

papersList = papers['id'].tolist()
citationDG = nx.DiGraph()
citationDG.add_nodes_from(papersList)


alpha = 0.15 #age parameter
year = datetime.datetime.now().year
age = [None] * len(papers)
weight = [None] * len(papers)
for n in range(0,(len(papers))):
    age[n] = year - papers.year[n]
    weight[n] = math.exp(-alpha*age[n])
papers['weight'] = weight

weightedEdgeList = []
for item in edgeList:
    weight = papers[papers['id']==item[0]].weight.tolist()[0]
    weightedEdgeList.append((item[0], item[1], weight))

citationDG.add_weighted_edges_from(weightedEdgeList)
pageRankDict = nx.pagerank(citationDG)
PRScore = [None] * len(paperPageRankDf)
for index, row in paperPageRankDf.iterrows():
    PRScore[index] = pageRankDict.get(paperPageRankDf.loc[index, 'paper_id'])
   
paperPageRankDf['citationPRscore'] = PRScore

paperPageRankDf = paperPageRankDf.sort_values(by = 'citationPRscore', ascending = False)
paperPageRankDf['citationPRrank'] = list(range(1,len(paperPageRankDf)+1))

#%%
"""calculate correlation"""
coauthorPRScore = paperPageRankDf['coauthorPRscore'].tolist()   
