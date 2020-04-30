import socket
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

    def receiver(self):
        while True:
            try:
                msg = ""
                rec_char_byte = self.client_socket.recv(1).decode("UTF-8")
                while (rec_char_byte is not '\n'):
                    msg += rec_char_byte
                    rec_char_byte = self.client_socket.recv(1).decode("UTF-8")
                # print("msg   :  " + msg)
                decoded_retour_world = json.loads(msg)
                self.draw(decoded_retour_world, self.window)
                msg = ""
            except Exception as ex:
                print(ex)

    def sender(self):
        while True:
            # try getting the world one byte at a time, until a new line.

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

    # Draw, flush and and calls method clear for all entities

    def draw(self, world, window):
        for entity in world['entities']:
            print(entity)
            libtcod.console_put_char(
                window, entity['x'], entity['y'], entity['char'], libtcod.BKGND_NONE)

        libtcod.console_flush()
        for entity in world['entities']:
            self.clear(entity, self.window)

    def clear(self, entity, window):
        libtcod.console_put_char(
            window, entity['x'], entity['y'], ' ', libtcod.BKGND_NONE)


c = Client()
c.run()
