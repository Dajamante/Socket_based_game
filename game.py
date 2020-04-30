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
    # launching a threaded server that can accept unlimited clients
    # and create threads for connections
    start_new_thread(server.run, ())

    while True:
        if not q.empty():
            # update the content from the queue with custom message
            i = q.get() + " and is now in game loop."
            # TO DO: get movement with id, send to some method which will update the
            # player with right ID
            print(i)
            # distribute the processed data to all the clients, one after the other
            # TO DO: send world json object instead
            for client in server.client_list:
                client.send_processed_data(i)


run_game()
