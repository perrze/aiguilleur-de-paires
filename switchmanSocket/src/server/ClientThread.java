package server;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import server.orderJson.UserMessage;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;

/**
 * This class is used to create a thread for each client connected to the server.
 * It is used to manage the communication between the server and the client.
 *
 * @author perrze
 */
public class ClientThread {
    Socket socket;
    BufferedReader in;
    PrintWriter out;
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
    public ClientThread(Socket socket,Backend backend) {
        try {
            // waiting for a client
            this.socket = socket;
            this.backend=backend;
            // Creating the streams for communication with the client
            out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            ipAddress = socket.getInetAddress();

        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("Accepting a client");
        declareThread();
        thread.start();
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
                        String dataType = in.readLine();
                        // get the data sent by the client
                        Object content = in.readLine();
                        decisionTree(dataType,content);
                    } catch (NullPointerException e){
                        System.out.println("Client "+id+" disconnected");
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
        final Gson gson = new GsonBuilder().setPrettyPrinting().create();
        switch(dataType){
            case "UserMessage":
                UserMessage msg = gson.fromJson((String) content,UserMessage.class);

                try {
//                    String id = backend.getSwitchmanIdFromMac(smMac);
                    backend.sendMessage(msg.idFrom, msg.idTo, msg.msg);

                }catch (Exception e) {
                    e.printStackTrace();
                }

                break;
        }
    }
    public void sendMessage(String idFrom, String message) {
        out.println("MessageToUser");
        out.println(idFrom+" : "+message);
    }



}