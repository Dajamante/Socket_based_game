import tcod as libtcod
from random import randint
import json


class Entity:
    """
    A generic object to represent players, walls and target objects.
    They are blocked by default.
    """

    def __init__(self, id, x, y, char='B', color=libtcod.white, blocked=True):
        self.id = id
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocked = blocked

    def get_position(self):
        return (self.x, self.y)

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
        return (self.x, self.y)

    def set_position(self, x, y):
        # Set position of x + dx and y + dy
        self.x = x
        self.y = y

    # return True if an entity is not traversable. This method is to control
    # that players do not run in walls or into each other.
    def get_blocking_entities(self, entities, destination_x, destination_y):
        for entity in entities:
            if entity != self and entity.x == destination_x and entity.y == destination_y:
                return True
        return False

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__,
                          sort_keys=True)


"""
Target entities to be picked.
They have a random color and random moves and are children class of entity.
"""


class TargetEntity(Entity):

    def __init__(self, x, y):
        self.id = 0
        self.char = '@'
        self.rand_color = libtcod.Color(
            randint(0, 255), randint(0, 255), randint(0, 255))
        super().__init__(x=x, y=y, id=self.id, char=self.char,
                         color=self.rand_color, blocked=False)

    def random_move(self, screen_width, screen_height):
        die_x = randint(-1, 1)
        die_y = randint(-1, 1)
        new_pos_x = self.x + die_x
        new_pos_y = self.y + die_y

        if(new_pos_x > 0 and new_pos_x < screen_width and new_pos_y > 0 and new_pos_y < screen_height):
            self.move(die_x, die_y)
        else:
            pass
