import java.io.IOException;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;

/**
 * This class is used to create a thread for each client connected to the server.
 * It is used to manage the communication between the server and the client.
 *
 * @author perrze
 */
public class ClientThread extends TypicalThread {
    /**
     * Constructor of ClientThread class which creates a new thread for a client
     * With in and out streams (ObjectInputStream and ObjectOutputStream)
     *
     * @param socket the socket of the client (Defined in Frontend)
     * @param backend the backend of the server
     */
    public ClientThread(Socket socket,Backend backend) {
        super(socket,backend);
        System.out.println("Accepting a client");
        declareThread();
        thread.start();
    }
    /**
     * Method which declares the thread for the client
     * The thread is used to read the messages sent by the client
     * Read first a String containing the type of data sent
     * Then read the data
     */
    public void declareThread() {
        this.thread = new Thread(new Runnable() {

            @Override
            public void run() {
                while (true) {
                    try {
                        // get the type of data sent by the client
                        String dataType = (String) in.readObject();
                        // get the data sent by the client
                        Object content = in.readObject();
                        decisionTree(dataType,content);
                    } catch (SocketException e){
                        System.out.println("client " +id+" disconnected");
                        close();
                        backend.removeClient(id);
                        thread.interrupt();
                        break;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    /**
     * Method which decides what to do with the data and data type sent by the client
     *
     * "SendMessageSwitchman" : send a String to a Switchman using its MacAddress
     * @param dataType : the type of data sent by the client
     * @param content : Object containing variable Objects
     * @throws IOException
     */
    public void decisionTree(String dataType, Object content) throws IOException {
        switch(dataType){
            case "SendMessageSwitchman":
                ArrayList<String> infos = (ArrayList<String>) content;
                String smMac=infos.get(0);
                String messageContent=infos.get(1);

                try {
                    String id = backend.getSwitchmanIdFromMac(smMac);
                    backend.sendMessage(id, messageContent);

                } catch (SmNotFoundException e) {
                    // send a message to user (app) to inform him that the switchman is not found
                    // Strings to be treated by the app to display a message to the user in good language
                    out.writeObject("MessageToUser");
                    out.writeObject("smNotFound");
                }
                catch (Exception e) {
                    e.printStackTrace();
                }

                break;
        }
    }


}