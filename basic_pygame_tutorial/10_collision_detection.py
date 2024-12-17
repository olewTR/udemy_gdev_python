import pygame
import random
pygame.init()

# define the display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Collision detection")

# load assets
dragon_image = pygame.image.load('dragon_left.png')
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.topleft = (25, 25)

coin_image = pygame.image.load('coin.png')
coin_image_rect = coin_image.get_rect()
coin_image_rect.topleft = ((WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

FPS = 60
VELOCITY = 5
BLACK = (0,0,0)
clock = pygame.time.Clock()

# game loop here
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # movement
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and dragon_image_rect.left > 0 :
        dragon_image_rect.x -= VELOCITY
    if (keys[pygame.K_RIGHT]or keys[pygame.K_d]) and dragon_image_rect.right < WINDOW_WIDTH:
        dragon_image_rect.x += VELOCITY
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and dragon_image_rect.top > 0 :
        dragon_image_rect.y -= VELOCITY
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and dragon_image_rect.bottom < WINDOW_HEIGHT:
        dragon_image_rect.y += VELOCITY

    # check for collision between dragon and a coin
    if dragon_image_rect.colliderect(coin_image_rect):
        print("hit!")
        coin_image_rect.left = random.randint(0,WINDOW_WIDTH - 32)
        coin_image_rect.top = random.randint(0, WINDOW_HEIGHT - 32)


    display_surface.fill(BLACK)
    # draw rectangles around images to show their rects
    pygame.draw.rect(display_surface, (0,255,0), dragon_image_rect, 1)
    pygame.draw.rect(display_surface, (255, 255, 0), coin_image_rect, 1)

    display_surface.blit(dragon_image, dragon_image_rect)
    display_surface.blit(coin_image, coin_image_rect)

    # refresh screen + at max 60 fps
    pygame.display.update()
    clock.tick(FPS)
# quit pygame
pygame.quit()