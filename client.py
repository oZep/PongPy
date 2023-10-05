import threading
import socket
from scripts.entities import Player

class Client:

    def __init__(self, port=51313, host='127.0.0.1'):
        '''
        intializes client
        (int port, str(host))
        '''
        self.host = host
        self.port = port
        #alias = input('Choose yo >>> ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        # make threads for receiving and sending
        self.receive_thread = threading.Thread(target=self.client_recieve)
        self.receive_thread.start()
        self.send_thread = threading.Thread(target=self.client_send)
        self.send_thread.start()
        self.connected = 0

    def client_recieve(self):
        '''
        recieve messages from the server
        '''
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'Connected':
                    self.connected = 1
                #else:
                #    print(message) # print the message that is sent from the server
                #    self.game.player2.pos = message['pos']
                #    self.game.player2.hp = message['health']
                if self.connected:
                    print(message)
                    # send game data 

                print(message)
            except:
                print("Error")
                self.client.close()
                break

    def client_send(self, message=''):
        '''
        send messages to the server
        '''
        while True:
            #if message == 'Connected': # need the server to only broadcast messages to everyone except for the sender
            #    self.client.send(message.encode('utf-8'))
            #message = f"{'playerSprite' : {self.game.player.select}; 'pos': {self.game.player.pos}; 'health': {self.game.player.hp};}"
            #self.client.send(message.encode('utf-8'))
            pass

