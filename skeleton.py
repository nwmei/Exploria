import pygame
import random

WIDTH = 500
HEIGHT = 480
FPS = 30

#define common colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Exploria")
clock = pygame.time.Clock()

#Game Loop
running = True
while running:
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    #draw
    screen.fill(BLACK)

    pygame.display.flip()

pygame.quit()











