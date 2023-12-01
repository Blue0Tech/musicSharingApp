import socket
from threading import Thread

IP = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}

def setup():
    print('\n\t\t\t\t\tIP MESSENGER\n')
    global PORT
    global IP
    global SERVER

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP,PORT))
    SERVER.listen(100)

    print('\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n')
    acceptConnections()

def acceptConnections():
    global SERVER
    global clients
    global BUFFER_SIZE

    while True:
        client,addr = SERVER.accept()
        name = client.recv(BUFFER_SIZE).decode().lower()
        clients[name] = {
            'client':client,
            'address':addr,
            'connected_with':'',
            'file_name':'',
            'file_size':4096
        }
        
        print(f'Connection established with {name} : {addr}')
        thread = Thread(target=clientThread,args=(client,name))
        thread.start()

def clientThread(client,name):
    pass

setup()