*************PageRank.csv*****************************
ID
Overall PageRank rank / auteur

*************pageRankOverallAndTopics.csv*************
ID
Overall PageRank rank/auteur
PageRank rank/topic/auteur
	Voor de topics, de PageRank scores zijn berekend alleen gebruikmakend van papers die hoger
	scoren op een bepaald topic dan een bepaalde threshold die Bart heeft bepaald.
	Alle auteurs zijn gebruikt (dus niet alleen de auteurs die bij die papers horen).
	Hierdoor zijn er dus steeds een aantal nodes (auteurs) in de graph die geen edges (samenwerkingsverbanden)
	hebben. Hierdoor krijgen deze auteurs een superlage score (maar dus wel een score hoger dan 0)
	Dus een auteur heeft op ieder topic een score en dus een rank.

*************PaperPageRank.csv***********************
ID
Overall PageRank score
		Bepaald door het gemiddelde te nemen over alle auteurs die hebben samengewerkt aan die paper
		