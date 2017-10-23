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
import ast

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

def topicPageRank(topicNum, authorLst, paperAuthorDf, firstYear, lastYear):
    """Match list of papers with paper_author table"""
    currentTopic = topicList[topicNum]
    paperAuthorDfTopic=paperAuthorDf[paperAuthorDf['paper_id'].isin(currentTopic)]   
    """Calculate PageRank for authors over each topic"""
    return pageRank(authorList, paperAuthorDfTopic, firstYear, lastYear)


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


authors['PageRankScore'] = pageRank(authorList, paperAuthorDf, 1987, 2016)

#%% 
" PAGERANK VOOR TOPICS"
paperTopic = pd.DataFrame.from_csv(r'C:\Users\s134277\Documents\GitHub\SnoBall\Athena\TopicModel\paperid_topic.csv')

" Create a list with an empty list for each topic "
topicList = []
num_topics = 20
for i in range(num_topics):
    topicList.append([])    
        
"""Fill the empty topic lists with paper id's associated with that topic"""
for i, paper in paperTopic.iterrows():
    assignedtopics = ast.literal_eval(paper[1]) #literal_eval because list was retrieved as string from csv
    for assignedtopic in assignedtopics:
        topicnum = assignedtopic[0]
        topicList[topicnum].append(paper.id)
      
""" Add PageRank score per topic """
for i in range(num_topics):
    string = "T"+str(i)+"PRScore"
    authors[string] = topicPageRank(i, authorList, paperAuthorDf, 1987, 2016)
#%%
""""Add ranking based on PageRank score"""
def addRank (authorsTable, rankedBy, namecolumn):
    authorsTable = authorsTable.sort_values(by = rankedBy, ascending = False)
    authorsTable[namecolumn] = list(range(1,len(authorsTable)+1))
    return authorsTable

authors = addRank(authors, 'PageRankScore', 'PageRankRank')
for i in range(num_topics):
    stringScore = "T"+str(i)+"PRScore"
    stringRank = "T"+str(i)+"PRRank"
    authors = addRank(authors, stringScore, stringRank)

authors = authors.sort_values(by = 'PageRankScore', ascending = False)

#%%
""" save to file """
working_dir = r'C:\Users\s134277\Documents\GitHub\SnoBall\Athena\PageRank\ '
os.chdir(working_dir)
overallPageRank = authors[['id', 'PageRankScore','PageRankRank']]
overallPageRank.to_csv('PageRank.csv', index = False)

topicRankList = []
topicScoreList = []
for i in range(num_topics):
    if i not in (2, 4, 8, 11, 12):
        stringScore = "T"+str(i)+"PRScore"
        stringRank = "T"+str(i)+"PRRank"
        topicRankList.append(stringRank)
        topicScoreList.append(stringScore)
columnList = ['id', 'PageRankScore'] + topicScoreList + ['PageRankRank'] + topicRankList

pageRankOverallAndTopics = authors[columnList] 

pageRankOverallAndTopics.to_csv('PageRankOverallAndTopics.csv', index = False)