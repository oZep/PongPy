import pygame
import sys
from .utils import load_image
from .UI import TextUI

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
            'Icon': load_image('icon.png'),
        }
    
    def enter(self):
        while (not self.connection):
            self.display.blit(self.assets['MainMenu'], (0,0)) # no outline
            self.display.blit(self.assets['Icon'], (self.display.get_width() // 3, 0)) # no outline
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # have to code the window closing
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
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
                    if event.key == pygame.K_PERIOD:
                        if self.port_select:
                            self.port += '.'
                        if self.host_select:
                            self.host += '.'
                    if event.key == pygame.K_DELETE:
                        if self.port_select:
                            self.port = self.port[:len(self.port)-1] # delete a character
                        if self.host_select:
                            self.host = self.host[:len(self.port)-1]
                    if event.key == pygame.K_a:
                        self.host_select = 0
                        self.port_select = 1
                    if event.key == pygame.K_d:
                        self.host_select = 1
                        self.port_select = 0


            if not self.start:
                # display host
                if self.host_select:
                    host_indicator = TextUI("Host:", pos=(200, self.display.get_height() // 2 - 20), color=(255,0,0))
                else:
                    host_indicator = TextUI("Host:", pos=(200, self.display.get_height() // 2 - 20))
                host_UI = TextUI(self.host, pos=(200, self.display.get_height() // 2))
                host_indicator.render(self.display, 22)
                host_UI.render(self.display, 22)
                #display server
                if self.port_select:
                    server_indicator = TextUI("Server:", pos=(40, self.display.get_height() // 2 - 20), color=(255,0,0))
                else:
                    server_indicator = TextUI("Server:", pos=(40, self.display.get_height() // 2 - 20))
                server_UI = TextUI(self.port, pos=(40, self.display.get_height() // 2))
                server_indicator.render(self.display, 22)
                server_UI.render(self.display, 22)

            if self.start:
                pass # connect to the client
            self.game.screen.blit(pygame.transform.scale(self.display, self.game.screen.get_size()), (0,0)) # render (now scaled) display image on big screen
            pygame.display.update()
            self.game.clock.tick(60) # run at 60 fps, like a sleep





