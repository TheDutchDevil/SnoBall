package nl.tue.wir.anton.models;

import java.util.List;

public class SimpleQueryResult {

    private List<Paper> papers;

    public SimpleQueryResult(List<Paper> papers) {
        this.papers = papers;
    }

    public List<Paper> getPapers() {
        return papers;
    }
}
