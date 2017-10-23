package nl.tue.wir.anton.documentstore;

import org.apache.lucene.index.LeafReaderContext;
import org.apache.lucene.queries.CustomScoreProvider;
import org.apache.lucene.queries.CustomScoreQuery;
import org.apache.lucene.queries.function.FunctionQuery;
import org.apache.lucene.search.Query;

import java.io.IOException;

public class PageRankScoreQuery extends CustomScoreQuery {
    public PageRankScoreQuery(Query subQuery) {
        super(subQuery);
    }

    public PageRankScoreQuery(Query subQuery, FunctionQuery scoringQuery) {
        super(subQuery, scoringQuery);
    }

    public PageRankScoreQuery(Query subQuery, FunctionQuery... scoringQueries) {
        super(subQuery, scoringQueries);
    }

    @Override
    protected CustomScoreProvider getCustomScoreProvider(LeafReaderContext context) throws IOException {
        return new PageRankScoreProvider(context);
    }
}
