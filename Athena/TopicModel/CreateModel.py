from __future__ import print_function
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import pandas as pd
import os


os.chdir('C:/Courses/2017Q1/NIPS-papers/')

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

# add common words to stopwords
common_words = []
common_words.append('learn')
common_words.append('use')
common_words.append('data')
common_words.append('set')
common_words.append('can')
common_words.append('one')
common_words.append('gener')

filepath = 'original/papers.csv'
papers = pd.read_csv(filepath, engine='python')
paper_topic = papers[['id', 'paper_text']]
paper_topic["tokenized_text"] = ""
paper_topic["document_term"] = ""
paper_topic["topics"] = ""

# loop through document list
for i , paper in paper_topic.iterrows():
    # clean and tokenize document string
    T = paper[1]
    raw = T.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [T for T in tokens if not T in en_stop]
    stemmed_tokens = [p_stemmer.stem(T) for T in stopped_tokens]
    no_common_words = [T for T in stemmed_tokens if not T in common_words]
    no_single_characters = [T for T in no_common_words if not len(T)== 1]
    no_numbers = [T for T in no_single_characters if not T.isnumeric()]
    paper_topic.set_value(i,'tokenized_text', no_numbers)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(paper_topic['tokenized_text'].values.tolist())
    
# convert tokenized documents into a document-term matrix
for i , paper in paper_topic.iterrows():
    paper_topic.set_value(i,'document_term', dictionary.doc2bow(paper[2]))
corpus = paper_topic['document_term'].values.tolist()

# generate LDA model
model = models.LdaModel(corpus, id2word=dictionary, alpha='auto', num_topics=20, passes=1) 
model.save('TitleModel.lda')
print('model saved')

#%% Save data to csv
paper_topic.to_csv('paper_topic.csv')

#%% Fill assign topics to papers
for i, paper in paper_topic.iterrows():
    assignedtopics = model[paper[3]]
    assignedtopics = [T for T in assignedtopics if T[1]>0.2 and T[0] not in [2,4,8,11,12]]
    paper_topic.set_value(i,'topics', assignedtopics)

#%% Save data to csv
paper_topic.to_csv('paper_topic.csv')
paperid_topic = paper_topic[['id', 'topics']]
paperid_topic.to_csv('paperid_topic.csv')

#%% create topic dataframe
topics = pd.DataFrame(index=range(model.num_topics),columns=['topicname','keywords','occurence','occurence_yearly'])
topicnums = []
for topicnum in range(model.num_topics):
    topics.set_value(topicnum,'keywords', model.show_topic(topicnum,30))
    topics.set_value(topicnum,'topicname', ("topic "+str(topicnum)))
    topics.set_value(topicnum,'occurence', 0)

topics.set_value(0,'topicname', ("Brain-Computer-Interfaces"))
topics.set_value(1,'topicname', ("Boosting"))
topics.set_value(2,'topicname', ("topic 2"))
topics.set_value(3,'topicname', ("Probabilistic Methods"))
topics.set_value(4,'topicname', ("topic 4"))
topics.set_value(5,'topicname', ("Metric Learning"))
topics.set_value(6,'topicname', ("Bandit Problems"))
topics.set_value(7,'topicname', ("Motor Control"))
topics.set_value(8,'topicname', ("topic 8"))
topics.set_value(9,'topicname', ("Visual Applications"))
topics.set_value(10,'topicname', ("Components Analysis and Sparsity"))
topics.set_value(11,'topicname', ("topic 11"))
topics.set_value(12,'topicname', ("topic 12"))
topics.set_value(13,'topicname', ("Neural Networks"))
topics.set_value(14,'topicname', ("Speech and Letter Recognition"))
topics.set_value(15,'topicname', ("Lifted Inference Models"))
topics.set_value(16,'topicname', ("Dimensionality Reduction and Manifold Learning"))
topics.set_value(17,'topicname', ("Motion and Tracking"))
topics.set_value(18,'topicname', ("Deep Learning"))
topics.set_value(19,'topicname', ("Gaussian Processes"))

#%% count total topic occurence
for i, paper in paperid_topic.iterrows():
    assignedtopics = paper[1]
    for assignedtopic in assignedtopics:
        topicnum = assignedtopic[0]
        occurence = topics.get_value(topicnum, 'occurence')
        topics.set_value(topicnum,'occurence', (occurence+1))

#%% add year to dataframe
paperid_topic = pd.concat([paperid_topic, papers[['year']]], axis=1, join='inner')
#%% count topic occurence per year
firstyear = min(paperid_topic['year'].values.tolist())
lastyear =  max(paperid_topic['year'].values.tolist())
yearlist = []

for year in range(firstyear,lastyear+1):
    yearlist.append([year,0])

topics['occurence_yearly'] = topics['occurence_yearly'].astype(object)
for i, topic in topics.iterrows():
    topics.loc[i,'occurence_yearly'] = yearlist[:]

#%%
for i, paper in paperid_topic.iterrows():
    assignedtopics = paper[1]
    paperyear = paper[2]
    for assignedtopic in assignedtopics:
        topicnum = assignedtopic[0]
        occurence_yearly = topics.get_value(topicnum, 'occurence_yearly')[:]
        yearid = -1
        for index, year in enumerate(occurence_yearly):
            if paperyear == year[0]:
                yearid = index
        yeardata = occurence_yearly[yearid][:]
        yeardata[1] = yeardata[1] + 1
        occurence_yearly[yearid] = yeardata
        topics.set_value(topicnum,'occurence_yearly', occurence_yearly)

#%% remove empty topics
topics.insert(loc=0, column='id', value=topics.index.values.tolist())
droplist = []
for i, topic in topics.iterrows():
    if topic[3] == 0:
        droplist.append(i)
topics = topics.drop(topics.index[droplist])

#%% Save data to csv
topics.to_csv('topics.csv')

#%% open new authors and new authors papers
new_paper_authors = pd.read_csv('new_paper_authors.csv', engine='python')

#%% create index
paperid_topic = paperid_topic.set_index('id')
#%% concat dataframes
paper_authors_topics = new_paper_authors.join(paperid_topic, on=['paper_id'], how='inner')
#%% open csv of authors
new_authors = pd.read_csv('new_authors.csv', engine='python')
new_authors = new_authors.drop('name', 1)
new_authors["topics"] = ''
#%% count topics
from collections import Counter

for index, author in new_authors.iterrows():
    topics = []
#    print(author[0])
    for i, paper in paper_authors_topics.iterrows():
        if paper[1] == author[0]:
            for topic in paper[2]:
                topics.append(topic[0])
    distinct = Counter(topics)
    distinct = distinct.most_common()
    new_authors.set_value(index,'topics',distinct)
new_authors.to_csv('authortopic.csv')
print('saved')
#%% Save data to csv
new_authors.to_csv('authortopic.csv')