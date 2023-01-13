import java.net.Socket;
import java.net.SocketException;
/**
 * This class is used to create a thread for each switchman connected to the server.
 * It is used to manage the communication with the switchman.
 *
 * @author perrze
 *
 */
public class SwitchmanThread extends TypicalThread {
    String macAddress;

    /**
     * Constructor of SwitchmanThread class which creates a new thread for a switchman
     * With in and out streams (ObjectInputStream and ObjectOutputStream)
     *
     * @param socket the socket of the switchman (Defined in Frontend)
     * @param backend the backend of the server
     */
    public SwitchmanThread(Socket socket,Backend backend) {
        super(socket,backend);
        System.out.println("Accepting a switchman");
        declareThread();
        thread.start();
    }

    /**
     * Method which declares the thread for the switchman
     * The thread is used to read the messages sent by the switchman
     * Read first a String containing the type of data sent
     * Then read the data
     */
    public void declareThread() {
        thread = new Thread(new Runnable() {

            @Override
            public void run() {
                // met le serveur en attente
                while (true) {
                    try {
                        // read the message sent by the client
                        String latestMessage = (String) in.readObject();
                        System.out.println("Message received: " + latestMessage);
                    } catch (SocketException e){
                        System.out.println("Switchman "+id+" disconnected");
                        close();
                        backend.removeSwitchman(id);
                        thread.interrupt();
                        break;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }



}
