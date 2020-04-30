import json


class World:
    def __init__(self):
        # max entities on screen
        self.max_entities = 10
        # world dimentions
        self.world_width = 100
        self.world_height = 100
        self.entities = []

    def to_json(self):
        return json.dumps(self.entities, default=lambda obj: obj.__dict__,
                          sort_keys=True) + "\n"
