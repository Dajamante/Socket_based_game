import tcod as libtcod

"""
window object of client.
Make sure that the screen width and height are the same than the world's (server)
"""


class Window:

    def __init__(self, width=50, height=50):

        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()
        self.screen_width = width
        self.screen_height = height
        start(self.screen_width, self.screen_height)


def start(screen_width, screen_height):
    libtcod.console_set_custom_font(
        'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(
        screen_width, screen_height, 'Jompai game', False)
    con = libtcod.console.Console(screen_width, screen_height)
