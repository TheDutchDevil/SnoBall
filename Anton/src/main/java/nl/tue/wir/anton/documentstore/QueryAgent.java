package nl.tue.wir.anton.documentstore;

import com.owlike.genson.GenericType;
import com.owlike.genson.Genson;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import nl.tue.wir.anton.models.SimpleQueryResult;
import nl.tue.wir.anton.models.Topic;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.SimpleFSDirectory;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

import static java.lang.Math.*;
import static nl.tue.wir.anton.documentstore.AntonIndexWriter.INDEX_NAME;

public class QueryAgent implements AutoCloseable {

    private static final Genson genson = new Genson();

    private IndexWriter indexWriter;

    public QueryAgent() throws IOException {

        FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
        indexWriter = new IndexWriter(directory, config);
    }

    public SimpleQueryResult simpleQuery(String query) {
        try {

            StandardAnalyzer analyzer = new StandardAnalyzer();

            IndexReader reader = DirectoryReader.open(indexWriter);
            IndexSearcher searcher = new IndexSearcher(reader);

            System.out.println("Answering query: " + query);

            Query q = new MultiFieldQueryParser(new String[] {"title", "paperBody", "paperAbstract", "name",
                    "alternativeNames", "gen_abstract", "keyword", "score", "year", "rank"}, analyzer).parse(query);

            q = new TopicBoosterQuery(q);

            TotalHitCountCollector counter = new TotalHitCountCollector();

            searcher.search(q, counter);

            TopDocs docs = searcher.search(q, max(1, counter.getTotalHits()));

            ScoreDoc hits[] = docs.scoreDocs;

            ScoreDoc[] rerankedHits = new ScoreDoc[Math.min(40, hits.length)];

            for(int i = 0; i< Math.min(40, hits.length); i++) {

                Document doc = searcher.doc(hits[i].doc);

                if(!doc.get("type").equals("topic")) {
                    hits[i].score = hits[i].score;
                }
                rerankedHits[i] = hits[i];
            }

            Arrays.sort(rerankedHits, new Comparator<ScoreDoc>() {
                @Override
                public int compare(ScoreDoc o1, ScoreDoc o2) {
                    if(o1 == o2) {
                        return 0;
                    } if (o1 == null) {
                        return -1;
                    } if (o2 == null) {
                        return 1;
                    }
                    return new Float(o2.score).compareTo(new Float(o1.score));
                }
            });

            System.out.print("Top 20 results have scores: [");

            for(int i = 0; i< Math.min(20, rerankedHits.length); i++) {
                System.out.print(String.valueOf(rerankedHits[i].score) + (i == 19 ? "]" : ", "));
            }

            System.out.println();

            List<Object> results  = new ArrayList<>();

            for(int i = 0; i< rerankedHits.length; i++) {
                Document doc = searcher.doc(rerankedHits[i].doc);

                if(doc.get("type").equals("paper")) {
                    Paper paper = new Paper();

                    paper.setAuthors(genson.deserialize(doc.get("authors"), new GenericType<List<Author>>() {
                    }));

                    paper.setTitle(doc.get("title"));
                    paper.setId(Integer.parseInt(doc.get("id")));
                    paper.setYear(Integer.parseInt(doc.get("year")));
                    paper.setRank(Integer.parseInt(doc.get("rank")));

                    results.add(paper);
                } else if(doc.get("type").equals("author")) {
                    Author author = new Author();

                    author.setName(doc.get("name"));
                    author.setId(Integer.parseInt(doc.get("id")));

                    author.setRank(Integer.parseInt(doc.get("rank")));

                    results.add(author);
                } else if(doc.get("type").equals("topic")) {
                    Topic topic = new Topic();

                    topic.setId(Integer.parseInt(doc.get("id")));
                    topic.setName(doc.get("name"));

                    topic.setKeywords(genson.deserialize(doc.get("keywordList"), new GenericType<List<String>>() {
                    }));

                    results.add(topic);
                }
            }

            return new SimpleQueryResult(results);

        } catch(IOException ex) {
            ex.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    public void close() throws Exception {

        indexWriter.close();

    }
}
