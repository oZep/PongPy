import pygame
import sys
from .utils import load_image
class MainMenu():
    def __init__(self, game, display):
        '''
        Initalizing main menu
        getting server and host
        establishing connection
        transitioning to main game loop
        ''' 

        self.display = display
        self.game = game
        self.connection = 0
        self.start = 0
        self.port = ''
        self.host = ''
        self.port_select = 0
        self.host_select = 0

        self.assets = {
            'MainMenu': load_image('MainMenu.png'),
        }
    
    def enter(self):
        while (not self.connection):
            self.display.blit(self.assets['MainMenu'], (0,0)) # no outline
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # have to code the window closing
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_0:
                    if self.port_select:
                        self.port += '0'
                    if self.host_select:
                        self.host += '0'
                if event.key == pygame.K_1:
                    if self.port_select:
                        self.port += '1'
                    if self.host_select:
                        self.host += '1'
                if event.key == pygame.K_2:
                    if self.port_select:
                        self.port += '2'
                    if self.host_select:
                        self.host += '2'
                if event.key == pygame.K_3:
                    if self.port_select:
                        self.port += '3'
                    if self.host_select:
                        self.host += '3'
                if event.key == pygame.K_4:
                    if self.port_select:
                        self.port += '4'
                    if self.host_select:
                        self.host += '4'
                if event.key == pygame.K_5:
                    if self.port_select:
                        self.port += '5'
                    if self.host_select:
                        self.host += '5'
                if event.key == pygame.K_6:
                    if self.port_select:
                        self.port += '6'
                    if self.host_select:
                        self.host += '6'
                if event.key == pygame.K_7:
                    if self.port_select:
                        self.port += '7'
                    if self.host_select:
                        self.host += '7'
                if event.key == pygame.K_8:
                    if self.port_select:
                        self.port += '8'
                    if self.host_select:
                        self.host += '8'
                if event.key == pygame.K_9:
                    if self.port_select:
                        self.port += '9'
                    if self.host_select:
                        self.host += '9'

            if not self.start:
                pass
            if self.start:
                pass # connect to the client
            self.game.screen.blit(pygame.transform.scale(self.display, self.game.screen.get_size()), (0,0)) # render (now scaled) display image on big screen
            pygame.display.update()
            self.game.clock.tick(60) # run at 60 fps, like a sleep





