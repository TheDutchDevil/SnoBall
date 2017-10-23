package nl.tue.wir.anton.api;

import com.owlike.genson.Genson;
import nl.tue.wir.anton.documentstore.QueryAgent;
import nl.tue.wir.anton.models.SimpleQueryResult;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.io.IOException;

@Path("queries")
public class Query {

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/simple/{query}")
    public String simpleQuery(@PathParam("query") String query) throws Exception {
        try(QueryAgent queryAgent = new QueryAgent()) {

            return new Genson().serialize(queryAgent.simpleQuery(query));
        }
    }
}
