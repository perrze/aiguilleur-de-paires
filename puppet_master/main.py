#!/bin/python3
import socket
import threading
from secrets import token_hex

#Example socket : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

global switchmans
switchmans={}
global androids
androids={}

# Threading for accepting switchman
# switchman_server_socket : servr socket on port 13000 for switchmans
def accepting_switchman(switchman_server_socket):
    global switchmans
    # print("test")
    while True:
        temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
        id = temp_conn.recv(1024).decode()
        # id=token_hex(6) # generate a token of 12 char for simulating bluetooth mac
        print("Connection from: " + str(temp_address) + " token: "+id)
        switchmans[id]=temp_conn
        
def accepting_android(android_server_socket):
    temp_conn, temp_address = android_server_socket.accept()  # accept new connection
    id = temp_conn.recv(1024).decode()
    # id=token_hex(6) # generate a token of 12 char for simulating bluetooth mac
    print("Connection from: " + str(temp_address) + " token: "+id)
    thread=threading.Thread(target=android_socket,args=(temp_conn,id))
    thread.start()
    androids[id]=[temp_conn,thread]
    
def android_socket(conn,id_and):
    global switchmans
    global androids
    order = conn.recv(1024).decode()
    if (order=="list"): # if list print list of switchmans
        # print("list")
        content=[]
        for switchman in switchmans:
            content.append(switchman)
        dataToSend=";".join(content)
        if(dataToSend==""):
            dataToSend="NONE"
        # print(dataToSend)
        conn.send(dataToSend.encode())
        # conn.send("test".encode())
    elif(order.split()[0]=="send"): # if send, send a command
        # print("SEND")
        try:
            
            id=order.split()[1] # position of id
            # print("TRY")
            if id in switchmans:
                # print("IF")
                command=order.split()[2] # position of command
                conn_sm=switchmans[id]
                print("(DEBUG) Command sent to SM ("+id+"): "+command)
                conn_sm.send(command.encode())  # send data to the client
                # receive data stream. it won't accept data packet greater than 1024 bytes
                input_data = conn_sm.recv(1024).decode() # recv client response
                print("(DEBUG) Data recv from switchman after order android ("+id+") : "+ input_data)
                conn.send(("OK;"+input_data).encode())
                
            else:
                conn.send("SMNotFound".encode())
        except:
            conn.send("SMNotFound".encode())
            print("(DEBUG) Error in send synthax")
    else:
        conn.send("CMDNotFound".encode())
    # print("try")
    # print(order)
    # conn.send("CONTENT".encode())
    print(androids)
    end = conn.recv(1024).decode()
    if  (end=="EXIT"):
        androids.pop(id_and)
    print(androids)
            


# function defining all possibilities for chat
def chat_module(switchman_server_socket):
    global switchmans
    term_in = input(' -> ')
    if term_in=="":
        return 
    if (term_in=="help"): # if help print help
        print("help menu :\n"
              "- send switchman_id command (ex: send a1b2c3 P1) : send a command to a switchman\n"
              "- list : give the list of available switchman\n")
    elif (term_in=="list"): # if list print list of switchmans
        for switchman in switchmans:
            print("id : "+switchman)
    elif(term_in.split()[0]=="send"): # if send, send a command
        try:
            id=term_in.split()[1] # position of id
            command=term_in.split()[2] # position of command
            if not(id in switchmans):
                return None
            conn=switchmans[id]
            conn.send(command.encode())  # send data to the client
            # receive data stream. it won't accept data packet greater than 1024 bytes
            input_data = conn.recv(1024).decode() # recv client response
            print("(DEBUG) Data recv from switchman ("+id+") : "+ input_data)
        except:
            print("(DEBUG) Error in send synthax")
    elif(term_in=="exit"):
        for id in switchmans:
            conn = switchmans[id]
            conn.send("CL".encode())  # send data to the client
            # receive data stream. it won't accept data packet greater than 1024 bytes
            input_data = conn.recv(1024).decode() # recv client response
            print("(DEBUG) Data recv from switchman ("+id+") : "+ input_data)
        switchman_server_socket.close()
        exit()
    else:
        print("Unrecognized command, use help for help")

def server_program():
    # get the hostname
    host_sm = "10.0.0.5"
    port_sm = 13000  # initiate port no above 1024

    switchman_server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    switchman_server_socket.bind((host_sm, port_sm))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    switchman_server_socket.listen(32)
    
    accepting_sm=threading.Thread(target=accepting_switchman,args=(switchman_server_socket,))
    accepting_sm.start()
    
    host_android = "10.0.0.5"
    port_android = 13130
    
    android_server_socket = socket.socket()
    android_server_socket.bind((host_android,port_android))
    android_server_socket.listen(32)
    
    accepting_and=threading.Thread(target=accepting_android,args=(android_server_socket,))
    accepting_and.start()
    
    
    # # Testing connectio without thread
    # temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
    # id=token_hex(6)
    # print("Connection from: " + str(temp_address) + " token: "+id)
    # switchmans[id]=temp_conn
    
    # print("test")
    while True:
        chat_module(switchman_server_socket)

if __name__ == '__main__':
    server_program()

