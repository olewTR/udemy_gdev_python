import pygame

pygame.init()

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Restricted Movement")


# load image
dragon_image = pygame.image.load('dragon_right.png')
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT //2)

# define game constants
FPS = 60
BLACK = (0,0,0)
VELOCITY = 5
clock = pygame.time.Clock()


# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # get a list of all keys currently pressed down
    keys = pygame.key.get_pressed()

    # move to expected direction
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and dragon_image_rect.left > 0 :
        dragon_image_rect.x -= VELOCITY
    if (keys[pygame.K_RIGHT]or keys[pygame.K_d]) and dragon_image_rect.right < WINDOW_WIDTH:
        dragon_image_rect.x += VELOCITY
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and dragon_image_rect.top > 0 :
        dragon_image_rect.y -= VELOCITY
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and dragon_image_rect.bottom < WINDOW_HEIGHT:
        dragon_image_rect.y += VELOCITY

    display_surface.fill(BLACK)
    display_surface.blit(dragon_image, dragon_image_rect)
    
    pygame.display.update()
    # tick the clock 
    clock.tick(FPS)


# quit the game
pygame.quit()