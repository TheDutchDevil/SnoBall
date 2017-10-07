package nl.tue.wir.anton.documentstore;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.SimpleFSDirectory;

import java.io.IOException;
import java.nio.file.Paths;

public class AntonIndexWriter {

    public final static String INDEX_NAME = "PAPER_INDEX";

    private final static Genson genson = new Genson();

    public void indexPaper(Paper paper) {

        try {

            FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            org.apache.lucene.index.IndexWriter indexWriter = new org.apache.lucene.index.IndexWriter(directory, config);


            Document doc = new Document();

            doc.add(new TextField("title", paper.getTitle(), Field.Store.YES));
            doc.add(new TextField("paperBody", paper.getPaperBody(), Field.Store.NO));

            doc.add(new StoredField("type", "paper"));

            doc.add(new StoredField("authors", genson.serialize(paper.getAuthors())));
            doc.add(new StoredField("id", paper.getId()));

            if(paper.getPaperAbstract() == null) {
                paper.setPaperAbstract("");
            }

            doc.add(new TextField("paperAbstract", paper.getPaperAbstract(), Field.Store.NO));


            indexWriter.addDocument(doc);

            indexWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void indexAuthor(Author author) {
        try {
            FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            org.apache.lucene.index.IndexWriter indexWriter = new org.apache.lucene.index.IndexWriter(directory, config);


            Document doc = new Document();

            doc.add(new TextField("name", author.getName(), Field.Store.YES));

            doc.add(new StoredField("type", "author"));
            doc.add(new StoredField("id", author.getId()));

            if(author.getAlternativeNames() != null) {
                doc.add(new TextField("alternativeNames", author.getAlternativeNames().replace(",", " "), Field.Store.YES));
            }

            indexWriter.addDocument(doc);

            indexWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}
