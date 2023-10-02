import sys
import os
import math
import random
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import Player, Moveable, Player2
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.UI import Heart
from scripts.states import MainMenu

class Game:
    def __init__(self):
        '''
        initializes Game
        '''
        pygame.init()

        # change the window caption
        pygame.display.set_caption("PongPy")
        # create window
        self.screen = pygame.display.set_mode((640, 480)) # (640, 480), (960, 720), (768, 576)

        self.display_white = pygame.Surface((320, 240), pygame.SRCALPHA) # render on smaller resolution then scale it up to bigger screen

        self.display_2 = pygame.Surface((320, 240))


        self.clock = pygame.time.Clock()
        self.escaped = 0
        
        self.movement = [False, False, False, False] 

        self.assets = {
            'player': load_image('entities/player/player.png'),
            'background': load_image('background.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=1),
            'player2/idle': Animation(load_images('entities/player/idle'), img_dur=1),
            'moveable/idle': Animation(load_images('entities/moveable/idle')),
        }

        # initalizing player
        self.player = Player(self, (self.display_white.get_width()/2, self.display_white.get_height()/2), (5, 20))

        # get player 2 by connecting to server
        self.player2 = Player2(self, (self.display_white.get_width()/2, self.display_white.get_height()/2), (5, 20))

        self.menu = MainMenu(self, self.display_2)

        # initalizing tilemap
        self.tilemap = Tilemap(self, tile_size=16)

        # loading the level
        self.load_level(0)  # self.load_level(self.level), hard coding to 1 atm

        # screen shake
        self.screenshake = 0


    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        # keep track
        self.particles = []

        # creating 'camera' 
        self.scroll = [0, 0]

        self.sparks = []
        
        # spawn the ememies
        self.moveable = []

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)]):
            if spawner['variant'] == 0: 
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.player2.pos = spawner['pos']
            else:
                self.moveable.append(Moveable(self, spawner['pos'], (5,5)))

    def run(self):
        '''
        runs the Game
        '''

        # creating an infinite game loop
        while True:

            self.menu.enter()


            self.display_white.fill((255, 255, 255, 0))    # black outlines
            # clear the screen for new image generation in loopd
            self.display_2.blit(self.assets['background'], (0,0)) # no outline

            self.screenshake = max(0, self.screenshake-1) # resets screenshake value

            # move 'camera' to focus on player, make him the center of the screen
            self.scroll[0] += (- self.scroll[0])  / 30  # x axis
            self.scroll[1] += (- self.scroll[1]) / 30

            # fix the jitter
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display_2, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.player.render(self.display_white, offset=render_scroll)

            # get movement from server
            self.player2.update(self.tilemap, (0,0))
            self.player2.render(self.display_white, offset=render_scroll)

            # for testing
            pygame.draw.rect(self.display_white, (0, 255, 0), (self.player.pos[0] - render_scroll[0], self.player.pos[1] - render_scroll[1], self.player.size[0], self.player.size[1]), 2)
            
            for puck in self.moveable.copy():
                puck.update(self.tilemap, (0,0))
                puck.render(self.display_white, offset=render_scroll)

            # white ouline based on display_white
            display_mask = pygame.mask.from_surface(self.display_white)
            display_sillhouette = display_mask.to_surface(setcolor=(255, 255, 255, 180), unsetcolor=(0, 0, 0, 0)) # 180 opaque, 0 transparent
            self.display_2.blit(display_sillhouette, (0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset) # putting what we drew onframe back into display
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # have to code the window closing
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: # referencing WASD
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_ESCAPE:
                        self.menu.enter()
                if event.type == pygame.KEYUP: # when key is released
                    if event.key == pygame.K_a: 
                        self.movement[0] = False
                    if event.key == pygame.K_d: 
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
            
            self.display_2.blit(self.display_white, (0, 0)) # white 
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset) # render (now scaled) display image on big screen
            pygame.display.update()
            self.clock.tick(60) # run at 60 fps, like a sleep

# returns the game then runs it
Game().run()