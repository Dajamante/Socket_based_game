from server import *
import queue
import time
from _thread import *
import threading
from entity import Entity
from entity import TargetEntity, PlayerEntity, WallEntity
from random import randint
from world import World
import json
import sys


"""
Main game class that manages the game.
World: manages entities to a list.
Server: manage connections throught threaded clients

TODO:
    4. rapport
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
        self.last_streamed = None

    # creating map
    # hard-coded height on which walls and entities appear to not
    # interfer with score lines

    def make_map(self):
        # Every second wall will be vertical
        verticalWall = False

        for i in range(self.world.max_walls):
            # Decide where wall should start
            wall_start_x = randint(1, self.world.world_width-5)
            wall_start_y = randint(1, self.world.world_height-15)

            # Each wall can consist of 0-7 tiles
            for j in range(randint(0, 7)):
                # add all tiles the wall will consist of
                if (verticalWall):
                    wall_tile = WallEntity(x=wall_start_x, y=wall_start_y + j)
                    self.world.entities.append(wall_tile)
                else:
                    wall_tile = WallEntity(x=wall_start_x + j, y=wall_start_y)
                    self.world.entities.append(wall_tile)

            # Switch between horizontal and vertical wall
            if (verticalWall):
                verticalWall = False
            else:
                verticalWall = True

    # creating targets entities
    def make_entities(self):
        i = 0
        while i < self.world.max_entities:
            # hardcoded height of spawning to not interfer with score line
            npc = TargetEntity(x=randint(1, self.world.world_width-5), y=randint(
                1, self.world.world_height-15))
            if not npc.is_already_occupied(self.world):
                self.world.entities.append(npc)
                i += 1
            else:
                pass

    # move the entity by id if it does not hit wall
    def update_position(self, player_id, dx, dy):
        entity_player = self.world.get_entity(player_id)
        print("Tries to update position")
        if not entity_player.has_hinder(self.world, dx, dy):
            print("Has checked if wall")
            entity_player.move(dx, dy)

    def update_score(self, player_id):
        player = self.world.get_entity(player_id)
        print(player)
        player.points += 1

    # this method is called everytime a player move,
    # and check if it crossed the path of a target
    def check_for_capture(self, player_id):
        print("what is player id? : " + str(player_id))

        player = self.world.get_entity(player_id)
        print(f"fetched object? {player}")
        print(f"type of fetch object? {type(player)}")
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
                    self.update_score(player_id)
                    # todo : if len(self.world.entities) - countplayers == 0
                    # publish scores eller något

    def check_winner(self):
        self.world.winner_exist = 1
        winner = None
        winners_id = 0
        # check if any player has 0 points, then do not update
        for e in self.world.entities:
            if type(e) is PlayerEntity:
                if(e.points is 0):
                    return winners_id

        # check which player has most points
        for e in self.world.entities:
            if type(e) is PlayerEntity:
                if (winner == None):
                    winner = e
                    winners_id = e.id
                elif e.points > winner.points:
                    winners_id = e.id
                else:
                    break

        return winners_id

    def stream_game(self):
        json_dump = self.world.to_json()

        for client in self.server.thread_client_list:
            # flagged closed clients
            if client.open == False:
                self.server.thread_client_list.remove(client)
                id_remove = client.id
                entity = self.world.get_entity(id_remove)
                self.world.entities.remove(entity)
            elif json_dump != self.last_streamed:
                client.send_processed_data(json_dump)

        self.last_streamed = json_dump

    def run_game(self):
        # initiate clock
        start = time.time()
        time_left = True
        # making players with some distance, probably better way to do it.
        # first player starts at x = 20, y = 20
        natural_distance = 10
        # create walls
        self.make_map()
        # create all targetentitites
        self.make_entities()
        # stream game once at start
        self.stream_game()

        while time_left:
            end = time.time()
            self.stream_game()
            self.world.clock = round(end - start, 0)
            # more than 40 seconds was just unbearable.
            if (end - start) > 40:
                time_left = False

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
                    cl = PlayerEntity(x=natural_distance,
                                      y=natural_distance, char='B', id=dict.get("player"))
                    self.world.entities.append(cl)
                    natural_distance += natural_distance

                elif "move" in dict:
                    id = dict.get('id')
                    dx, dy = dict.get("move")[0], dict.get("move")[1]
                    self.update_position(player_id=id, dx=dx, dy=dy)
                    self.stream_game()
                    print("id will be checked for capture : " + str(id))
                    self.check_for_capture(id)

        self.world.winners_id = self.check_winner()
        while not time_left:
            self.stream_game()
            print('I have sent the winner to client')


game = Game()
game.run_game()
