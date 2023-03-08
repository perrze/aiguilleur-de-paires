package server;

import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

class SmNotFoundException extends Exception {
    public SmNotFoundException(String message) {
        super(message);
    }
}

public class Backend {
    private static final int RANDOM_HEX_LENGTH = 6;
    HashMap<String,ClientThread> clients;
    HashMap<String,SwitchmanThread> switchmans;


    Backend () {
        clients = new HashMap<>();
        switchmans = new HashMap<>();
    }

    String newHexId () {
        Random randomService = new Random();
        StringBuilder sb = new StringBuilder();
        while (sb.length() < RANDOM_HEX_LENGTH) {
            sb.append(Integer.toHexString(randomService.nextInt()));
        }
        sb.setLength(RANDOM_HEX_LENGTH);
        return sb.toString();
    }

    public String addClient(ClientThread client){
        String tempId=newHexId();
        while(clients.containsKey(tempId)){
            tempId=newHexId();
        }
        client.id=tempId;
        clients.put(tempId,client);
        return tempId;
    }

    public String addSwitchman(SwitchmanThread switchman){
        String tempId=newHexId();
        while(switchmans.containsKey(tempId)){
            tempId=newHexId();
        }
        switchman.id=tempId;
        switchmans.put(tempId,switchman);
        return tempId;
    }

    public void removeSwitchman(String id) {
        switchmans.remove(id);
    }
    public void removeClient(String id) {
        clients.remove(id);
    }

    // Return IP address of the switchman that match the mac address provided
    InetAddress getSmIpFromMac(String smMac) throws SmNotFoundException {
        // For every switchman known by server
        for(Map.Entry<String, SwitchmanThread> entry : switchmans.entrySet()) {
            SwitchmanThread value = entry.getValue();
            // If the mac address match
            if (value.macAddress.equals(smMac)) {
                // Return the IP address
                return value.ipAddress;
            }
        }
        throw new SmNotFoundException("Switchman("+ smMac +") not found");

    }

    String getSwitchmanIdFromMac(String smMac) throws SmNotFoundException {
        // For every switchman known by server
        for(Map.Entry<String, SwitchmanThread> entry : switchmans.entrySet()) {
            SwitchmanThread value = entry.getValue();
            // If the mac address match
            if (value.macAddress.equals(smMac)) {
                // Return the IP address
                return value.id;
            }
        }
        throw new SmNotFoundException("Switchman("+ smMac +") not found");

    }

    // Send a message to a peer (client or switchman)
    void sendMessage(String idFrom,String idTo, String messageContent) throws IOException {
        // For every client known by server
        for(Map.Entry<String, ClientThread> entry : clients.entrySet()) {
            ClientThread client = entry.getValue();
            // test if the client is the one we want to send the message
            if (client.id.equals(idTo)) {
                // Send the message
                client.sendMessage(idTo,messageContent);
            }
        }
        // For every switchman known by server
        for (Map.Entry<String, SwitchmanThread> entry : switchmans.entrySet()) {
            SwitchmanThread switchman = entry.getValue();
            // test if the switchman is the one we want to send the message;
            if (switchman.id.equals(idTo)) {
                // Send the message
                switchman.sendMessage(idTo,messageContent);
            }
        }

    }


}
