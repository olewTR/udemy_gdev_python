import pygame
pygame.init()

WINDWOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDWOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Blitting images')

#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#end of the game
pygame.quit()