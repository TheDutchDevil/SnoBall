package nl.tue.wir.anton.api;

import nl.tue.wir.anton.documentstore.AntonIndexWriter;

import javax.ws.rs.DELETE;
import javax.ws.rs.Path;
import java.io.IOException;

@Path("delete")
public class Delete {

    @DELETE
    public void deleteAll() throws IOException {
        try(AntonIndexWriter writ = new AntonIndexWriter()) {
            writ.deleteAll();
        }
    }
}
