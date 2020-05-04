import json


class World:
    def __init__(self):
        # max entities on screen
        self.max_entities = 17
        # world dimentions, must be the same than client's
        self.world_width = 50
        self.world_height = 50
        self.entities = []

    # method that returns entity by ID, we need it to move them around
    # and delete them
    def get_entity(self, id):
        for entity in self.entities:
            if entity.id == id:
                return entity
        return None

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__,
                          sort_keys=True) + "\n"
