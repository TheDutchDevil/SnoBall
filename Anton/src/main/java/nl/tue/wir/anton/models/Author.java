package nl.tue.wir.anton.models;

public class Author extends QueryResultParent {

    private String name;
    private String alternativeNames;
    private int id;
    private int rank;
    private double score;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

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

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }
}
