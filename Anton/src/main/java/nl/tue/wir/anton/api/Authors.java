package nl.tue.wir.anton.api;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.documentstore.AntonIndexWriter;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.Paper;
import nl.tue.wir.anton.models.RequestResult;

import javax.validation.constraints.NotNull;
import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Path("authors")
public class Authors {

    private static Genson genson = new Genson();

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putAuthor(@NotNull Author author) throws IOException {

        if(author.getName() == null) {
            return genson.serialize(RequestResult.failedResult("Name missing"));
        }

        try(AntonIndexWriter writer = new AntonIndexWriter()) {

            writer.indexAuthor(author);
        }

        return genson.serialize(RequestResult.succeededResult());
    }

    @PUT
    @Path("many")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putAuthor(@NotNull List<Author> authors) throws IOException, InterruptedException {

        try(final AntonIndexWriter writer = new AntonIndexWriter()) {

            for (Author author : authors) {
                if (author.getName() == null) {
                    return genson.serialize(RequestResult.failedResult("Name missing"));
                }
            }

            List<Thread> threads = new ArrayList<>();

            for (final List<Author> authorPart : partition(4, authors)) {
                Thread thread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        for (Author author : authorPart) {
                            System.out.println("Indexing: " + author.getName());

                            writer.indexAuthor(author);
                        }
                    }
                });

                thread.start();

                threads.add(thread);
            }

            for (Thread thread : threads) {
                thread.join();
            }
        }

        return genson.serialize(RequestResult.succeededResult());
    }

    private List<List<Author>> partition(int cores, List<Author> papers) {
        int partitionSize = (papers.size() / cores) + 1;
        List<List<Author>> partitions = new ArrayList<>();
        for (int i = 0; i < papers.size(); i += partitionSize) {
            partitions.add(papers.subList(i,
                    Math.min(i + partitionSize, papers.size())));
        }

        return partitions;
    }
}