from server import *
import queue
from _thread import *
import threading
from entity import Entity
from entity import TargetEntity
from random import randint


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
    # max entities on screen
    max_entities = 10
    # world dimentions
    world_width = 100
    world_height = 100
    players = []
    entities = []
    everyone = []

    make_entities()

    while True:
        if not q.empty():
            # update the content from the queue with custom message
            i = q.get() + " and is now in game loop."

            update_position(i)
            # TO DO: get movement with id, send to some method which will update the
            # player with right ID
            print(i)
            # distribute the processed data to all the clients, one after the other
            # TO DO: send world json object instead
            for client in server.client_list:
                client.send_processed_data(i)

    def make_entities():
        for client in server.clients_list:
            players.append(client)
        # making targets:
        for i in range(max_entities):
            npc = TargetEntity(randint(1, world_width-5), randint(
                1, world_height-5))
        entities.append(npc)

        # putting every entity and player in a single array
        everyone = [*entities, *players]

    def update_position(i):
        # get entity by id
        # move the entity
        pass


run_game()
