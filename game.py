from server import *
import queue
from _thread import *
import threading
from entity import Entity
from entity import TargetEntity
from random import randint
from world import World
import time
import json


class Game:

    def __init__(self):
        # initate game
        # initiate queue
        self.q = queue.Queue()
        # start the server
        # creates the server
        self.world = World()
        self.server = Server(self.q)
        # launching a threaded server that can accept unlimited clients
        # and create threads for connections
        count_clients = start_new_thread(self.server.run, ())

    def make_entities(self):
        # making targets:
        for i in range(self.world.max_entities):
            npc = TargetEntity(x=randint(1, self.world.world_width-5), y=randint(
                1, self.world.world_height-5))
            self.world.entities.append(npc)

    def update_position(self, pos_index):
        # get entity by id
        # move the entity
        pass

    def stream_game(self):
        for client in self.server.thread_client_list:
            time.sleep(3)
            json_dump = self.world.to_json()
            # print(json_dump)
            client.send_processed_data(json_dump)

    def run_game(self):
        natural_distance = 20
        self.make_entities()

        while True:
            self.stream_game()
            if not self.q.empty():

                dict = self.q.get()
                print(dict)
                if "player" in dict:
                    cl = Entity(x=natural_distance,
                                y=natural_distance, char='B', id=dict["player"])
                    # print(cl)
                    self.world.entities.append(cl)
                    natural_distance += 20

                # update_position(i)
                # TO DO: get movement with id, send to some method which will update the
                # player with right ID
                # distribute the processed data to all the clients, one after the other
                # TO DO: send world json object instead

    # same then in entities, but adds an n to indicate end of data


game = Game()
game.run_game()
