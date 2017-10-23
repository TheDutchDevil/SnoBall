package nl.tue.wir.anton.documentstore;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.LeafReaderContext;
import org.apache.lucene.queries.CustomScoreProvider;

import java.io.IOException;

public class TopicBoosterScoreProvider extends CustomScoreProvider {

    public TopicBoosterScoreProvider(LeafReaderContext context) {
        super(context);
    }



    public float customScore(int docId, float subQueryScore, float valSrcScores[]) throws IOException
    {
        IndexReader r = context.reader();

        Document doc = r.document(docId);

        float score = subQueryScore;

        if(doc.get("type").equals("topic")) {

            score = score * 1.9f;

            System.out.println("Topic " + doc.get("name") + " in query results with score: " + subQueryScore + " boosted to: " + score);
        }

        return score;
    }
}
