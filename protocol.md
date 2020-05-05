Protocol

1. Data exchange:

   We chose to communicate with json because it's universal and easy to debug. We are sending hashmaps (Python dictionaries) in both direction. Json was well adapted for this purpose as the data is small. Our game instantiate a world object which has a list of entities, that is distributed to every connected clients (sys.getsizeof() gives that the size of the world in bytes is smaller than 4000)

   ### Client

   The client is instantiated with a socket, and connects to a server (in our case "localhost" and non priority-port).

```python
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client_socket.connect((SERVER, PORT))
```

Keypresses are handled by the client, saved in a hashmap (Python dictionary) and sent to the server in json format. The dictionary are encoded in UTF-8.
It is impossible to crash the client by sending bad data, since it will send only keypress up-down-left-right and exit signal.

```python
if "move" in action:
    json_dump = json.dumps(action).encode('utf-8')
    self.client_socket.sendall(json_dump)

if "exit" in action:
    self.client_socket.close()
    break
```

### Server

The server has also a listening socket that receives all incoming connections. It also has a queue for operations that will be processed by the main game loop, and a list of threaded clients, to organize distribution to all connected clients.

```python
self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.server_socket.bind((SERVER, PORT))
self.server_socket.listen()
self.queue = queue
```

It creates a threaded_client object (as the name explains, it is a representation of the client on the server, set in a thread). This threaded client takes the data from the actual client and put it in a dictionary. The dictionary is updated with the client id number.
All the instructions are then put in a queue for processing by the game logic.

// rutor och hur man rör sig mellan olika states

1. Innehålla ett tillståndsdiagram (state diagram) som beskriver vilka tillstånd klienten och servern kan ha samt vad som gör att de övergår från ett tillstånd till ett annat.
2. Vara så detaljerat att en godtycklig student som har klarat kursen kan bygga en ny klient som fungerar med din server utifrån endast protokollet.
   Protokollet ska dessutom uppfylla följande krav:
3. Protokollet ska antingen skicka text (ASCII, ISO8859-1 eller helst UTF8) eller vara binärt.
4. Ha viss datasäkerhet. Det ska inte gå att krascha servern (eller klienten) genom att skicka trasig data. Ni behöver inte skydda er mot timingattacker.
5. Protokollet får inte vara programspråkspecifikt. Det är till exempel inte tillåtet att förvänta sig att mottagaren automatiskt kan deserialisera ett Python-objekt.
6. Protokollet ska delas upp i olika funktioner/metoder.
