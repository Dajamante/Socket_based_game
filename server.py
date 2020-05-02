import socket
import threading
import queue
from _thread import *
import json

SERVER = "localhost"
PORT = 65432

"""
Representation of the player on the server. "Player manager".
Getting the data from clients in the form of a dictionary {move: [a b]}
adding an id-variable and sending it to the queue.
"""


class ThreadedClient():

    def __init__(self, conn, q, id):
        self.conn = conn
        self.q = q
        self.id = id

    def run(self):

        while True:
            # data received from client
            data = self.conn.recv(1024).decode('ascii')
            data = json.loads(data)
            if not data:
                print('Bye')
                break

            # formatting self.id ++ requested move
            # to be able to access that shit later

            data["id"] = self.id
            # string_data = f"data from client {self.id} is put in queue"
            # print(string_data)

            # put the json/dictionary in queue
            # use json loads to restore the data!
            self.q.put(data)

            # Can be used to testing response
            # msg_back = f"ping back to client {self.id}"
            # self.conn.send(msg_back.encode('ascii'))

        self.conn.close()

    def send_processed_data(self, data):
        self.conn.sendall(data.encode('ascii'))


class Server:

    def __init__(self, queue):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER, PORT))
        self.server_socket.listen()
        self.queue = queue
        self.thread_client_list = []

    def run(self):
        # Starts with player 1, increment count for any new player
        # The server is threaded and runs independently
        count = 1
        while True:
            print("Waiting for connection, server started.")
            conn, address = self.server_socket.accept()
            print(f"Connected to :{address}")

            # class threaded clients that has information on the server queue
            # and the client connection
            threaded_client = ThreadedClient(conn, self.queue, count)
            self.thread_client_list.append(threaded_client)
            # informing the game that a new client has come. Using the queue IS A
            # THREAD SAFE method since Queue is thread safe.
            new_ent = {"player": count}
            self.queue.put(new_ent)

            # all new clients have their own threads
            start_new_thread(threaded_client.run, ())
            count += 1
