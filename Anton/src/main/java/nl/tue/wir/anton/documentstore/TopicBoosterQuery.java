package nl.tue.wir.anton.documentstore;

import org.apache.lucene.index.LeafReaderContext;
import org.apache.lucene.queries.CustomScoreProvider;
import org.apache.lucene.queries.CustomScoreQuery;
import org.apache.lucene.queries.function.FunctionQuery;
import org.apache.lucene.search.Query;

import java.io.IOException;

public class TopicBoosterQuery extends CustomScoreQuery {
    public TopicBoosterQuery(Query subQuery) {
        super(subQuery);
    }

    public TopicBoosterQuery(Query subQuery, FunctionQuery scoringQuery) {
        super(subQuery, scoringQuery);
    }

    public TopicBoosterQuery(Query subQuery, FunctionQuery... scoringQueries) {
        super(subQuery, scoringQueries);
    }

    @Override
    protected CustomScoreProvider getCustomScoreProvider(LeafReaderContext context) throws IOException {
        return new TopicBoosterScoreProvider(context);
    }
}
