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

            if not self.start:
                pass

            self.game.screen.blit(pygame.transform.scale(self.display, self.game.screen.get_size()), (0,0)) # render (now scaled) display image on big screen
            pygame.display.update()
            self.game.clock.tick(60) # run at 60 fps, like a sleep





