package client;

import java.io.EOFException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

/**
 * This class is used on client device to connect to the server
 *
 */
public class ClientSide {
    boolean isConnected;
    Socket socket;
    ObjectInputStream in;
    ObjectOutputStream out;
    String id;
    Thread thread;

    /**
     * Constructor of Client.ClientSide class which creates a new Socket on client by connecting to the server
     * Also declare a Thread containing inputstream to get infos from server
     * @param portClient the port of the client
     * @param ipServer the ip of the server
     */
    ClientSide(int portClient, String ipServer){
        this.isConnected=connection(portClient,ipServer);
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
     * Method which creates a new Socket on client by connecting to the server
     *
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
            System.out.println("Connection to "+servAdr);
            socket = new Socket(servAdr, port);
            System.out.println("Socket created");
            out = new ObjectOutputStream(socket.getOutputStream());
            in = new ObjectInputStream(socket.getInputStream());
        } catch (Exception e) {
            isConnected = false;
            e.printStackTrace();
        }
        return isConnected;
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
     * Method which declares a Thread containing inputstream to get infos from server
     * It calls decisionTree() method to know what to do with data received
     *
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
                    } catch (EOFException e) {
                        System.out.println("Connection lost with server.");
                        close();
                        System.exit(10);
                    } catch (IOException e) {
                        e.printStackTrace();
                    } catch (ClassNotFoundException e) {
                        e.printStackTrace();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    /**
     * Method which decides what to do with the data received from the server
     * @param dataType type of data received
     * @param content data received

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
        client.ClientSide clientSide=new client.ClientSide(5000,"10.0.0.5");
        System.out.println("Client is running");



        try {
            clientSide.out.writeObject("");
            clientSide.out.writeObject("Hello World");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }

}

