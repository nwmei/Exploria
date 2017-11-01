import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

#define common colors5
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Player(pygame.sprite.Sprite):
    """
    sprite for player
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.xdirection = 1
        self.ydirection = 1

    def update(self):
        if self.rect.right > WIDTH:
            self.xdirection = -1
            self.image.fill(BLUE)
        elif self.rect.left < 0:
            self.xdirection = 1
            self.image.fill(WHITE)
        elif self.rect.y > HEIGHT:
            self.ydirection = -1
            self.image.fill(RED)
        elif self.rect.y < 0:
            self.ydirection = 1
        speed = 5
        self.rect.x += self.xdirection * speed
        self.rect.y += self.ydirection * speed

#create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Exploria")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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











