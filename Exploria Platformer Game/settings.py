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

#starting platforms
PLATFORM_LIST = [(WIDTH/2-50, HEIGHT*3/4-50, 1000, 30),
                 (0, HEIGHT*1/3+50, 800, 30),
                 (125, HEIGHT-700, 100, 30),
                 (175, 90, 1000, 30)]

#define common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
