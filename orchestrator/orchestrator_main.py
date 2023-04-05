from flask import Flask,jsonify,request
import socket
import threading
from secrets import token_hex
#Example socket : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

global switchmans
switchmans={}
global androids
androids={}
#===========================================================================
#                            Switchman Socket
#===========================================================================
# switchmans = []
switchmansReturn=[
  {
    "id": "a1b2c3e4f5a6"
  }
]

switchman={
  "id": "a1b2c3e4f5a6",
  "state": "P1"
}

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
        # try:
        #     # print("try")
        #     test_switchman(switchman)
        #     returning.append({"id":switchman})
        #     # print(returning)            
        # except Exception as e:
        #     # print("test")
        #     if str(e)=="[Errno 32] Broken pipe":
        #         switchmans.pop(switchman)
        #         # print(switchmans)
        #         return False
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
        # while(not(toPrint)):
        #     toPrint=list_switchmans(switchmans)
        #     # print("(DEBUG) Updated switchmans")  
        # print(toPrint)
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
    # get the hostname
    host_sm = "0.0.0.0"
    # host_sm = "127.0.0.1"
    port_sm = 13000  # initiate port no above 1024

    switchman_server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    # switchman_server_socket.setblocking(0)
    switchman_server_socket.bind((host_sm, port_sm))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    switchman_server_socket.listen(32)
    
    accepting_sm=threading.Thread(target=accepting_switchman,args=(switchman_server_socket,))
    accepting_sm.start()
    
    # # Testing connectio without thread
    # temp_conn, temp_address = switchman_server_socket.accept()  # accept new connection
    # id=token_hex(6)
    # print("Connection from: " + str(temp_address) + " token: "+id)
    # switchmans[id]=temp_conn
    
    # print("test")
    while True:
        chat_module(switchman_server_socket)




#===========================================================================
#                            Flask
#===========================================================================


app = Flask(__name__)


@app.route("/")
def get_root():
    return "Welcome to switchman API"

@app.route("/switchmans")
def get_switchmans():
    return jsonify(list_switchmans()),200
    # return jsonify(switchmans),200

@app.route("/switchmans/act", methods=['POST'])
def post_act_switchman():
    global switchmans
    key_allowed=["id","state"]
    data=request.get_json()
    if(data):
        for key in data:
            if (not(key in key_allowed)):
                return '',400
        idFound=False
        for  switchman in switchmans:
            if switchman==data['id']:
                idFound=True
                # getting information
                id=data['id']
                command=data['state'] 
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
                    return 'Switchman Not Found',410
        if(idFound):
            return jsonify(switchman),200
        else:
            print('(DEBUG) SM not found')
            return 'Switchman Not Found',404
    else:
        return '',400




if __name__ == '__main__':
    serverThread=threading.Thread(target=server_program)
    serverThread.start()
    app.run(host="0.0.0.0")