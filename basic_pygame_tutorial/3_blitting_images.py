import pygame
pygame.init()

WINDWOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
display_surface = pygame.display.set_mode((WINDWOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Blitting images')

# create images ... returns surface object with 
# image drawn on it -> when ready it can be positioned on
# the main surface using its rectangle size
dragon_left_image = pygame.image.load("dragon_left.png")
# coordinates will be:
dragon_left_rect = dragon_left_image.get_rect()
dragon_left_rect.topleft = (0,0)
dragon_right_image = pygame.image.load("dragon_right.png")
#coordinates will be :
dragon_right_rect = dragon_right_image.get_rect()
dragon_right_rect.topright = (WINDWOW_WIDTH,0)


#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #blit (copy) a surface object to the main display
    display_surface.blit(dragon_left_image, dragon_left_rect)
    display_surface.blit(dragon_right_image, dragon_right_rect)

    pygame.draw.line(display_surface, (255,255,255), (0, 75), (WINDWOW_WIDTH, 75), 4)

    pygame.display.update()

#end of the game
pygame.quit()