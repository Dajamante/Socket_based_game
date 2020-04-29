from server import *
import queue
from _thread import *
import threading


def run_game():
    # initate game
    # initiate queue
    q = queue.Queue()
    # start the server
    # creates the server
    server = Server(q)
    # launching a threaded server and create threads for connections
    start_new_thread(server.run, ())

    while True:
        if not q.empty():
            i = q.get()
            print(i)


run_game()
