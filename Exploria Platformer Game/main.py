#Exploria Platform Game
import pygame as pg
import random
import os
from settings import *
from sprites import *


class Game:
    def __init__(self):
        """initialize game window, etc"""
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.last_vertical_correction = pg.time.get_ticks()
        self.platform_rect_list = []

    def new(self):
        """start a new game"""
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # create platforms, starting with base
        self.base_platform = Platform(-3000, HEIGHT-40, 16350, 300) #width was W*10
        self.all_sprites.add(self.base_platform)
        self.platforms.add(self.base_platform)
        self.platform_rect_list.append(self.base_platform.rect)
        # other platforms
        for platform in PLATFORM_LIST:
            plat = Platform(*platform)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            self.platform_rect_list.append(plat.rect)
        self.run()
    
    def run(self):
        """game loop"""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        """game loop update"""
        self.all_sprites.update()
        # # if player hits surface of platform
        # if self.player.vel.y > 0:
        #     hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        #     if hits:
        #         self.player.pos.y = hits[0].rect.top+1
        #         self.player.vel.y = 0
        # # if player hits bottom of platform (from jumping)
        # if self.player.vel.y < 0:
        #     hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        #     if hits:
        #         self.player.pos.y = hits[0].rect.bottom+40
        #         self.player.vel.y = 0

        # if player hits side of platforms
        platform_collision_index = self.player.rect.collidelist(self.platform_rect_list)

        collision_point_list = self.player.check_collision(self.platform_rect_list[platform_collision_index])

        # left side
        if collision_point_list[5] == 1 and self.player.vel.x > 0:
            self.player.pos.x = self.platform_rect_list[platform_collision_index].left - 1
            self.player.vel.x = 0

        # right side
        if collision_point_list[4] == 1 and self.player.vel.x < 0:
            self.player.pos.x = self.platform_rect_list[platform_collision_index].right + 1
            self.player.vel.x = 0

        # on top of platform
        if (collision_point_list[2] == 1 or collision_point_list[3] == 1 or collision_point_list[7] == 1) \
                and self.player.vel.y > 0:
            self.player.pos.y = self.platform_rect_list[platform_collision_index].top + 1
            self.player.vel.y = 0

        # under platform
        if (collision_point_list[0] == 1 or collision_point_list[1] == 1 or collision_point_list[6] == 1) \
                and self.player.vel.y < 0:
            self.player.pos.y = self.platform_rect_list[platform_collision_index].bottom - 1
            self.player.vel.y = 0

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT/6 or self.player.rect.top >= HEIGHT/2:
            self.player.pos.y -= self.player.vel.y
            for platform in self.platforms:
                platform.rect.y -= self.player.vel.y

        # correction of y coordinates of player
        now = pg.time.get_ticks()
        if now - self.last_vertical_correction > 10:
            self.last_vertical_correction = now
            if abs(self.player.pos.y - HEIGHT/2) > 2:
                if HEIGHT/2 - self.player.pos.y < 0:
                    sign = -1
                else:
                    sign = 1
                self.player.pos.y += sign
                for platform in self.platforms:
                    platform.rect.y += sign

        # scroll map horizontally while player moves
        self.player.pos.x -= self.player.vel.x
        for platform in self.platforms:
            platform.rect.x -= int(self.player.vel.x)

    def events(self):
        """game loop events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.player.vel.y == 0:
                        self.player.jump()
    
    def draw(self):
        """game loop draw"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        """game start screen"""
        pass

    def show_go_screen(self):
        """game over screen"""
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen

pg.quit()

    
