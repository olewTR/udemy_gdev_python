import pygame
pygame.init()


# prepare surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('follow the mouse')

# load the dragon

dragon_image = pygame.image.load('dragon_right.png')
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.topleft = (0,0)



# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # this time only move the image if left button pressed and mouse moved
        if (event.type == pygame.MOUSEMOTION) and  (event.buttons[0] == 1):
            dragon_image_rect.centerx = event.pos[0]
            dragon_image_rect.centery = event.pos[1]


    # clear the surface
    display_surface.fill((0,0,0))
    # copy the image over to the display
    display_surface.blit(dragon_image, dragon_image_rect)
    pygame.display.update()

# end 
pygame.quit()