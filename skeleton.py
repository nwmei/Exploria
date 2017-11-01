import pygame
import random
import os


WIDTH = 800
HEIGHT = 600
FPS = 30

#define common colors5
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


class Player(pygame.sprite.Sprite):
    """
    sprite for player
    """
    def __init__(self,file):
        pygame.sprite.Sprite.__init__(self)
        self.file = file
        self.image = pygame.image.load(os.path.join(img_folder, self.file)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WIDTH), random.randint(0,HEIGHT))
        self.xdirection = 1
        self.ydirection = 1

    def update(self):
        if self.rect.right > WIDTH:
            self.xdirection = random.randint(-5,-1)
        elif self.rect.left < 0:
            self.xdirection = random.randint(1,5)
        elif self.rect.y > HEIGHT:
            self.ydirection = random.randint(-5,-1)
        elif self.rect.y < 0:
            self.ydirection = random.randint(1,5)
        speed = 6
        self.rect.x += self.xdirection * speed
        self.rect.y += self.ydirection * speed

#create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Exploria Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player("peter.jpeg")
cop = Player("copcar.png")
all_sprites.add(player,cop)

#Game Loop
running = True
while running:
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    all_sprites.update()
    #draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()











