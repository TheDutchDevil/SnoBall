package nl.tue.wir.anton.documentstore;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import nl.tue.wir.anton.models.SimpleQueryResult;
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
import java.util.List;

import static java.lang.Math.*;
import static nl.tue.wir.anton.documentstore.AntonIndexWriter.INDEX_NAME;

public class QueryAgent {

    private static final Genson genson = new Genson();

    public SimpleQueryResult simpleQuery(String query) {
        try {
            StandardAnalyzer analyzer = new StandardAnalyzer();

            FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            IndexWriter indexWriter = new IndexWriter(directory, config);

            IndexReader reader = DirectoryReader.open(indexWriter);
            IndexSearcher searcher = new IndexSearcher(reader);

            Query q = new MultiFieldQueryParser(new String[] {"title", "paperBody", "paperAbstract", "name", "alternativeNames"}, analyzer).parse(query);

            TotalHitCountCollector counter = new TotalHitCountCollector();

            searcher.search(q, counter);

            TopDocs docs = searcher.search(q, max(1, counter.getTotalHits()));

            ScoreDoc hits[] = docs.scoreDocs;

            List<Object> results  = new ArrayList<>();

            for(int i = 0; i< hits.length; i++) {
                Document doc = searcher.doc(hits[i].doc);

                if(doc.get("type").equals("paper")) {
                    Paper paper = new Paper();

                    paper.setAuthors(genson.deserialize(doc.get("authors"), List.class));

                    paper.setTitle(doc.get("title"));

                    results.add(paper);
                } else if(doc.get("type").equals("author")) {
                    Author author = new Author();

                    author.setName(doc.get("name"));

                    results.add(author);
                }
            }

            indexWriter.close();

            return new SimpleQueryResult(results);

        } catch(IOException ex) {
            ex.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return null;
    }
}
