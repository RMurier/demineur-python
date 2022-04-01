import pygame
import pygame.locals
import os

pygame.init()
screen = pygame.display.set_mode((1200 , 1000))
pygame.mouse.set_visible(False)  # hide the cursor
MANUAL_CURSOR = pygame.image.load(os.path.join(os.path.dirname(__file__), 'hippo.jpg')).convert_alpha()
# pygame.mouse.set_cursor((8,8),(4,4),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
             screen.blit( MANUAL_CURSOR, ( pygame.mouse.get_pos() ) )
             pygame.display.update()