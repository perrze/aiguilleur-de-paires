#! /bin/python3 
import socket
from threading import *
import json

HOST = "10.0.0.5"
PORT = 5000



# clientSocket.sendall(b"Hello, world")
# while(True):
#     data = clientSocket.recv(1024)
#     if(data!=None):
#         print(data)
#     clientSocket.sendall(b"Message Test 1")
#     clientSocket.sendall(bytes(input(),"UTF8"))


class Client(Thread):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __init__(self,host,port):
        Thread.__init__(self)
        self.serverIp=host
        self.port=port
        self.clientSocket.connect((HOST, PORT))
        self.start()
    def run(self):
        while True:
            dataType=self.clientSocket.recv(4096).decode("UTF8")
            content=self.clientSocket.recv(4096).decode("UTF8")
            if(len(content)!=0 or len(dataType)!=0):
                print(dataType)
                print(content)  
                self.decisionTree(dataType,content)
            
    def decisionTree(self,dataType,content):
        print("test")
        match dataType:
            case "UserMessage":
                content=json.loads(content)
                idFrom = content[0]
                message = content[1]
                print("UserMessage from "+idFrom+" : "+message)


client=Client(HOST,PORT)