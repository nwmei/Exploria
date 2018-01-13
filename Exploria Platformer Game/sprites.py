import pygame as pg
from settings import *
import math

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.direction = "right"
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(692, 1458, 120, 207)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.collision = [False] * 8
        self.health = PLAYER_MAX_HEALTH
        self.last_auto_healing = pg.time.get_ticks()

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                         self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = [pg.transform.flip(self.game.spritesheet.get_image(678, 860, 120, 201), True, False),
                              pg.transform.flip(self.game.spritesheet.get_image(692, 1458, 120, 207), True, False)]
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump(self):
        self.game.jump_sound.play()
        self.vel.y = -PLAYER_JUMP

    def under_jump(self):
        """make player jump off current platform"""
        self.pos.y += 1
        platform_collision_indices = self.rect.collidelistall(self.game.platform_rect_list)
        floor_index = self.lower_platform_index(platform_collision_indices)
        self.pos.y -= 1
        if self.game.platform_rect_list[floor_index] != self.game.base_platform.rect and floor_index != -1:
            self.pos = (self.pos[0], self.game.platform_rect_list[floor_index].midbottom[1])

    def lower_platform_index(self, indices):
        """takes in a list of indices of platform rects and return index for platform that player is standing on"""
        if len(indices) == 0:
            floor_index = -1
        elif len(indices) == 1:
            floor_index = indices[0]
        else:
            # check which player is standing on
            floor_index = indices[0]
            for index in indices:
                if self.game.platform_rect_list[index].y > self.game.platform_rect_list[floor_index].y:
                    floor_index = index
        return floor_index

    def update(self):
        self.animate()

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
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # find which platform rect the player is colliding with
        platform_collision_indices = self.rect.collidelistall(self.game.platform_rect_list)

        floor_index = self.lower_platform_index(platform_collision_indices)
        collision_point_list = self.check_collision(self.game.platform_rect_list[floor_index])
        # on top of platform
        if self.pos.x < self.game.platform_rect_list[floor_index].right + 10 and \
            self.pos.x > self.game.platform_rect_list[floor_index].left - 10:
            if (collision_point_list[2] == 1 or collision_point_list[3] == 1 or collision_point_list[7] == 1) \
                    and collision_point_list[5] != 1 and collision_point_list[4] != 1 and self.vel.y > 0:
                self.pos.y = self.game.platform_rect_list[floor_index].top + 1
                self.vel.y = 0

        # auto healing
        now = pg.time.get_ticks()
        if now - self.last_auto_healing > 10000 and self.health < PLAYER_MAX_HEALTH:
            self.last_auto_healing = now
            self.health += 1
            if self.health > 100:
                self.health = 100

    def animate(self):
        now = pg.time.get_ticks()

        # walk animation
        self.walking = True if self.vel.x != 0 else False
        if self.vel.x < 0:
            self.direction = "left"
        elif self.vel.x > 0:
            self.direction = "right"

        if self.walking and self.vel.y == 0:
            if now - self.last_update > 170:
                frame_set = self.walk_frames_l if self.direction == "left" else self.walk_frames_r
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(frame_set)
                bottom = self.rect.bottom
                self.image = frame_set[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif not self.jumping and not self.walking:
            if now - self.last_update > 370:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.game.spritesheet.get_image(692, 1458, 120, 207) if self.direction == "right" \
                    else pg.transform.flip(self.game.spritesheet.get_image(692, 1458, 120, 207), True, False)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


    def check_collision(self, sprite_rect):
        """returns list containing 0s and 1s depending on where player is colliding with platform"""
        self.collision[0] = sprite_rect.collidepoint(self.rect.topleft)
        self.collision[1] = sprite_rect.collidepoint(self.rect.topright)
        self.collision[2] = sprite_rect.collidepoint(self.rect.bottomleft)
        self.collision[3] = sprite_rect.collidepoint(self.rect.bottomright)
        self.collision[4] = sprite_rect.collidepoint(self.rect.midleft)
        self.collision[5] = sprite_rect.collidepoint(self.rect.midright)
        self.collision[6] = sprite_rect.collidepoint(self.rect.midtop)
        self.collision[7] = sprite_rect.collidepoint(self.rect.midbottom)
        return self.collision


class Platform(pg.sprite.Sprite):
    """class for game platforms"""
    def __init__(self, x, y, w, h, game):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(0, 384, 380, 94)
        self.image = pg.transform.scale(self.image, (w, h*2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spritesheet:
    """ utility class for loading and parsing spritesheets """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab image out of spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image

class PowerUp:
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = math.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top -5
        if not self.game.platforms.has(self.plat):
            self.kill()
