package nl.tue.wir.anton.api;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import nl.tue.wir.anton.documentstore.AntonIndexWriter;
import nl.tue.wir.anton.models.RequestResult;

import javax.validation.constraints.NotNull;
import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

@Path("papers")
public class Insert {

    private static Genson genson = new Genson();

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putPaper(@NotNull Paper paper) throws IOException {

        if (paper.getTitle() == null) {
            return genson.serialize(RequestResult.failedResult("Title missing"));
        }

        if (paper.getPaperBody() == null) {
            return genson.serialize(RequestResult.failedResult("Paper body missing"));
        }

        if (paper.getAuthors() == null || paper.getAuthors().size() == 0) {
            return genson.serialize(RequestResult.failedResult("Authors missing"));
        }

        if (paper.getGen_abstract() == null) {
            return genson.serialize(RequestResult.failedResult("gen_abstract missing"));
        }

        System.out.println("Indexing: " + paper.getTitle());

        try (AntonIndexWriter writer = new AntonIndexWriter()) {

            writer.indexPaper(paper);
        }

        return genson.serialize(RequestResult.succeededResult());
    }

    @PUT
    @Path("many")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putPapers(@NotNull List<Paper> papers) throws IOException, InterruptedException {

        for (Paper paper : papers) {

            if (paper.getTitle() == null) {
                return genson.serialize(RequestResult.failedResult("Title missing"));
            }

            if (paper.getPaperBody() == null) {
                return genson.serialize(RequestResult.failedResult("Paper body missing"));
            }

            if (paper.getAuthors() == null) {
                return genson.serialize(RequestResult.failedResult("Authors missing"));
            }

            if (paper.getGen_abstract() == null) {
                return genson.serialize(RequestResult.failedResult("gen_abstract missing"));
            }
        }

        try (final AntonIndexWriter writer = new AntonIndexWriter()) {

            List<Thread> threads = new ArrayList<>();

            for (final List<Paper> papersPart : partition(Runtime.getRuntime().availableProcessors(), papers)) {
                Thread thread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        for (Paper paper : papersPart) {

                            System.out.println("Indexing: " + paper.getTitle());

                            writer.indexPaper(paper);

                        }
                    }
                });

                thread.run();
                threads.add(thread);

            }

            for (Thread thread : threads) {
                thread.join();
            }
        }

        return genson.serialize(RequestResult.succeededResult());
    }

    private List<List<Paper>> partition(int cores, List<Paper> papers) {
        int partitionSize = (papers.size() / cores) + 1;
        List<List<Paper>> partitions = new ArrayList<>();
        for (int i = 0; i < papers.size(); i += partitionSize) {
            partitions.add(papers.subList(i,
                    Math.min(i + partitionSize, papers.size())));
        }

        return partitions;
    }

}
