package nl.tue.wir.anton.documentstore;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.LeafReaderContext;
import org.apache.lucene.queries.CustomScoreProvider;

import java.io.IOException;

public class PageRankScoreProvider extends CustomScoreProvider {

    public PageRankScoreProvider(LeafReaderContext context) {
        super(context);
    }



    public float customScore(int docId, float subQueryScore, float valSrcScores[]) throws IOException
    {
        IndexReader r = context.reader();

        Document doc = r.document(docId);

        float score = subQueryScore;

        return score;
    }
}
