package nl.tue.wir.anton.documentstore;

import nl.tue.wir.anton.models.Paper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.SimpleFSDirectory;

import java.io.IOException;
import java.nio.file.Paths;

public class PaperWriter {

    public final static String INDEX_NAME = "PAPER_INDEX";

    public void indexPaper(Paper paper) {

        try {

            FSDirectory directory = new SimpleFSDirectory(Paths.get(INDEX_NAME));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            IndexWriter indexWriter = new IndexWriter(directory, config);


            Document doc = new Document();

            doc.add(new TextField("title", paper.getTitle(), Field.Store.YES));
            doc.add(new TextField("paperBody", paper.getPaperBody(), Field.Store.YES));

            if(paper.getPaperAbstract() == null) {
                paper.setPaperAbstract("");
            }

            doc.add(new TextField("paperAbstract", paper.getPaperAbstract(), Field.Store.YES));


            indexWriter.addDocument(doc);

            indexWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}
