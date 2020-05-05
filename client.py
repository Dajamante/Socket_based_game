import socket
from time import gmtime, strftime
import json
import tcod as libtcod
import time
import random
from input_handlers import handle_keys
from entity import Entity
from window import Window
from _thread import *
SERVER = "localhost"
PORT = 65432

"""
Class client.
Sending key press, getting world back one byte at a time.
recv is blocking so the receiving is threaded.
"""


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER, PORT))
        self.addr = (SERVER, PORT)
        self.window = Window()
        self.key = self.window.key
        self.mouse = self.window.mouse
        self.clock = 0

    # send and recv : possible conflict?
    def receiver(self):
        # try getting the world one byte at a time, until a new line.
        while True:
            try:
                msg = ""
                rec_char_byte = self.client_socket.recv(1).decode("ascii")
                while (rec_char_byte is not '\n'):
                    msg += rec_char_byte
                    rec_char_byte = self.client_socket.recv(1).decode("ascii")
                # print("msg   :  " + msg)
                decoded_retour_world = json.loads(msg)
                scores = self.get_scores(decoded_retour_world)
                time = self.get_time(decoded_retour_world)
                
                #Check if there is no winner
                if self.check_winner_exist(decoded_retour_world) == 0:
                    self.draw(decoded_retour_world, self.window, scores, time)
                    msg = ""
                else:
                #There exist a winner, check who one or if there is no winner
                    winner = self.check_winner(decoded_retour_world)
                    if (winner > 0):
                        #there is a winner
                        winner_str = self.get_winner_string(winner)
                        self.draw_finish_screen(
                            decoded_retour_world, self.window, winner_str)
                        msg = ""
                    elif winner == 0:
                        #there is no winner
                        winner_str = "There is no winner"
                        self.draw_finish_screen(
                            decoded_retour_world, self.window, winner_str)
                        msg = ""
                
            except Exception as ex:
                print(ex)
                break

    def sender(self):
        while True:
            # Check for tangenttryckning
            libtcod.sys_check_for_event(
                libtcod.EVENT_KEY_PRESS, self.key, self.mouse)

            # Save action in dictionary
            action = handle_keys(self.key)
            # print(action)

            # if the dictionary in handle keys have key word move:
            if "move" in action:

                # The client sends the move dictionary to the server
                # in the form of a json object
                json_dump = json.dumps(action).encode('utf-8')
                # print(json_dump)
                self.client_socket.sendall(json_dump)

            # if the dictionary in handle keys have key word exit we close the window:
            if "exit" in action:
                print("Thank you for playing, good bye.")
                self.client_socket.close()
                break

    def run(self):
        # msg = "String sent from client"
        start_new_thread(self.receiver, ())
        self.sender()

    def get_scores(self, world):
        scores = ""
        for entity in world['entities']:
            print(entity)
            if "id" in entity:
                scores += "Player " + \
                    str(entity['id']) + " : " + \
                    str(entity["points"]) + " points\n"
                print(scores)
        return scores

    def get_time(self, world):
        return "Time  " + str(world['clock'])

    # Check if there is a winner and return the id
    def check_winner(self, world):
        if world['winners_id'] == 0:
            return 0
        else:
            return world["winners_id"]
    
    # Check if a winner exits 
    def check_winner_exist(self, world):
        if world['winner_exist'] == 1:
            return 1
        else:
            return 0
        

    def get_winner_string(self, winner):
        return "The winner is " + str(winner)


    def draw(self, world, window, scores, time):
        libtcod.console_print(window, 5, 45, scores)
        libtcod.console_print(window, 5, 47, time)

        for entity in world['entities']:
            # print(entity)
            libtcod.console_set_default_foreground(window, entity['color'])
            libtcod.console_put_char(
                window, entity['x'], entity['y'], entity['char'], libtcod.BKGND_NONE)
        libtcod.console_flush()
        for entity in world['entities']:
            self.clear(entity, self.window)

    def clear(self, entity, window):
        libtcod.console_put_char(
            window, entity['x'], entity['y'], ' ', libtcod.BKGND_NONE)

    def draw_finish_screen(self, world, window, winner):
        for entity in world['entities']:
            self.clear(entity, self.window)

        libtcod.console_print(window, 20, 20, winner)
        libtcod.console_flush()
    


c = Client()
c.run()
