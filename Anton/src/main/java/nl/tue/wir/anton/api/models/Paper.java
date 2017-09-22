package nl.tue.wir.anton.api.models;

public class Paper {
    private String title;
    private String paperAbstract;
    private String paperBody;

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
}
