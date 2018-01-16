#game options and settings
TITLE = 'Exploria'
WIDTH = 1350
HEIGHT = 720
FPS = 60

#Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 14
PLAYER_MAX_HEALTH = 100
FONT_NAME = 'arial'
SPRITESHEET = 'spritesheet_jumper.png'
TILES_SPRITESHEET = 'tiles_spritesheet.png'

# Game properties
BOOST_POWER = 10
POW_SPAWN_PCT = 50

# starting platforms
PLATFORM_LIST = [(500, 300, 25, 30),
                 (500, -20, 25, 30),
                 (330, 155, 2, 0),
                 (330, 455, 2, 0),
                 (670+70*23, 155, 2, 0),
                 (670+70*23, 455, 2, 0)]
BASE_PLATFORM = (-600, 620, 50, 5)

# define common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
