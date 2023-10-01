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
        
        self.pos[0] += frame_movement[0]
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
        self.pos[1] += frame_movement[1]
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
        self.banana = 2

    def update(self, tilemap, movement=(0,0)):
        '''
        updates players animations depending on movement
        '''
        super().update(tilemap, movement=movement)


        # Use this for particle effects
        #if movement[0] != 0: # if moving horizontally
        #    self.set_action('run')
        #elif movement[1] > 0:
        #    self.set_action('runDOWN')
        #elif movement[1] < 0:
        #    self.set_action('runUP')
        #else:
        self.set_action('idle')

        if abs(self.velocity[0]) < 0.1: # stops small sliding across screen after dash
            self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.1:
            self.velocity[1] = 0


    def render(self, surf, offset={0,0}):
        '''
        partly overriding rendering for dashing
        '''
        super().render(surf, offset=offset) # show player

class Player2(PhysicsEntity):
    def __init__(self, game, pos, size):
        '''
        instantiates plauer entity
        (game, position, size)
        '''
        super().__init__(game, 'player1', pos, size)

    def rect(self):
        '''
        creates a rectangle at the entitiies current postion
        '''
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


class Moveable(PhysicsEntity):
    def __init__(self, game, pos, size):
        '''
        instantiates plauer entity
        (game, position, size)
        '''
        super().__init__(game, 'moveable', pos, size)
        self.timer = 0

    def rect(self):
        '''
        creates a rectangle at the entitiies current postion
        '''
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0,0)):
        if self.rect().colliderect(self.game.player.rect()) and not self.timer: # if enemy hitbox collides with player
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 10)):
                if self.game.player.movement[0] > 0 and not self.collisions['left']:
                    self.pos = (self.game.player.pos[0]+16, self.game.player.pos[1])
                elif self.game.player.movement[0] < 0 and not self.collisions['right']:
                    self.pos = (self.game.player.pos[0]-16, self.game.player.pos[1])
                elif self.game.player.movement[1] > 0 and not self.collisions['up']:
                    self.pos = (self.game.player.pos[0], self.game.player.pos[1] + 16)
                elif self.game.player.movement[1] < 0 and not self.collisions['down']:
                    self.pos = (self.game.player.pos[0], self.game.player.pos[1]- 16)
                self.timer = 100
                self.game.player.banana = max(0, self.game.player.banana -1)

        if self.timer > 0:
            self.timer -= 1
