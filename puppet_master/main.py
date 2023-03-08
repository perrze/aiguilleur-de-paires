#!/bin/python3
import socket
import threading
from secrets import token_hex

#Example socket : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

global switchmans
switchmans={}


def accepting_switchman(switchman_server_socket):
    global switchmans
    # print("test")
    while True:
        temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
        id=token_hex(3)
        print("Connection from: " + str(temp_address) + " token: "+id)
        switchmans[id]=temp_conn


def chat_module():
    global switchmans
    term_in = input(' -> ')
    if (term_in=="help"):
        print("help menu :\n"
              "- send switchman_id command (ex: send a1b2c3 P1) : send a command to a switchman\n"
              "- list : give the list of available switchman\n")
    elif (term_in=="list"):
        for switchman in switchmans:
            print("id : "+switchman)
    elif(term_in.split()[0]=="send"):
        try:
            id=term_in.split()[1]
            command=term_in.split()[2]
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
        exit()
    else:
        print("Unrecognized command, use help for help")

def server_program():
    # get the hostname
    host = "10.0.0.5"
    port = 13000  # initiate port no above 1024

    switchman_server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    switchman_server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    switchman_server_socket.listen(10)
    
    accepting=threading.Thread(target=accepting_switchman,args=(switchman_server_socket,))
    accepting.start()
    # temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
    # id=token_hex(3)
    # print("Connection from: " + str(temp_address) + " token: "+id)
    # switchmans[id]=temp_conn
    print("test")
    while True:
        chat_module()

if __name__ == '__main__':
    server_program()


# def server_program():
#     # get the hostname
#     host = "10.0.0.5"
#     port = 13000  # initiate port no above 1024

#     switchman_server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     switchman_server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     switchman_server_socket.listen(2)
#     conn, address = switchman_server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
        
#         output_data = input(' -> ')
#         conn.send(output_data.encode())  # send data to the client
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         input_data = conn.recv(1024).decode() # recv client response
#         print("(DEBUG) Data recv from switchman : "+ input_data)
#         if not input_data:
#             # if data is not received break
#             break
        
#     conn.close()  # close the connection
    

# if __name__ == '__main__':
#     server_program()

