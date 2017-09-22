package nl.tue.wir.anton.api;

import nl.tue.wir.anton.api.models.Paper;

import javax.ws.rs.Consumes;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.core.MediaType;

@Path("papers")
public class Insert {

    @PUT
    @Consumes(MediaType.APPLICATION_JSON)
    public void putPaper(Paper paper) {
        System.out.println(paper.getTitle());
    }


}
