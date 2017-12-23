import pygame
import random
import os
from os import path

# Tutorial from: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
#Oceanography Pollution Game, a version of Shmup
#BU ES144

WIDTH = 600 #was 480
HEIGHT = 700 #was 600
FPS = 60

#spritesheets
POLLUTION_SPRITESHEET = 'pollution.png'

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
snd_folder = os.path.join(game_folder, "snd")

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def draw_GO_screen():
    fact_list = []
    fact_list.append("Toxic chemicals will negatively impact plankton")
    fact_list.append("Pesticides get into the ocean, the entire food web can be effected")
    fact_list.append("Other causes of marine pollution: wind-blown debris, dust")
    fact_list.append("80% of marine pollution comes from land")
    screen.blit(background, background_rect)
    draw_text(screen, "Oceanography Game", 55, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH/2, HEIGHT/2,WHITE)
    draw_text(screen, 'Press SPACEBAR to begin', 18, WIDTH/2, HEIGHT/2 + 30,WHITE)
    draw_text(screen, 'You saved ' + str(global_fish_saved) + ' fish. Do better!', 18, WIDTH/2, HEIGHT/2 + 60 + 30,WHITE)
    draw_text(screen, 'Fun Fact: ', 18, WIDTH/2, HEIGHT/2 + 200,BLACK)
    draw_text(screen, random.choice(fact_list), 18, WIDTH / 2, HEIGHT / 2 + 230, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                waiting = False


def newmob():
    mob = Mob()
    mobs.add(mob)
    all_sprites.add(mob)

def newFish():
    fish = Fish()
    all_fish.add(fish)
    all_sprites.add(fish)

def draw_shield_bar(surf, x, y, percentage):
    if percentage < 0:
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf,WHITE, outline_rect, 2)

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(path.join(img_folder, filename))

    def get_image(self, x, y, width, height):
        # extract image out of spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image


class Player(pygame.sprite.Sprite):
    """
    sprite for player
    """
    def __init__(self):
        self.height = 40
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((player_img), (60,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.fish_saved = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -3
        if keystate[pygame.K_RIGHT]:
            self.speedx = 3
        if keystate[pygame.K_UP]:
            self.speedy = -3
        if keystate[pygame.K_DOWN]:
            self.speedy = 3
        if keystate[pygame.K_SPACE]:
            self.shoot()

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
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser_snd.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(fish_image_list), (50, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #respawn
        if ((self.rect.top > HEIGHT) or (self.rect.left < -30) or (self.rect.right > WIDTH+30)) :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
            self.speedx = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((random.choice(pollution_image_list)), (25, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 2)
        self.speedx = random.randrange(-1, 1)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #respawn
        if ((self.rect.top > HEIGHT) or (self.rect.left < -30) or (self.rect.right > WIDTH+30)) :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)
            self.speedx = random.randrange(-2, 2)

class PassingStars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,3))
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
        self.speedy = -6

    def update(self):
        self.rect.y += self.speedy
        #delete if goes off screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Blood(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = blood_image_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(blood_image_list):
                self.kill()
            else:
                center = self.rect.center
                self.image = blood_image_list[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
#create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oceanagraphy Pollution Game")
clock = pygame.time.Clock()

#load graphics
background = pygame.image.load(path.join(img_folder, "island.xcf")).convert()
background_rect = background.get_rect()

laser_img = pygame.image.load(path.join(img_folder, "laser.png"))
player_img = pygame.image.load(path.join(img_folder, "ship1.png"))
meteor_img = pygame.image.load(path.join(img_folder, "meteor.png"))

pollution_sheet = Spritesheet(POLLUTION_SPRITESHEET)
pollution_image_list = []
pollution_image_list.append(pollution_sheet.get_image(19, 7, 39, 55))
pollution_image_list.append(pollution_sheet.get_image(243, 12, 17, 50))
pollution_image_list.append(pollution_sheet.get_image(287, 13, 16, 49))
pollution_image_list.append(pollution_sheet.get_image(98, 14, 51, 48))
pollution_image_list.append(pollution_sheet.get_image(206, 16, 35, 46))
pollution_image_list.append(pollution_sheet.get_image(2, 17, 15, 45))
pollution_image_list.append(pollution_sheet.get_image(373, 17, 28, 45))
pollution_image_list.append(pollution_sheet.get_image(60, 18, 36, 44))
pollution_image_list.append(pollution_sheet.get_image(330, 22, 21, 40))
pollution_image_list.append(pollution_sheet.get_image(496, 22, 17, 40))
pollution_image_list.append(pollution_sheet.get_image(262, 27, 23, 35))
pollution_image_list.append(pollution_sheet.get_image(353, 28, 18, 34))
pollution_image_list.append(pollution_sheet.get_image(305, 32, 23, 30))
pollution_image_list.append(pollution_sheet.get_image(403, 32, 60, 30))
pollution_image_list.append(pollution_sheet.get_image(151, 34, 53, 28))
pollution_image_list.append(pollution_sheet.get_image(465, 36, 29, 26))

fish_sheet = Spritesheet("fish.png")
fish_image_list = []
fish_image_list.append(fish_sheet.get_image(9, 0, 18, 32))
fish_image_list.append(fish_sheet.get_image(192, 0, 32, 32))
fish_image_list.append(fish_sheet.get_image(107, 1, 21, 31))
fish_image_list.append(pygame.transform.rotate(fish_sheet.get_image(35, 224, 26, 32), 180))
fish_image_list.append(pygame.transform.rotate(fish_sheet.get_image(198, 224, 18, 32), 180))

blood_sheet = Spritesheet("blood.png")
blood_image_list = []
start = 0
for x in range(15):
    image = blood_sheet.get_image(start, 0, 480, 480)
    image.set_colorkey(BLACK)
    blood_image_list.append(pygame.transform.scale(image, (80, 80)))
    start += 480

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(7):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename))
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

#load sounds
laser_snd = pygame.mixer.Sound(path.join(snd_folder, "laser.wav"))
laser_snd.set_volume(0.5)
explosion_snd = pygame.mixer.Sound(path.join(snd_folder, "explosion.wav"))
pygame.mixer.music.load(path.join(snd_folder, 'space_music.mp3'))
pygame.mixer.music.set_volume(0.01)


#Game Loop
score = 0
fish_killed = 0
pygame.mixer.music.play(loops=-1)
game_over = True
running = True
global_fish_saved = 0
while running:
    if game_over:
        draw_GO_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        all_fish = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # create new mobs and add to all_sprites and mobs
        for i in range(5):
            newmob()
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()
    #check if there is collision
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) #if player and mob collide
    for hit in hits:
        expl = Explosion(player.rect.center, 'sm')
        all_sprites.add(expl)
        player.shield -= random.randrange(15, 25)
        player.rect.y += 40
        newmob()
        if player.shield <= 0:
            game_over = True
    shots = pygame.sprite.groupcollide(bullets, mobs, True, True) #if bullet and mob collide
    for shot in shots:
        explosion_snd.play()
        expl = Explosion(shot.rect.center, random.choice(['lg', 'sm']))
        all_sprites.add(expl)
        score += 1
        if random.choice([True, False, False]):
            newFish()
            player.fish_saved += 1
            global_fish_saved += 1
        newmob()

    kills = pygame.sprite.groupcollide(bullets, all_fish, True, True) #if bullet and fish collide
    for kill in kills:
        explosion_snd.play()
        blood = Blood(kill.rect.center)
        all_sprites.add(blood)
        score -= 1
        player.fish_saved -= 1
        global_fish_saved -= 1
        fish_killed += 1


    #draw
    screen.fill(BLUE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    top_text = 'health: ' + str(player.shield) + '   fish saved: ' + str(player.fish_saved) + '   fish killed:  = ' + str(fish_killed)
    draw_text(screen,top_text, 22, WIDTH/2, 10, BLACK)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()

pygame.quit()











