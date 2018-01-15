#game options and settings
TITLE = 'Exploria'
WIDTH = 1300
HEIGHT = 650
FPS = 60

#Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 14
PLAYER_MAX_HEALTH = 100
FONT_NAME = 'arial'
SPRITESHEET = 'spritesheet_jumper.png'

# Game properties
BOOST_POWER = 10
POW_SPAWN_PCT = 50

# starting platforms
PLATFORM_LIST = [(WIDTH/2-50, 350, 2000, 30),
                 (125, HEIGHT-700, 100, 30),
                 (175, 90, 1000, 30)]

# define common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE


# function to combine sprite rects
def expand_parameters(starting_value, final_length):
    """ takes initial platform parameters, returns list of multiple parameters in form (x, y, z)"""
    ret = [starting_value]
    for i in range(final_length):
        x, y, w, h = starting_value
        x += 5
        ret.append((x, y, w, h))
        starting_value = (x, y, w, h)
    return ret
