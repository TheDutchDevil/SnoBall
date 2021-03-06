package nl.tue.wir.anton.documentstore;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import nl.tue.wir.anton.models.Topic;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.SimpleFSDirectory;

import java.io.IOException;
import java.nio.file.Paths;

public class AntonIndexWriter implements AutoCloseable{

    public final static String INDEX_NAME = "PAPER_INDEX";

    private final static Genson genson = new Genson();

    public void deleteAll() throws IOException {
        FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
        org.apache.lucene.index.IndexWriter indexWriter = new org.apache.lucene.index.IndexWriter(directory, config);

        indexWriter.deleteAll();
    }

    private final IndexWriter indexWriter;

    public AntonIndexWriter() throws IOException {


        FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());

        config.setRAMBufferSizeMB(2000);

         indexWriter = new org.apache.lucene.index.IndexWriter(directory, config);

    }

    public void indexPaper(Paper paper) {

        try {

            Document doc = new Document();

            doc.add(new TextField("title", paper.getTitle(), Field.Store.YES));
            doc.add(new TextField("paperBody", paper.getPaperBody(), Field.Store.NO));
            doc.add(new TextField("gen_abstract", paper.getGen_abstract(), Field.Store.NO));

            doc.add(new StoredField("type", "paper"));

            doc.add(new StoredField("authors", genson.serialize(paper.getAuthors())));
            doc.add(new StoredField("id", paper.getId()));
            doc.add(new TextField("year", String.valueOf(paper.getYear()), Field.Store.YES));
            doc.add(new TextField("score", String.valueOf(paper.getScore()), Field.Store.YES));
            doc.add(new TextField("rank", String.valueOf(paper.getRank()), Field.Store.YES));

            if(paper.getPaperAbstract() == null) {
                paper.setPaperAbstract("");
            }

            doc.add(new TextField("paperAbstract", paper.getPaperAbstract(), Field.Store.NO));


            indexWriter.addDocument(doc);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public void indexAuthor(Author author) {
        try {


            Document doc = new Document();

            doc.add(new TextField("name", author.getName(), Field.Store.YES));

            doc.add(new StoredField("type", "author"));
            doc.add(new StoredField("id", author.getId()));
            doc.add(new TextField("score", String.valueOf(author.getScore()), Field.Store.YES));
            doc.add(new TextField("rank", String.valueOf(author.getRank()), Field.Store.YES));


            if(author.getAlternativeNames() != null) {
                doc.add(new TextField("alternativeNames", author.getAlternativeNames().replace(",", " "), Field.Store.YES));
            }

            indexWriter.addDocument(doc);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void indexTopic(Topic topic) {
        try {

            Document doc = new Document();

            doc.add(new TextField("name", topic.getName(), Field.Store.YES));

            for(String keyword : topic.getKeywords()) {
                doc.add(new TextField("keyword", keyword, Field.Store.NO));
            }
            doc.add(new StoredField("id", topic.getId()));
            doc.add(new StoredField("type", "topic"));
            doc.add(new StoredField("keywordList", genson.serialize(topic.getKeywords())));

            indexWriter.addDocument(doc);
        }
        catch(IOException ex) {
            ex.printStackTrace();
        }
    }

    @Override
    public void close() throws IOException {
        indexWriter.close();
    }


}
