*************PageRank.csv*****************************
ID
Pagerank score
Overall PageRank rank / auteur

created in PageRankInclAgeExclusivity.py

*************pageRankOverallAndTopics.csv*************
ID				= author ID
Overall PageRank score and rank	= score and rank based on PageRank score over complete co-authorgraph
PageRank rank/topic/author score and rank
	For each topic, PageRank scores are computed using only papers that score higher
	on a certain topic than the threshold determined in the Topic Model.
	All authors are still used in the co-author graph (so not only the authors related to
	the papers that are related to the topic). Therefore, a lot of authors are isolates in the
	co-author graph of the topic. These authors get a very low PageRank score.	
	Voor de topics, de PageRank scores zijn berekend alleen gebruikmakend van papers die hoger
	scoren op een bepaald topic dan een bepaalde threshold die Bart heeft bepaald.

The topics that are considered irrelevant in the topic inspection, are excluded.

*************PaperPageRank.csv***********************
ID		= paper ID
PageRank  	= PageRankscore of paper
		Calculated by 0.85*(average PageRank score of all contributed authors)+0.15*(PageRank score over
			citation graph).
PageRank rank	= rank based on PageRank score

created in PageRankPapers.py

*************author-info-scopus2.csv*****************
In this file, the author info retrieved from the ELSEVIER API is stored.

Created in retrieve scopus info.py
		