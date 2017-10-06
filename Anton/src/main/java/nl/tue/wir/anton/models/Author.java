package nl.tue.wir.anton.models;

public class Author extends QueryResultParent {

    private String name;
    private String alternativeNames;

    public Author() {

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAlternativeNames() {
        return alternativeNames;
    }

    public void setAlternativeNames(String alternativeNames) {
        this.alternativeNames = alternativeNames;
    }

    public String getType() {
        return "author";
    }
}
