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
model = models.LdaModel(corpus, id2word=dictionary, alpha='auto', num_topics=10, passes=1) 
model.save('TitleModel.lda')
print('model saved')

#%% Save data to csv
paper_topic.to_csv('paper_topic.csv')

#%% Fill assign topics to papers
for i, paper in paper_topic.iterrows():
    assignedtopics = model[paper[3]]
    assignedtopics = [T for T in assignedtopics if T[1]>0.2]
    paper_topic.set_value(i,'topics', assignedtopics)

#%% Save data to csv
paper_topic.to_csv('paper_topic.csv')
paperid_topic = paper_topic[['id', 'topics']]
paperid_topic.to_csv('paperid_topic.csv')

#%% create topic dataframe
topics = pd.DataFrame(index=range(model.num_topics),columns=['topicname','keywords','occurence','occurence_yearly'])
topicnums = []
for topicnum in range(model.num_topics):
    topics.set_value(topicnum,'keywords', model.show_topic(topicnum,15))
    topics.set_value(topicnum,'topicname', ("topic "+str(topicnum)))
    topics.set_value(topicnum,'occurence', 0)

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
#    topics.set_value(i,'occurence_yearly', yearlist)
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
#%% Save data to csv
topics.to_csv('topics.csv')
