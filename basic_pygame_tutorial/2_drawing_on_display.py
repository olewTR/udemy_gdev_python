import pygame
#initializing pygame
pygame.init()

#create a display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Drawing objects')

#define colors as tuples
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255, 0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#give a background color
display_surface.fill(YELLOW)

#draw shapes on display
pygame.draw.line(display_surface, RED, (0,0), (100,100), 10)
pygame.draw.line(display_surface, GREEN, (100, 100), (100,200), 3)
pygame.draw.circle(display_surface, BLACK, (200,240), 200, 3)
pygame.draw.circle(display_surface, WHITE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), 55, 11)
pygame.draw.rect(display_surface, MAGENTA, (450, 0, 100, 100))
pygame.draw.rect(display_surface, CYAN, (450, 150, 40,120))

#the main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #updating the display
    pygame.display.update()

#end of the game
pygame.quit()