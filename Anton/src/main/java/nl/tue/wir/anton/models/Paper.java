package nl.tue.wir.anton.models;

import java.util.List;

public class Paper extends QueryResultParent {
    private String title;
    private String paperAbstract;
    private String paperBody;
    private List<String> authors;

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

    public void setAuthors(List<String> authors) {
        this.authors = authors;
    }

    @Override
    public String getType() {
        return "paper";
    }
}
