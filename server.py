import socket
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

if(not os.path.isdir('shared_files')):
    os.makedirs('shared_files')

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

    while True:
        client,addr = SERVER.accept()
        name = client.recv(4096).decode().lower()
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

def ftp():
    global IP

    authoriser = DummyAuthorizer()
    authoriser.add_user('ftp','ftp','.','elradfmw')

    handler = FTPHandler
    handler.authorizer = authoriser

    ftp_server = FTPServer((IP,21),handler)
    ftp_server.serve_forever()

setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp)
ftp_thread.start()