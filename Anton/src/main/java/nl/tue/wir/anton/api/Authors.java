package nl.tue.wir.anton.api;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.documentstore.AntonIndexWriter;
import nl.tue.wir.anton.models.Author;
import nl.tue.wir.anton.models.RequestResult;

import javax.validation.constraints.NotNull;
import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.util.List;

@Path("authors")
public class Authors {

    private static Genson genson = new Genson();

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putAuthor(@NotNull Author author) {

        if(author.getName() == null) {
            return genson.serialize(RequestResult.failedResult("Name missing"));
        }

        AntonIndexWriter writer = new AntonIndexWriter();

        writer.indexAuthor(author);

        return genson.serialize(RequestResult.succeededResult());
    }

    @PUT
    @Path("many")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putAuthor(@NotNull List<Author> authors) {

        AntonIndexWriter writer = new AntonIndexWriter();

        for(Author author : authors) {
            if (author.getName() == null) {
                return genson.serialize(RequestResult.failedResult("Name missing"));
            }

            System.out.println("Indexing: " + author.getName());

            writer.indexAuthor(author);
        }

        return genson.serialize(RequestResult.succeededResult());
    }
}