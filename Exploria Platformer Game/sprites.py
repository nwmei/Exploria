import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.collision = [False] * 9

    def jump(self):
        self.vel.y = -14

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos

    def check_collision(self, platform_rect):
        self.collision[0] = platform_rect.collidepoint(self.rect.topleft)
        self.collision[1] = platform_rect.collidepoint(self.rect.topright)
        self.collision[2] = platform_rect.collidepoint(self.rect.bottomleft)
        self.collision[3] = platform_rect.collidepoint(self.rect.bottomright)
        self.collision[4] = platform_rect.collidepoint(self.rect.midleft)
        self.collision[5] = platform_rect.collidepoint(self.rect.midright)
        self.collision[6] = platform_rect.collidepoint(self.rect.midtop)
        self.collision[7] = platform_rect.collidepoint(self.rect.midbottom)
        return self.collision

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
