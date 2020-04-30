import socket
import json
import tcod as libtcod
import time
import random
from input_handlers import handle_keys
from entity import Entity
from window import Window

SERVER = "localhost"
PORT = 65432


class Client:
    def __init__(self, id):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((SERVER, PORT))
        self.addr = (SERVER, PORT)
        self.window = Window()
        self.key = self.window.key
        self.mouse = self.window.mouse

        #Kommer vi att behöva göra detta?? Kommer inte game bara skicka oss vår spelare?
        #Initiate the player for which belongs to this client
        self.entity = Entity(id=id, x=20, y=20+id, char='B',
                             color=libtcod.white, blocked=True)

    def run(self):
        #msg = "String sent from client"

        while True:
            time.sleep(0.15)
            # self.s.send(msg.encode('ascii'))
            # retour = self.s.recv(1024)

            # Ping back to client
            #print("Printing from client: " + str(retour))

            while True:

                # The ServerPlayer (a representation of the client on the server)
                # sends back a json object, the world with all entities
                retour_world = self.s.recv(1024)

                #Decode the message receive
                try:
                    decoded_retour_world = json.loads(
                        retour_world.decode('utf-8'))
                    print(f"Received back from server: {decoded_retour_world}")
                    print(decoded_retour_world)
                    self.draw(decoded_retour_world, self.window)
                except Exception as ex:
                    print(ex)


                #Check for tangenttryckning
                libtcod.sys_check_for_event(
                    libtcod.EVENT_KEY_PRESS, self.key, self.mouse)
                
                #Save action in dictionary
                action = handle_keys(self.key)

                # if the dictionary in handle keys have key word move:
                if "move" in action:
                    
                    # The client sends the move dictionary to the server
                    # in the form of a json object
                    json_dump = json.dumps(action).encode('utf-8')
                    self.s.sendall(json_dump)

                # if the dictionary in handle keys have key word exit we close the window:
                if "exit" in action:
                    print("Thank you for playing, good bye.")
                    self.s.close()
                    break

            self.s.close()


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



r = random.randint(0,5)
c = Client(r)
c.run()
