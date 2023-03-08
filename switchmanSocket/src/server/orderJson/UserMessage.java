package server.orderJson;

public class UserMessage {
    public String idFrom;
    public String idTo;
    public String msg;

    UserMessage(String idFrom,String idTo, String msg) {
        this.idFrom = idFrom;
        this.idTo = idTo;
        this.msg = msg;
    }
}
