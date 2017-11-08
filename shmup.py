import pygame
import random
import os
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60

#define common colors5
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "snd")#.replace('\\', '/')

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    """
    sprite for player
    """
    def __init__(self):
        self.height = 40
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((player_img), (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 80

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -3
        if keystate[pygame.K_d]:
            self.speedx = 3
        if keystate[pygame.K_w]:
            self.speedy = -3
        if keystate[pygame.K_s]:
            self.speedy = 3

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #walls
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        laser_snd.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(5)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #respawn
        if ((self.rect.top > HEIGHT) or (self.rect.left < -30) or (self.rect.right > WIDTH+30)) :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5)
            self.speedx = random.randrange(-2,2)

class PassingStars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(-500,-10)
        self.speedy = 50

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH)
            self.rect.y = random.randrange(-500, -10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #delete if goes off screen
        if self.rect.bottom < 0:
            self.kill()

#create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup Game")
clock = pygame.time.Clock()

#load graphics
laser_img = pygame.image.load(path.join(img_folder, "laser.png"))
player_img = pygame.image.load(path.join(img_folder, "ship1.png"))
meteor_img = pygame.image.load(path.join(img_folder, "meteor.png"))

#load sounds
laser_snd = pygame.mixer.Sound(path.join(snd_folder, "laser.wav"))
explosion_snd = pygame.mixer.Sound(path.join(snd_folder, "explosion.wav"))
pygame.mixer.music.load(path.join(snd_folder, 'space_music.mp3'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#create new mobs and aadd to all_sprites and mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#create the passing stars
for star_count in range(50):
    star = PassingStars()
    all_sprites.add(star)

#Game Loop
score = 0
pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update
    all_sprites.update()
    #check if there is collision
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        player.health -= 15
        player.rect.y += 40
        if player.health == 0:
            running = False
    shots = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for shot in shots:
        explosion_snd.play()
        score += 1
        mob = Mob()
        mobs.add(mob)
        all_sprites.add(mob)

    #draw
    screen.fill(BLUE)
    all_sprites.draw(screen)
    score_and_health = 'score: ' + str(score) + '  ' + 'health: ' + str(player.health)
    draw_text(screen,score_and_health, 18, WIDTH/2, 10)

    pygame.display.flip()

pygame.quit()











