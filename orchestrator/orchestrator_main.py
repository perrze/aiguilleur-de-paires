#!/bin/python
# ---------------------------------- Imports --------------------------------- #

from flask import Flask,jsonify,request
import socket
import threading
import logging
from secrets import token_hex
from os import environ,getenv
from flask_cors import CORS
import sys

#===========================================================================
#                            Switchman Socket
#===========================================================================

# Threading for accepting switchman
# switchman_server_socket : server socket on port 13000 for switchmans
def accepting_switchman(switchman_server_socket):
    global switchmans # Calling the global var
    while True:
        try:
            temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
            id = temp_conn.recv(1024).decode()
            # id=token_hex(6) # generate a token of 12 char for simulating bluetooth mac
            # Logging
            if GDPR_COMPLIANCE:
                info_logger.info("Switchman connected from token: " + id)  
            else:
                info_logger.info("Switchman connected from: " + str(temp_address) + " token: "+id)
            # Adding new switchmans to temporary DB      
            switchmans[id]=temp_conn
        except:
            pass
"""Used for testing socket connection to a switchman
"""
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
"""Used to check if a socket is closed by differents means
"""
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

"""List the switchmans known by the DB 
"""
def list_switchmans():
    global switchmans
    if not(len(switchmans)>0): # If the list is empty
       return [{"id":"List Empty"}]
    returning=[]
    for switchman in switchmans: # For each switchmans known
        if(test_switchman(switchman)): # Testing if the switchman's socket is close
            returning.append({"id":switchman}) # Adding a Switchman object to the list which will be returned
    if (len(returning)>0):
        return returning
    else:
        return [{"id":"List Empty"}]

def print_switchmans_list(listToPrint):
    for i in listToPrint:
        print("id : "+i["id"],file=sys.stderr)

"""Chat module is use for controlling switchmans from command line
It can be started automatically by passing the USE_CHAT in environment variables
"""
def chat_module(switchman_server_socket):
    global switchmans
    term_in = input(' -> ')
    if term_in=="":
        return 
    if (term_in=="help"): # if help print help
        print("help menu :\n"
              "- send switchman_id command (ex: send a1b2c3 P1) : send a command to a switchman\n"
              "- list : give the list of available switchman\n",file=sys.stderr)
    elif (term_in=="list"): # if list print list of switchmans
        toPrint=False
        while(not(toPrint)):
            try:
                toPrint=list_switchmans()
            except:
                print("(DEBUG) Updated list",file=sys.stderr)
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
            print("(DEBUG) Data recv from switchman ("+id+") : "+ input_data,file=sys.stderr)
        except:
            print("(DEBUG) Error in send synthax",file=sys.stderr)
    elif(term_in=="exit"):
        for id in switchmans:
            conn = switchmans[id]
            conn.send("CL".encode())  # send data to the client
            # receive data stream. it won't accept data packet greater than 1024 bytes
            input_data = conn.recv(1024).decode() # recv client response
            print("(DEBUG) Data recv from switchman ("+id+") : "+ input_data,file=sys.stderr)
        switchman_server_socket.close()
        exit()
    else:
        print("Unrecognized command, use help for help",file=sys.stderr)

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
"""List the switchmans known by the orchestrator formatted according to the contract
"""
@app.route("/switchmans")
def listSwitchmans():
    return jsonify(list_switchmans()),200
    
"""Make a Switchman executing an order given in a post request
"""
@app.route("/switchmans/send", methods=['POST'])
def sendSwitchman():
    # Getting data sent
    data=request.json
    info_logger.info("Data sent: "+str(data))
    global switchmans 
    key_allowed=["id","pair"]
    if(data):
        # Testing if data is well formatted
        if len(data)!=2:
            return 'Bad JSON',400
        for key in data:
            if (not(key in key_allowed)):
                return 'Bad JSON',400
        idFound=False
        # Searching for the good switchman
        for  switchman in switchmans:
            if switchman==data['id']:
                idFound=True
                # getting information
                id=data['id']
                command=data['pair'] 
                # Update database
                # switchmans[id]['state']==command 
                conn_sm=switchmans[id]
                test_switchman(switchman)
                if test_switchman(switchman): # Testing if the socket is still open
                    info_logger.info("Command sent to SM ("+id+"): "+command)
                    conn_sm.send(command.encode())  # send data to the client
                    # receive data stream. it won't accept data packet greater than 1024 bytes
                    input_data = conn_sm.recv(1024).decode() # recv client response
                    debug_logger.debug("Data recv from switchman ("+id+") : "+ input_data)
                else:
                    debug_logger.debug("Switchman disconnected")
                    return 'Switchman Not Found',404
        if(idFound): # Switchman was found and action were taken
            return jsonify({"id": id,"pair":command}),200
        else: # Switchman not found
            debug_logger.debug("Switchman ("+id+") not found")
            return 'Switchman Not Found',404
    else:
        return 'No Data',400

# ---------------------------------------------------------------------------- #
#                                Main functions                                #
# ---------------------------------------------------------------------------- #

formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S')
def setup_logger(name, log_file, level=logging.INFO):

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# ---------------------------- Setup instructions ---------------------------- #

global switchmans
switchmans={}

if __name__ == '__main__':
    
    # Setuping loggers
    
    info_logger = setup_logger('info_logger','/var/log/orchestrator.info.log',level=logging.INFO)
    debug_logger = setup_logger('debug_logger','/var/log/orchestrator.debug.log',level=logging.DEBUG)
    
    logging.basicConfig(filename="/var/log/orchestrator.flask.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    
    
    # Defining constants
    """We are using default values for each of constants
    They can be changed by environment variables
    """
    if "HOST" in environ:
        HOST = getenv("HOST")
    else:
        HOST = "0.0.0.0"
    if "SM_PORT" in environ:
        SM_PORT = int(getenv("SM_PORT"))
    else:
        SM_PORT = 13000
    if "USE_CHAT" in environ:
        USE_CHAT=True
    else:
        USE_CHAT=False
    if "GDPR_COMPLIANCE" in environ:
        GDPR_COMPLIANCE = eval(getenv("GDPR_COMPLIANCE"))
    else:
        GDPR_COMPLIANCE = False
        
    # Starting a thread for switchman acceptance
    serverThread=threading.Thread(target=server_program)
    serverThread.start()
    
    # Starting flask
    app.run(host=HOST)
    
