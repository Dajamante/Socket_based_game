import socket
import threading
import queue
from _thread import *


SERVER = "localhost"
PORT = 65432


def threaded_client(conn, q, id):

    while True:
        # data received from client
        data = conn.recv(1024).decode('ascii')

        if not data:
            print('Bye')
            break
        q.put(data)
        print(f"data from client {id} is put in queue")

        # testing response
        msg_back = f"data from client {id} was put in server's queue"
        conn.send(msg_back.encode('ascii'))

    conn.close()


class Server:

    def __init__(self, queue):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER, PORT))
        self.server_socket.listen()
        self.queue = queue

    def run(self):
        # Starts with player 1, increment count for any new player
        # The server is threaded and runs independently
        count = 1
        while True:
            print("Waiting for connection, server started.")
            conn, address = self.server_socket.accept()
            print(f"Connected to :{address}")
            start_new_thread(threaded_client, (conn, self.queue, count,))
            count += 1
