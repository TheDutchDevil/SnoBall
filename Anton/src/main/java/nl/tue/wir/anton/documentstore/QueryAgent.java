package nl.tue.wir.anton.documentstore;

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
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.SimpleFSDirectory;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import static nl.tue.wir.anton.documentstore.PaperWriter.INDEX_NAME;

public class QueryAgent {

    public SimpleQueryResult simpleQuery(String query) {
        try {
            StandardAnalyzer analyzer = new StandardAnalyzer();

            FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            IndexWriter indexWriter = new IndexWriter(directory, config);

            IndexReader reader = DirectoryReader.open(indexWriter);
            IndexSearcher searcher = new IndexSearcher(reader);

            Query q = new MultiFieldQueryParser(new String[] {"title", "paperBody", "paperAbstract"}, analyzer).parse(query);

            TopDocs docs = searcher.search(q, 10);

            ScoreDoc hits[] = docs.scoreDocs;

            List<Paper> results  = new ArrayList<>();

            for(int i = 0; i< hits.length; i++) {
                Document doc = searcher.doc(hits[i].doc);

                Paper paper = new Paper();

                paper.setTitle(doc.get("title"));
                paper.setPaperAbstract(doc.get("paperAbstract"));
                paper.setPaperBody(doc.get("paperBody"));

                results.add(paper);
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
