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

@Path("papers")
public class Insert {

    private static Genson genson = new Genson();

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public String putPaper(@NotNull Paper paper) {

        if(paper.getTitle() == null) {
             return genson.serialize(RequestResult.failedResult("Title missing"));
        }

        if(paper.getPaperBody() == null) {
            return genson.serialize(RequestResult.failedResult("Paper body missing"));
        }

        if(paper.getAuthors() == null || paper.getAuthors().size() == 0) {
            return genson.serialize(RequestResult.failedResult("Authors missing"));
        }

        if(paper.getGen_abstract() == null) {
            return genson.serialize(RequestResult.failedResult("gen_abstract missing"));
        }

        System.out.println("Indexing: " + paper.getTitle());

        AntonIndexWriter writer = new AntonIndexWriter();

        writer.indexPaper(paper);

        return genson.serialize(RequestResult.succeededResult());
    }


}
