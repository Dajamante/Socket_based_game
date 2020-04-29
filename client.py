import socket
import time

SERVER = "localhost"
PORT = 65432


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((SERVER, PORT))
        self.addr = (SERVER, PORT)

    def run(self):

        msg = "String sent from client"

        while True:
            time.sleep(1)
            self.s.send(msg.encode('ascii'))

            retour = self.s.recv(1024)
            print(retour)
        self.s.close()


c = Client()
c.run()
