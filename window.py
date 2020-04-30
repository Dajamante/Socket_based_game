import tcod as libtcod


class Window:

    def __init__(self):

        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()
        self.screen_width = 50
        self.screen_height = 50
        start(self.screen_width, self.screen_height)


def start(screen_width, screen_height):
    libtcod.console_set_custom_font(
        'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(
        screen_width, screen_height, 'libtcod tutorial game', False)
    con = libtcod.console.Console(screen_width, screen_height)