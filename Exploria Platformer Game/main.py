import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *

# Exploria Platform Game

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
        self.platform_distances_from_base = []
        self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        """start a new game"""
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # create platforms, starting with base
        self.base_platform = Platform(-3000, HEIGHT-40, 16350, 300, self)
        self.all_sprites.add(self.base_platform)
        self.platforms.add(self.base_platform)
        self.platform_rect_list.append(self.base_platform.rect)
        self.platform_distances_from_base.append(0)

        # other platforms
        for platform in PLATFORM_LIST:
            x, y, w, h = platform
            plat = Platform(x, y, w, h, self)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            # created a list of plat rects so that program can refer to them in the
            # order that they were created. iterating through a sprite group does not
            # always happen in the order that sprites were added to the group. The elements
            # in the rect list point to the actual rects of the platforms (mutable).
            self.platform_rect_list.append(plat.rect)
            # platform distances list indices correspond to rect list.
            self.platform_distances_from_base.append(self.base_platform.rect.y - plat.rect.y)

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

        # scroll map vertically while player moves
        if self.player.rect.top <= HEIGHT/6 or self.player.rect.top >= HEIGHT/2:
            self.player.pos.y -= self.player.vel.y
            for platform in self.platforms:
                platform.rect.y -= self.player.vel.y

        # scroll map horizontally while player moves
        self.player.pos.x -= self.player.vel.x
        for platform in self.platforms:
            platform.rect.x -= int(self.player.vel.x)

        # scheduled correction of y coordinates of all sprites
        now = pg.time.get_ticks()
        if now - self.last_vertical_correction > 10:
            self.last_vertical_correction = now
            if abs(self.player.pos.y - HEIGHT/2) > 2:
                if HEIGHT/2 - self.player.pos.y < 0:
                    sign = -2
                else:
                    sign = 2
                self.player.pos.y += sign
                for platform in self.platforms:
                    platform.rect.y += sign
                # fix distance from base platform to other platforms
                # just refer to the rects in the rect list
                for iteration in range(len(self.platform_rect_list)):
                    self.platform_rect_list[iteration].y = self.base_platform.rect.y - self.platform_distances_from_base[iteration]

    def events(self):
        """game loop events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.player.vel.y == 0:
                        self.player.jump()
                if event.key == pg.K_DOWN:
                    self.player.under_jump()
    
    def draw(self):
        """game loop draw"""
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text('Health: '+str(self.player.health), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()

    def show_start_screen(self):
        """game start screen"""
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """game over screen"""
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

    
