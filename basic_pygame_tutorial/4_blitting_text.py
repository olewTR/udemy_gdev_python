import pygame
pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("blitting text")

#define colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
BLACK = (0, 0,)

# see all available fonts from system
fonts = pygame.font.get_fonts()
for font in fonts:
    print(font)

#define fonts
system_font = pygame.font.SysFont('calibri', 64)
custom_font = pygame.font.Font('AttackGraffiti.ttf', 32)

#define text to display
system_text = system_font.render('Dragons Rule!', True, GREEN, DARKGREEN)
system_text_rect =  system_text.get_rect()
system_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

custom_text = custom_font.render('Move the dragon soon!', True, GREEN)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)

#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # blit the text we want to display
    display_surface.blit(system_text, system_text_rect)
    display_surface.blit(custom_text, custom_text_rect)
    
    #update the main display
    pygame.display.update()

pygame.quit()