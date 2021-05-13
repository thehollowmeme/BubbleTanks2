from .resolution import get_resolution


# screen
SCR_W, SCR_H = get_resolution()
SCR_W2 = SCR_W // 2
SCR_H2 = SCR_H // 2
SCR_SIZE = (SCR_W, SCR_H)
HEIGHT_SCALE_FACTOR = SCR_H / 960
WIDTH_SCALE_FACTOR = SCR_W / 1280

# animation states
OPEN = 1
WAIT = 0
CLOSE = -1

# upgrade buttons
UPG_BUTTON_LEFT = 0
UPG_BUTTON_CENTER = 1
UPG_BUTTON_RIGHT = 2
UPG_BUTTON_WIDE_LEFT = 3
UPG_BUTTON_WIDE_RIGHT = 4

# popup window
WINDOW_CLOSED = 0
WINDOW_OPENING = 1
WINDOW_CLOSING = 2
WINDOW_OPENED = 3

# game
ROOM_RADIUS = int(7/6 * SCR_H)
DIST_BETWEEN_ROOMS = 2 * ROOM_RADIUS + SCR_W2
TRANSPORTATION_TIME = 600
MU = 0.00064

# room
BOSS_IS_FAR_AWAY = 0
BOSS_IN_NEIGHBOUR_ROOM = 1
BOSS_IN_CURRENT_ROOM = 2

# main menu
class State:
    MAIN_MENU = 0
    SETTINGS = 1
    LANGUAGES = 2
    RESOLUTIONS = 3
    EXIT_CONFIRMATION = 4


__all__ = [

    "SCR_W",
    "SCR_H",
    "SCR_W2",
    "SCR_H2",
    "SCR_SIZE",
    "OPEN",
    "CLOSE",
    "WAIT",
    "ROOM_RADIUS",
    "DIST_BETWEEN_ROOMS",
    "TRANSPORTATION_TIME",
    "MU",
    "BOSS_IS_FAR_AWAY",
    "BOSS_IN_NEIGHBOUR_ROOM",
    "BOSS_IN_CURRENT_ROOM",
    "WINDOW_CLOSED",
    "WINDOW_OPENING",
    "WINDOW_CLOSING",
    "WINDOW_OPENED",
    "UPG_BUTTON_LEFT",
    "UPG_BUTTON_CENTER",
    "UPG_BUTTON_RIGHT",
    "UPG_BUTTON_WIDE_LEFT",
    "UPG_BUTTON_WIDE_RIGHT",
    "HEIGHT_SCALE_FACTOR",
    "WIDTH_SCALE_FACTOR",
    "State"

]
