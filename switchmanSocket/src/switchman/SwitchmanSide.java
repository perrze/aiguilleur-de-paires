import java.io.EOFException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

/**
 * This class is used on switchman device to connect to the server
 */
public class SwitchmanSide {

    boolean isConnected;
    Socket socket;
    ObjectInputStream in;
    ObjectOutputStream out;
    String id;
    Thread thread;

    /**
     * Constructor of SwitchmanSide class which creates a new Socket on switchman by connecting to the server
     * @param portClient
     * @param ipServer
     */
    SwitchmanSide(int portClient, String ipServer){
        this.isConnected=connection(portClient,ipServer);
        System.out.println("Connection to "+ipServer);
        if (!isConnected){
            System.out.println("Connection failed");
            System.exit(1);
        }
        try {
            id = (String) in.readObject();
            System.out.println("id: "+id);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        declareThread();
        thread.start();

    }

    /**
     * Method which creates a new Socket on switchman by connecting to the server
     * @param port the port of the server
     * @param adr the address of the server
     * @return
     */
    public boolean connection(int port,String adr) {
        boolean isConnected = true;
        InetAddress servAdr;
        try {
            if (adr.equals(""))	servAdr = InetAddress.getByName("localhost");
            else servAdr = InetAddress.getByName(adr);
//            System.out.println("Socket");
            socket = new Socket(servAdr, port);
//            System.out.println("Socket created");
            out = new ObjectOutputStream(socket.getOutputStream());
            in = new ObjectInputStream(socket.getInputStream());
//            System.out.println("Streams created");
        } catch (Exception e) {
            isConnected = false;
            e.printStackTrace();
        }
        return isConnected;
    }

    void close(){
        try {
            in.close();
            out.close();
            socket.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Method which declares a Thread containing inputstream to get infos from server
     * It calls the method decisionTree() to decide what to do with the received message
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
                    } catch (EOFException e) {
                        System.out.println("Connection lost with server.");
                        close();
                        System.exit(10);
                    } catch (IOException e) {
                        e.printStackTrace();
                    } catch (ClassNotFoundException e) {
                        e.printStackTrace();
                    } catch (Exception e) {
                    }
                }
            }
        });
    }

    /**
     * Method which decides what to do with the received message
     * @param dataType
     * @param content
     * @throws IOException
     */
    public void decisionTree(String dataType, Object content) throws IOException {
        switch(dataType){
            case "MessageToUser":
                ArrayList<String> contentArray= (ArrayList<String>) content;
                String peerIp=contentArray.get(0);
                String peerId=contentArray.get(1);
                String message=contentArray.get(2);
                System.out.println("Message From "+peerId+"("+peerIp+") : "+message);
                break;
        }
    }
    public static void main(String[] args) {
        System.out.println("Switchman is starting");
        SwitchmanSide switchmanSide=new SwitchmanSide(5001,"10.0.0.5");
        System.out.println("Switchman is running");
    }
}

