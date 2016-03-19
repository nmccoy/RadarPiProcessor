import pygame,sys
from pygame.locals import *


print "buttz1a"
#Display
RESOLUTION = ( 1280, 1024 )
#RESOLUTION = ( 500, 400 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
print "buttz2a"

def start_gui():
        print "buttz3a"
	pygame.init()
        print "buttz4a"
	screen = pygame.display.set_mode([0,0])
	print "buttz5a"
	print "exxxtra butts"
	pygame.display.set_caption('Hello world!')
        print "buttz6a"
	#update_speed(screen,0)
	print "GUI started"
        return screen
 
def gui_loop():
	print "buttz"
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


screen=start_gui()
while True:
	gui_loop()

