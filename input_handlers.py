import tcod as libtcod

"""
handle_keys method: return a python dictionary with dx, dy
This class comes from the tutorial TCOD
"""


def handle_keys(key):
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return{'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # no key pressed
    return {}
