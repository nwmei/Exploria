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
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
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
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # find which platform rect the player is colliding with
        platform_collision_index = self.rect.collidelist(self.game.platform_rect_list)
        collision_point_list = self.check_collision(self.game.platform_rect_list[platform_collision_index])

        # on top of platform
        if (collision_point_list[2] == 1 or collision_point_list[3] == 1 or collision_point_list[7] == 1) \
                and collision_point_list[5] != 1 and collision_point_list[4] != 1 and self.vel.y > 0:
            self.pos.y = self.game.platform_rect_list[platform_collision_index].top + 1
            self.vel.y = 0
        # under platform
        if (collision_point_list[0] == 1 or collision_point_list[1] == 1 or collision_point_list[6] == 1) \
                and collision_point_list[5] != 1 and collision_point_list[4] != 1 and self.vel.y < 0:
            self.pos.y = self.game.platform_rect_list[platform_collision_index].bottom + 40
            self.vel.y = 0
        # left side
        if collision_point_list[5] == 1 and self.vel.x > 0:
            self.pos.x = self.game.platform_rect_list[platform_collision_index].left - 1
            self.vel.x = 0
        # right side
        if collision_point_list[4] == 1 and self.vel.x < 0:
            self.pos.x = self.game.platform_rect_list[platform_collision_index].right + 1
            self.vel.x = 0


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
