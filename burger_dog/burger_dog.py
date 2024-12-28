import pygame, random
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Burger Dog game')

# set game values
FPS = 60
clock = pygame.time.Clock()
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burger_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY

# set colors
ORANGE = (246, 170, 54)
BLACK = (0,0, 0)
WHITE = (255, 255, 255)

# set fonts
font = pygame.font.Font('./burger_dog_assets/WashYourHand.ttf',32)

# set texts
points_text = font.render('Burger points: ' + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10,10)

score_text = font.render('Points: ' + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render('Burger dog', True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH //2
title_rect.y = 10

eaten_text = font.render('Eaten Burgers: ' + str(burger_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.y = 50

lives_text = font.render('Lives: ' + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

boost_text = font.render('Boost: ' + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH -10, 50)

game_over_text = font.render('Final score: ' + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render('Press any key to continue...', True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT// + 64)

# set sounds and music
bark_sound = pygame.mixer.Sound('./burger_dog_assets/bark_sound.wav')
miss_sound = pygame.mixer.Sound('./burger_dog_assets/miss_sound.wav')
pygame.mixer.music.load('./burger_dog_assets/bd_background_music.wav')

# set images
player_image_right = pygame.image.load('./burger_dog_assets/dog_right.png')
player_image_left = pygame.image.load('./burger_dog_assets/dog_left.png')

player_image = player_image_left
player_image_rect = player_image.get_rect()
player_image_rect.centerx = (WINDOW_WIDTH //2)
player_image_rect.bottom = (WINDOW_HEIGHT)

burger_image = pygame.image.load('./burger_dog_assets/burger.png')
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH -32 ), -BUFFER_DISTANCE) # place it above screen


# game loop
running = True
# pygame.mixer_music.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # key pressed is not an event, so outside of that loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_image_rect.left > 0:
        player_image = player_image_left
        player_image_rect.x -= player_velocity
    if keys[pygame.K_RIGHT] and player_image_rect.right < WINDOW_WIDTH:
        player_image = player_image_right
        player_image_rect.x += player_velocity
    if keys[pygame.K_UP] and player_image_rect.top > 100:
        player_image_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_image_rect.bottom < WINDOW_HEIGHT:
        player_image_rect.y += player_velocity

    # engage boost if available
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -=1
        boost_text = font.render('Boost: ' + str(boost_level), True, ORANGE)
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY

    # drop the burger - only y needs to update
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity*(WINDOW_HEIGHT - burger_rect.y + 100))

    # if the player missed the burger
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        lives_text = font.render('Lives: ' + str(player_lives), True, ORANGE)
        miss_sound.play()

        # reset the burger position
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH -32 ), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        # reset the player position and boost level 
        player_image_rect.centerx = WINDOW_WIDTH//2
        player_image_rect.bottom = WINDOW_HEIGHT
        boost_level = STARTING_BOOST_LEVEL

    # player caught the burger
    if player_image_rect.colliderect(burger_rect):
        score += burger_points
        burger_eaten += 1
        bark_sound.play()
        burger_velocity += BURGER_ACCELERATION
        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

        # reposition burger
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH -32 ), -BUFFER_DISTANCE)


    display_surface.fill(BLACK)

    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOW_WIDTH, 100), 3)

    display_surface.blit(player_image, player_image_rect)
    display_surface.blit(burger_image, burger_rect)

    pygame.display.update()
    clock.tick(FPS)
# end of game 
pygame.quit()