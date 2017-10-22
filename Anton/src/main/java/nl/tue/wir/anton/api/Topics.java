package nl.tue.wir.anton.api;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.documentstore.AntonIndexWriter;
import nl.tue.wir.anton.models.RequestResult;
import nl.tue.wir.anton.models.SimpleQueryResult;
import nl.tue.wir.anton.models.Topic;

import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.io.IOException;
import java.util.List;

@Path("/topics")
public class Topics {

    private static Genson genson = new Genson();

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public static String putPapers(List<Topic> topics) throws IOException {
        try(AntonIndexWriter writer = new AntonIndexWriter()) {

            for (Topic topic : topics) {
                if (topic.getName() == null) {
                    return genson.serialize(RequestResult.failedResult("no name"));
                }
                if (topic.getKeywords() == null) {
                    return genson.serialize(RequestResult.failedResult("no keywords"));
                }

                System.out.println("Indexing: " + topic.getName());

                writer.indexTopic(topic);
            }
        }

        return genson.serialize(RequestResult.succeededResult());
    }
}
