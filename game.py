from server import *
import queue


def run_game():
    #initate game
    #initiate queue
    q = queue.Queue()
    #start the server
    # creates the server
    server = Server(q)
    # launching the server and create threads for connections
    server.run()
    
    while True:
        
        if not q.empty():
            i = q.get()
            print(i)

     

run_game()

