from server import *
import queue
from _thread import *
import threading
from entity import Entity
from entity import TargetEntity, WallEntity
from random import randint
from world import World
import json


"""
Main game class that manages the game.
World: manages entities to a list.
Server: manage connections throught threaded clients

TODO:
    1. create walls (Johanna)
    2. make sure objects such as players and walls are untraversable (methods already done in old project) (Johanna)
    3. make score for players (check tutorial part 7)(Aissata)
    4. making winning condition and eventual replay
    5. delete from world all players that are exiting the game
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
        start_new_thread(self.server.run, ())

    # creating map
    def make_map(self):
        #Every second wall will be vertical
        verticalWall = False

        for i in range(self.world.max_walls):
            #Decide where wall should start
            wall_start_x = randint(1, self.world.world_width-5)
            wall_start_y = randint(1, self.world.world_height-5)
            
            #Each wall can consist of 0-7 tiles
            for j in range(randint(0, 7)):
                #add all tiles the wall will consist of
                if (verticalWall):
                    wall_tile = WallEntity(x=wall_start_x, y=wall_start_y + j)
                    self.world.entities.append(wall_tile)
                else:
                    wall_tile = WallEntity(x=wall_start_x + j, y=wall_start_y)
                    self.world.entities.append(wall_tile)
            
            #Switch between horizontal and vertical wall
            if (verticalWall):
                    verticalWall = False
            else: 
                verticalWall = True

    
    # creating targets entities
    def make_entities(self):
    

        for i in range(self.world.max_entities):
            npc = TargetEntity(x=randint(1, self.world.world_width-5), y=randint(
                1, self.world.world_height-5))
            # print(type(npc))
            # if type(npc) is TargetEntity:
            #    print("Capture the flag")
            self.world.entities.append(npc)

    # move the entity by id

    def update_position(self, id, dx, dy):
        try:
            ent = self.world.get_entity(id)
            ent.move(dx, dy)
        except (TypeError, AttributeError):
            print(f"what the fuck just happened with {id}")

    # this method is called everytime a player move,
    # and check if it crossed the path of a target
    def check_for_capture(self, player_id):
        player = self.world.get_entity(player_id)
        pl_x, pl_y = player.get_position()
        for e in self.world.entities:
            # check for every targets if both
            # x and y positions match, print capture message
            # and delete from world
            if type(e) is TargetEntity:
                e_x, e_y = e.get_position()
                if(pl_x == e_x and pl_y == e_y):
                    print(f"Captured {e}!")
                    self.world.entities.remove(e)
                    # todo : if len(self.world.entities) - countplayers == 0
                    # publish scores eller något

    def stream_game(self):
        for client in self.server.thread_client_list:
            json_dump = self.world.to_json()
            # print(json_dump)
            client.send_processed_data(json_dump)

    def run_game(self):
        # making players with some distance, probably better way to do it.
        # first player starts at x = 20, y = 20
        natural_distance = 10
        #create walls 
        self.make_map()
        #create all targetentitites
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
                    self.check_for_capture(id)


game = Game()
game.run_game()
