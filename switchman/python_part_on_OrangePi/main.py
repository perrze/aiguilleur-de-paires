#!/bin/python3
import socket
import serial
from os import environ,getenv

def client_program():
    # Defining serial parameters into ser
    ser = serial.Serial(SERIAL_DEV, 9600, timeout=1)
    ser.reset_input_buffer() # Emptying initial input buffer
    
    client_socket = socket.socket()  # instantiate client socket
    client_socket.connect((HOST, SOCKET_PORT))  # connect to the server
    
    client_socket.send(get_mac_address().encode())
    
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
    ser.write((port+"\n").encode('utf-8')) # writing received port into arduino
    line = ser.readline().decode('utf-8').rstrip()
    return line

def get_mac_address():
    with open(MAC_FILE) as f:
        content = f.read()
    return ''.join(content.split()[0].split(":"))


if __name__ == '__main__':
    if "ORCHIP" in environ:
        HOST = getenv("ORCHIP")  
    else:
        HOST="10.10.0.5"
    if "SOCKET_PORT" in environ:
        SOCKET_PORT=getenv("SOCKET_PORT")
    else:
        SOCKET_PORT=13000
    if "SERIAL_DEV" in environ:
        SERIAL_DEV = getenv("SERIAL_DEV")
    else:
        SERIAL_DEV = "/dev/ttyACM0"
    if "MAC_FILE" in environ:
        MAC_FILE = getenv("MAC_FILE")
    else:
        MAC_FILE="/sys/kernel/debug/bluetooth/hci0/identity"
    client_program()
    # print(send_mac_address_6())