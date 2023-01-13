import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * This class is used to create an interface for clients and switchmans to connect to the server
 * It links backend and and threads (Like controller in MVC)
 * @author perrze
 */
public class Frontend {
    private ServerSocket clientsSocket;
    private ServerSocket switchmansSocket;
    private Backend backend;
    private Thread waitingClient;
    private Thread waitingSwitchman;

    /**
     * Constructor of Frontend class which creates sockets for switchmans and clients
     *
     * @param portClient the port for clients to connect
     * @param portSwitchman the port for switchmans to connect
     */
    Frontend(int portClient, int portSwitchman){
        try {
            clientsSocket = new ServerSocket(portClient);
            switchmansSocket =  new ServerSocket(portSwitchman);
            startWaiting();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }

    /**
     * Method which starts the threads for waiting connection from clients and switchmans
     * One thread for each
     * If connected, adding it to te backend lists
     */
    public void startWaiting(){
        waitingClient = new Thread(new Runnable() {

            @Override
            public void run() {
                while(true){
                    try {
                        // Two types of peer connect to the server
                        // Clients peer
                        Socket socketClient=clientsSocket.accept();
                        String id = backend.addClient(new ClientThread(socketClient,backend));
                        ClientThread tempClient= backend.clients.get(id);
                        tempClient.out.writeObject(tempClient.id);
                        System.out.println("client " +tempClient.id+" connected");
                    } catch (IOException e) {

                    }
                }
            }
        });
        waitingClient.start();
        waitingSwitchman = new Thread(new Runnable() {

            @Override
            public void run() {
                while(true){
                    try{
                        // Switchman peer
                        Socket socketSwitchman = switchmansSocket.accept();
                        String id = backend.addSwitchman(new SwitchmanThread(socketSwitchman,backend));
                        SwitchmanThread tempSm=backend.switchmans.get(id);
                        tempSm.out.writeObject(tempSm.id);
                        System.out.println("Switchman "+tempSm.id+" connected");
                    } catch (IOException e) {
                    }
                }
            }
        });
        waitingSwitchman.start();

    }

    /**
     * Main method to launch the server
     * @param args
     */
    public static void main(String[] args){
        System.out.println("Server started");
        Frontend frontend = new Frontend(5000,5001);
        frontend.backend = new Backend();
    }
}
