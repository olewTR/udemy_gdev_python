import pygame
import random
pygame.init()

# set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Feed the Dragon')

# set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# set colors
GREEN = (0,255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# set fonts
font = pygame.font.Font('AttackGraffiti.ttf', 32)

# set text
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft=(10,10)

title_text = font.render('Feed the Dragon', True, GREEN, DARKGREEN)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render('lives : ' + str(player_lives), True, GREEN, DARKGREEN)
livest_rect = lives_text.get_rect()
livest_rect.topright = (WINDOW_WIDTH - 10, 10)

# this will not be blittered in main game loop, only on game over
game_over_text = font.render('GAMEOVER!', True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT //2)

continue_text = font.render('Press any key to play again', True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT//2 + 32) # one line below gameover txt

# set sound and music
coin_sound = pygame.mixer.Sound('coin_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('ftd_background_music.wav')

# set images
player_image = pygame.image.load('dragon_right.png')
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT //2

coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32) # because there is a text, and 
# also -32 because of size of the image itself, we don't want it to appear with only 
# one pixel on surface

# main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check if key pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # move the coin on screen
    if coin_rect.x < 0: #player missed the coin
        player_lives -= 1 # can be shorter?
        miss_sound.play()
        # reset coin position
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        # move the coint
        coin_rect.x -= coin_velocity

    # check for collisions
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        # reset the coin position
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    # update text for score / lives
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render('lives : ' + str(player_lives), True, GREEN, DARKGREEN)

    # check conditions for game over 
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # pause the game and wait for decision
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False



    # refresh the screen with black background
    display_surface.fill(BLACK)

    # copy text on HUD and display a line do divide it from game area
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, livest_rect)
    pygame.draw.line(display_surface, WHITE, (0,64), (WINDOW_WIDTH, 64), 1)

    # copy images to the display surface
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    # tick the loop and update screen
    pygame.display.update()
    clock.tick(FPS)

# end the game
pygame.quit()