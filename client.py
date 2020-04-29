import socket
import time 

SERVER = "localhost"
PORT = 65432

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((SERVER, PORT))
        self.addr = (SERVER, PORT)

    def run(self):
        
        msg = "string to revert"

        while True:
            time.sleep(0.5)
            self.s.send(msg.encode('ascii')) 
            
            #Receive back string from server
            #data = self.s.recv(1024) 
            #print('Received from the server :',str(data.decode('ascii'))) 
            
            # print the received message 
            # here it would be a reverse of sent message 
            #print('Received from the server :',str(data.decode('ascii'))) 
            
            # # ask the client whether he wants to continue 
            # ans = input('\nDo you want to continue(y/n) :') 
            # if ans == 'y': 
            #     continue
            # else: 
            #     break
        # close the connection 
        self.s.close()

n = Network()
n.run()