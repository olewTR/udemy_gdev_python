import pygame

#initialize pygame
pygame.init()

#create a display surface and set its caption
# constants defined UPPERCASE by convention

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dupa jasiu tralala')

#the main game loop
running = True
while running:
    # loop through the list of event objects that have occured
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

#end of the game
pygame.quit()