#!/bin/python3
import socket
import serial
from secrets import token_hex
from os import environ


def client_program():
    #host = environ["ORCHIP"]  # as both code is running on same pc
    host="10.10.0.5"
    print("Host: "+host)
    port = 13000  # socket server port number
    # Defining serial parameters into ser
    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.reset_input_buffer() # Emptying initial input buffer
    ser=""
    client_socket = socket.socket()  # instantiate client socket
    client_socket.connect((host, port))  # connect to the server

    #id=token_hex(6)
    id="46ea41494069"
    client_socket.send(id.encode())
    
    input_data="XX"

    while True:

        input_data = client_socket.recv(1024).decode()  # receive server port order
        if input_data=="CL":
            break
        elif input_data=="TS":
            client_socket.send("OK".encode())
        else:
            print("(DEBUG) Data recv from master : "+input_data)
            output_data = serial_connection(input_data,ser)
            print("(DEBUG) Data recv from Arduino : "+output_data)
            client_socket.send(output_data.encode())

    client_socket.send("EX".encode())
    client_socket.close()


def serial_connection(port,ser):
    #ser.write((port+"\n").encode('utf-8')) # writing received port into arduino
    #line = ser.readline().decode('utf-8').rstrip()
    line=port
    return line

if __name__ == '__main__':
    client_program()
