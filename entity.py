import tcod as libtcod


class Entity:
    """
    A generic object to represent players (at the moment).
    """

    def __init__(self, id,  x, y, char, color=libtcod.white, blocked=True):
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

    # return True if an entity is not traversable.
    def get_blocking_entities(self, entities, destination_x, destination_y):
        for entity in entities:
            if entity != self and entity.x == destination_x and entity.y == destination_y:
                return True
        return False
