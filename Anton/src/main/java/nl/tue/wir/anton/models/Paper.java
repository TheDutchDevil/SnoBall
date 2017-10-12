package nl.tue.wir.anton.models;

import java.util.List;

public class Paper extends QueryResultParent {
    private String title;
    private String paperAbstract;
    private String gen_abstract;
    private String paperBody;
    private List<String> authors;
    private int id;

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

    public List<String> getAuthors() {
        return authors;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setAuthors(List<String> authors) {
        this.authors = authors;
    }

    public String getGen_abstract() {
        return gen_abstract;
    }

    public void setGen_abstract(String gen_abstract) {
        this.gen_abstract = gen_abstract;
    }


    @Override
    public String getType() {
        return "paper";
    }
}
