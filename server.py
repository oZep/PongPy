import threading
import socket

HOST = '127.0.0.1' # local host
PORT = 51313
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []
aliases = []



def broadcast(message):
    '''
    broadcasts message to all clients
    '''
    for client in clients:
        client.send(message)

def handle_client(client):
    '''
    handles clients' connections
    '''
    while True:
        try:
            message = client.recv(1024) # max bites 1024
            broadcast(message)
        except: # get rid of the client causing the error
            index = clients.index(client) # searches tuple and returns index
            clients.remove(client)
            client.close()
            print("Server has stopped")
            break

def recieve():
    '''
    main function to recieve client connections
    '''
    while True:

        print('Server is running and listening...')
        # let server accept any incomming connections
        client, address = server.accept()

        print(f'Connection is established with {str(address)}') # cannot concatenate therefore f strings

        # append alias and client to the list
        clients.append(client)

        if len(clients) == 2:
            print('sent')
            broadcast('Connected'.encode('utf-8'))
                    

        # create and start the thread
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    recieve()