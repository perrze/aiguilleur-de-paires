import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;

/**
 * This class is used as a sample thread for clients and switchmans.
 * @author perrze
 */
public class TypicalThread {
    Socket socket;
    ObjectInputStream in;
    ObjectOutputStream out;
    InetAddress ipAddress;
    Thread thread;
    Backend backend;
    String id;

    /**
     * Constructor of TypicalThread class which creates a new thread model for clients and switchmans
     * With in and out streams (ObjectInputStream and ObjectOutputStream)
     * @param socket
     * @param backend
     */
    public TypicalThread(Socket socket,Backend backend) {
        try {
            // waiting for a client
            this.socket = socket;
            this.backend=backend;
            // Creating the streams for communication with the client
            out = new ObjectOutputStream(socket.getOutputStream());
            in = new ObjectInputStream(socket.getInputStream());

            ipAddress = socket.getInetAddress();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    /**
     * Method which close the streams and the socket of the thread
     */
    public void close() {
        try {
            in.close();
            out.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    /**
     * Method which sends a message to the peer
     * @param idFrom the id of the sender
     * @param message the message to send
     */
    public void sendMessage(String idFrom, String message) throws IOException {
        out.writeObject("MessageToUser");
        out.writeObject(idFrom+" : "+message);
    }



}
