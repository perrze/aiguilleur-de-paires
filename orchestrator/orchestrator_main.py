#!/bin/python
from flask import Flask,jsonify,request
import socket
import threading
from secrets import token_hex
from os import environ,getenv
from flask_cors import CORS
import sys
#Example socket : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

global switchmans
switchmans={}
#===========================================================================
#                            Switchman Socket
#===========================================================================

# Threading for accepting switchman
# switchman_server_socket : servr socket on port 13000 for switchmans
def accepting_switchman(switchman_server_socket):
    global switchmans
    # print("test")
    while True:
        try:
            temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
            id = temp_conn.recv(1024).decode()
            # id=token_hex(6) # generate a token of 12 char for simulating bluetooth mac
            print("Connection from: " + str(temp_address) + " token: "+id)
            switchmans[id]=temp_conn
        except:
            pass
 
def test_switchman(switchman):
    global switchmans
    conn = switchmans[switchman]
    try:
        conn.send("TS".encode())
        if not(is_socket_closed(conn)):
            return True
        else:
            return False
    except:
        switchmans.pop(switchman)
        # print(switchmans)
        return False
    
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False
    return False

def list_switchmans():
    global switchmans
    # print(len(switchmans))
    if not(len(switchmans)>0):
       return [{"id":"List Empty"}]
    returning=[]
    for switchman in switchmans:
        # print("for")
        if(test_switchman(switchman)):
            returning.append({"id":switchman})
        else:
            return False
    return returning

def print_switchmans_list(listToPrint):
    for i in listToPrint:
        print("id : "+i["id"])

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
        toPrint=False
        while(not(toPrint)):
            try:
                toPrint=list_switchmans()
            except:
                print("(DEBUG) Updated list")
        print_switchmans_list(toPrint)
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

    switchman_server_socket = socket.socket()  # get instance
    # switchman_server_socket.setblocking(0)
    switchman_server_socket.bind((HOST, SM_PORT))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    switchman_server_socket.listen(32)
    
    accepting_sm=threading.Thread(target=accepting_switchman,args=(switchman_server_socket,))
    accepting_sm.start()
    
    while USE_CHAT:
        chat_module(switchman_server_socket)

#===========================================================================
#                            Flask
#===========================================================================


app = Flask(__name__)
CORS(app)


@app.route("/")
def get_root():
    return "Welcome to switchman API"

@app.route("/switchmans")
def listSwitchmans():
    return jsonify(list_switchmans()),200
    # return jsonify(switchmans),200

@app.route("/switchmans/send", methods=['POST'])
def sendSwitchman():
    global switchmans
    key_allowed=["id","pair"]
    data=request.get_json()
    print("Data to check"+str(data), file=sys.stderr)
    if(data):
        if len(data)!=2:
            return 'Bad JSON',400
        for key in data:
            if (not(key in key_allowed)):
                return 'Bad JSON',400
        idFound=False
        for  switchman in switchmans:
            if switchman==data['id']:
                idFound=True
                # getting information
                id=data['id']
                command=data['pair'] 
                # Update database
                # switchmans[id]['state']==command 
                conn_sm=switchmans[id]
                if test_switchman(switchman): # Trying, to be removed ?
                    print("(DEBUG) Command sent to SM ("+id+"): "+command)
                    conn_sm.send(command.encode())  # send data to the client
                    # receive data stream. it won't accept data packet greater than 1024 bytes
                    input_data = conn_sm.recv(1024).decode() # recv client response
                    print("(DEBUG) Data recv from switchman after order android ("+id+") : "+ input_data)
                else:
                    print("(DEBUG) SMDisco")
                    return 'Switchman Not Found',404
        if(idFound):
            return jsonify({"id": id,"pair":command}),200
        else:
            print('(DEBUG) SM not found')
            return 'Switchman Not Found',404
    else:
        return 'No Data',400

if __name__ == '__main__':
    
    if "HOST" in environ:
        HOST = getenv("HOST")
    else:
        HOST = "0.0.0.0"
    if "SM_PORT" in environ:
        SM_PORT = getenv("SM_PORT")
    else:
        SM_PORT = 13000
    if "USE_CHAT" in environ:
        USE_CHAT=True
    else:
        USE_CHAT=False
    
    serverThread=threading.Thread(target=server_program)
    serverThread.start()
    app.run(host="0.0.0.0",debug="run")
