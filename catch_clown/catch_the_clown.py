import pygame, random
pygame.init()

# set the constants
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Catch the clown')
clock = pygame.time.Clock()
FPS = 60

# game settings
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = .1

score = 0
player_lives = PLAYER_STARTING_LIVES
clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1,1]) # clown moving direction on x
clown_dy = random.choice([-1,1]) # clown moving direction on y

BLUE = (1,175, 209)
YELLOW = (248, 231, 28)

font = pygame.font.Font('Franxurter.ttf', 32)

title_text = font.render('Catch the Clown',True, BLUE, YELLOW)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render('Score: ' +  str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)

lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50,50)

game_over_text = font.render('GAME OVER', True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH //2 , WINDOW_HEIGHT//2)

continue_text = font.render('Click anywhere to play again', True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT//2 + 32)

click_sound = pygame.mixer.Sound('click_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
pygame.mixer.music.load('ctc_background_music.wav')

background_image = pygame.image.load('background.png')
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

clown_image = pygame.image.load('clown.png')
clown_rect = clown_image.get_rect()
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)


# main game loop
pygame.mixer.music.play(-1, 0.0)
runnig = True
while runnig:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
        
            # the clown clicked?
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                previous_dx = clown_dx
                previous_dy = clown_dy
                while(previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1,1])
                    clown_dy = random.choice([-1,1])

            else:
                miss_sound.play()
                player_lives = player_lives-1

    # move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # bounce from the edges
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx = -clown_dx
    if clown_rect.top <= 0 or clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = -clown_dy

    score_text = font.render('Score: ' + str(score), True, YELLOW)
    lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)

    # is it gameover?
    if player_lives == 0:
        display_surface.blit(background_image, background_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # pause the game 
        pygame.mixer.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES

                    clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type ==pygame.QUIT:
                    is_paused = False
                    runnig =  False
    
    # update the display
    display_surface.blit(background_image, background_rect)
    
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)

    display_surface.blit(clown_image, clown_rect)

    pygame.display.update()
    clock.tick(FPS)


# quit the game
pygame.quit()