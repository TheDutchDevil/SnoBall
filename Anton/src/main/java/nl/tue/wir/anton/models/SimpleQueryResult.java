package nl.tue.wir.anton.models;

import java.util.List;

public class SimpleQueryResult {

    private List<Object> items;

    public SimpleQueryResult(List<Object> items) {
        this.items = items;
    }

    public List<Object> getItems() {
        return items;
    }
}
