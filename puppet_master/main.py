#!/bin/python3
import socket

#Example socket : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

def server_program():
    # get the hostname
    host = "10.0.0.5"
    port = 13000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        
        output_data = input(' -> ')
        conn.send(output_data.encode())  # send data to the client
        # receive data stream. it won't accept data packet greater than 1024 bytes
        input_data = conn.recv(1024).decode() # recv client response
        print("(DEBUG) Data recv from switchman : "+ input_data)
        if not input_data:
            # if data is not received break
            break
        
    conn.close()  # close the connection
    

if __name__ == '__main__':
    server_program()