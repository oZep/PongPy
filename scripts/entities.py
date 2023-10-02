import pygame
import math
import random

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.UI import Heart

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        '''
        initializes entities
        (game, entitiy type, position, size)
        '''
        self.game = game
        self.type = e_type
        self.pos = list(pos) #make sure each entitiy has it's own list, (x,y)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.speed = 1.5

        self.action = ''
        self.anim_offset = (-3, -3) #renders with an offset to pad the animation against the hitbox
        self.flip = False
        
        self.set_action('idle') #**

        self.last_movement = [0, 0]

    def rect(self):
        '''
        creates a rectangle at the entitiies current postion
        '''
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        '''
        sets a new action to change animation
        (string of animation name) -> animation
        '''
        if action != self.action: # if action has changed
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    
    def update(self, tilemap, movement=(0,0)):
        '''
        updates frames and entitiy position 
        '''
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # this value will be reset every frame, used to stop constant increase of velocity

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0] * self.speed
        entity_rect = self.rect() # getting the entities rectange
        # move tile based on collision on y axis
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # if moving right and you collide with tile
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # if moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        # Note: Y-axis collision handling comes after X-axis handling
        self.pos[1] += frame_movement[1] * self.speed
        entity_rect = self.rect()  # Update entity rectangle for y-axis handling
        # move tile based on collision on y axis
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: # if moving right and you collide with tile
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0: # if moving left
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        entity_rect = self.rect()  # Update entity rectangle for y-axis handling

        # find when to flip img for animation
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement # keeps track of movement

        self.animation.update() # update animation


    def render(self, surf, offset={0,0}):
        '''
        renders entitiy asset
        '''
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1])) # fliping agasint horizontal axis



class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        '''
        instantiates player entity
        (game, position, size)
        '''
        super().__init__(game,'player', pos, size)
        self.set_action('idle')

    def update(self, tilemap, movement=(0,0)):
        '''
        updates frames and entitiy position 
        '''
        super().update(tilemap, movement)

        # player boundary
        if self.pos[1] > 220: 
            self.pos[1] = 220 # screen height - 20
        if self.pos[1] < 0:
            self.pos[1] = 0
        
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > 155: # half screen width - 5
            self.pos[1] = 155


class Player2(PhysicsEntity):
    def __init__(self, game, pos, size):
        '''
        instantiates plauer entity
        (game, position, size)
        '''
        super().__init__(game, 'player2', pos, size)
        self.set_action('idle')


class Moveable(PhysicsEntity):
    def __init__(self, game, pos, size):
        '''
        instantiates plauer entity
        (game, position, size)
        '''
        super().__init__(game, 'moveable', pos, size)
        self.timer = 0


    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)
        if self.rect().colliderect(self.game.player.rect()):
            self.velocity = [0,0]
            if self.game.player.last_movement[0] == 0 or self.game.player.last_movement[1] == 0:
                self.velocity = [2,1]
            else:
                self.velocity[0] = abs(self.game.player.last_movement[0]) / (self.game.player.last_movement[0]) * 2
                self.velocity[1] = abs(self.game.player.last_movement[1]) / (self.game.player.last_movement[1]) * 2
        elif self.rect().colliderect(self.game.player2.rect()): # if enemy hitbox collides with player
            self.velocity = [0,0]
            if self.game.player2.last_movement[0] == 0 or self.game.player2.last_movement[1] == 0:
                self.velocity = [-2,-1]
            else:
                self.velocity[0] = abs(self.game.player2.last_movement[0]) / (self.game.player2.last_movement[0]) * 2
                self.velocity[1] = abs(self.game.player2.last_movement[1]) / (self.game.player2.last_movement[1]) * 2
        
        if self.pos[1] < 0:
            self.velocity[1] = -self.velocity[1]
        if self.pos[1] > 230: # half screen width - 5
            self.velocity[1] = -self.velocity[1]

        if self.pos[0] < 0:
            self.velocity[0] = -self.velocity[0]
        if self.pos[0] > 310: # half screen width - 5
            self.velocity[0] = -self.velocity[0]


        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.005, 0) # right falling to left
        else:
            self.velocity[0] = min(self.velocity[0] + 0.005, 0) # left falling to to right
        
        if self.velocity[1] > 0:
            self.velocity[1] = max(self.velocity[1] - 0.005, 0) # right falling to left
        else:
            self.velocity[1] = min(self.velocity[1] + 0.005, 0) # left falling to to right
