from server import *
import queue
from _thread import *
import threading
from entity import Entity
from entity import TargetEntity
from random import randint
from world import World
import json


"""
Main game class that manages the game.
World: manages entities to a list.
Server: manage connections throught threaded clients

TODO:
    create walls
    make sure objects such as players and walls are untraversable (with the boolean blocked, check old project)
    make objects disappear when picked
    make score for players
    making winning condition and replay
"""


class Game:

    def __init__(self):

        # initiate queue
        self.q = queue.Queue()
        # start the server
        # creates the server
        self.world = World()
        self.server = Server(self.q)
        # launching a threaded server that can accept unlimited clients
        # and create threads for connections
        count_clients = start_new_thread(self.server.run, ())

    # creating targets entities
    def make_entities(self):

        for i in range(self.world.max_entities):
            npc = TargetEntity(x=randint(1, self.world.world_width-5), y=randint(
                1, self.world.world_height-5))
            self.world.entities.append(npc)

    # move the entity by id
    def update_position(self, id, dx, dy):
        try:
            ent = self.world.get_entity(id)
            ent.move(dx, dy)
        except (TypeError, AttributeError):
            print(f"what the fuck just happened with {id}")

    def stream_game(self):
        for client in self.server.thread_client_list:
            json_dump = self.world.to_json()
            # print(json_dump)
            client.send_processed_data(json_dump)

    def run_game(self):
        # making players with some distance, probably better way to do it.
        natural_distance = 20
        self.make_entities()
        # stream game once at start
        self.stream_game()
        while True:

            # processing the queue that threaded_clients are filling
            if not self.q.empty():

                dict = self.q.get()
                # sometimes we have none objects that crash the application
                # we skip when dict is none
                if dict is None:
                    continue
                # if new player or movement, stream game
                # TODO: stream game if exit.
                elif "player" in dict:
                    cl = Entity(x=natural_distance,
                                y=natural_distance, char='B', id=dict.get("player"))
                    self.world.entities.append(cl)
                    natural_distance += 20
                    self.stream_game()
                elif "move" in dict:
                    id = dict.get('id')
                    dx, dy = dict.get("move")[0], dict.get("move")[1]
                    self.update_position(id=id, dx=dx, dy=dy)
                    self.stream_game()


game = Game()
game.run_game()
