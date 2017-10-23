package nl.tue.wir.anton.models;

import java.util.List;

public class Topic extends QueryResultParent {
    private int id;
    private String name;
    private List<String> keywords;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<String> getKeywords() {
        return keywords;
    }

    public void setKeywords(List<String> keywords) {
        this.keywords = keywords;
    }

    @Override
    public String getType() {
        return "topic";
    }
}
