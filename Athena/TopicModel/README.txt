*************CreateModel.py*****************************
Script which preprocesses the data and creates the topic model. Within this script, all the csv files in this folder are created.

*************authortopics.csv*************
The following columns are present in this csv
empty
	which is the rowid
id
	which is the author id
topics
	Contains a list of tuples with topic id and the occurences for this topic

*************Paperid_topic.csv***********************
empty
	which is the rowid
id
	which is the paper id
topics
	Contains a list of tuples with topic id and the probabilatie that the paper is constructed by the topic

*************topics.csv***********************
empty
	which is the rowid
id
	which is the topic id
topicname
	which is a manual created topicname
keywords
	which is a list of keywords generated by the topic model
occurence
	which is the total count of papers with the topic assigned
occurence_yearly
	which is a list of tuples with year and occurence for this year

*************topics_titlewords.csv***********************
empty
	which is the rowid
id
	which is the topic id
topicname
	which is a manual created topicname
keywords
	which is a list of keywords manualy extracted from the 20 most related papers
occurence
	which is the total count of papers with the topic assigned
occurence_yearly
	which is a list of tuples with year and occurence for this year

*************topicnames.txt***********************
gives the manual created topicnames for the topic model with 10 and 20 topics

*************topicpapertitles.txt***********************
gives the 20 most related papers for every topic for the 20 topics topic model