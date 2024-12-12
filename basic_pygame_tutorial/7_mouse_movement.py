import pygame
pygame.init()

# create the display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('mouse movement')


# load images
dragon_image = pygame.image.load('dragon_right.png')
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.topleft = (25, 25)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragon_image_rect.centerx = event.pos[0] # center of dragon, not top left
            dragon_image_rect.centery = event.pos[1]


    # fill the display (clean it)
    display_surface.fill((0,0,0))

    # blitter
    display_surface.blit(dragon_image, dragon_image_rect)

    #update the display
    pygame.display.update()

pygame.quit()
