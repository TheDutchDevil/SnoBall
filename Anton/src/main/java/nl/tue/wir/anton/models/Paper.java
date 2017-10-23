package nl.tue.wir.anton.models;

import java.util.List;

public class Paper extends QueryResultParent {
    private String title;
    private String paperAbstract;
    private String gen_abstract;
    private String paperBody;
    private List<Author> authors;
    private int id;
    private int rank;
    private double score;
    private int year;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getPaperAbstract() {
        return paperAbstract;
    }

    public void setPaperAbstract(String paperAbstract) {
        this.paperAbstract = paperAbstract;
    }

    public String getPaperBody() {
        return paperBody;
    }

    public void setPaperBody(String paperBody) {
        this.paperBody = paperBody;
    }

    public List<Author> getAuthors() {
        return authors;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setAuthors(List<Author> authors) {
        this.authors = authors;
    }

    public String getGen_abstract() {
        return gen_abstract;
    }

    public void setGen_abstract(String gen_abstract) {
        this.gen_abstract = gen_abstract;
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

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    @Override
    public String getType() {
        return "paper";
    }
}
