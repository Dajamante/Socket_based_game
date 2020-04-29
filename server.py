import socket
import threading 
import queue
from _thread import *


SERVER = "127.0.0.1"
PORT = 65432
print_lock = threading.Lock() 




def threaded_client(conn, q, id):

    while True: 
        # data received from client 
        data = conn.recv(1024).decode('ascii')
       
        if not data: 
            print('Bye') 
            
            # lock released on exit 
            #print_lock.release() 
            break

        # reverse the given string from client 
        #data = data[::-1]
        msg = "Received data"
        conn.send(msg.encode('ascii')) 
        q.put(data) 
        print(f"data from client {id} is put in queue")
        # # send back reversed string to client 
        

    # connection closed 
    conn.close() 


class Server:

    def __init__(self, queue):
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((SERVER, PORT))
            # open up port -> accept client socket -> create player reprensentation
            self.server_socket.listen()
            self.queue = queue
            
    

    def run(self):
        count = 0
        while count < 2:
            print("Waiting for connection, server started.")
            conn, address = self.server_socket.accept()
            print(f"Connected to :{address}")
            # Player = Entity(client_number, x=20, y=20, char='B')
            # self.clientList.append(Player)
            #print_lock.acquire() 
            start_new_thread(threaded_client, (conn, self.queue, count,))
            count += 1
        
        
            

