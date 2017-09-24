package nl.tue.wir.anton.models;

public class RequestResult {
    private boolean result;
    private String message;

    private RequestResult(boolean result, String message) {
        this.result = result;
        this.message = message;
    }

    public boolean isResult() {
        return result;
    }

    public String getMessage() {
        return message;
    }

    public static RequestResult failedResult(String message) {
        return new RequestResult(false, message);
    }

    public static RequestResult succeededResult() {
        return new RequestResult(true, null);
    }
}
