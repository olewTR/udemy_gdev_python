import pygame
# init pygame libraries
pygame.init()

# create a display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Continuous Movement")

# load the image
dragon_image = pygame.image.load('dragon_right.png')
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT //2)

# set fps and clock
FPS = 60 # how fast the games runs - here 60 times per second, its called in the game loop
clock = pygame.time.Clock()
# set game values
VELOCITY = 5


# define colors
BLACK = (0,0,0)

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # move the dragon if key pressed
    if keys[pygame.K_LEFT]:
        dragon_image_rect.x -= VELOCITY
    if keys[pygame.K_RIGHT]:
        dragon_image_rect.x += VELOCITY
    if keys[pygame.K_UP]:
        dragon_image_rect.y -= VELOCITY
    if keys[pygame.K_DOWN]:
        dragon_image_rect.y += VELOCITY


    display_surface.fill(BLACK)
    display_surface.blit(dragon_image, dragon_image_rect)

    pygame.display.update()
    # tick the clock
    clock.tick(FPS)

# quit game
pygame.quit()
