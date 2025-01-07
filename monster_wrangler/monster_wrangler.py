import pygame, random

pygame.init()

# set display window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Monster Wrangler')

# set fps and clock
FPS = 60
clock = pygame.time.Clock()

# classes goes here
class Game():
    """A class to control the gameplay """
    def __init__(self, player, monster_group):
        """initialize the game object here"""
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # set sounds and music
        self.next_level_sound = pygame.mixer.Sound('./monster_wrangler_assets/next_level.wav')

        # set fonts
        self.font = pygame.font.Font('./monster_wrangler_assets/Abrushow.ttf', 24)

        # set images
        blue_image = pygame.image.load('./monster_wrangler_assets/blue_monster.png')
        green_image = pygame.image.load('./monster_wrangler_assets/green_monster.png')
        purple_image = pygame.image.load('./monster_wrangler_assets/purple_monster.png')
        yellow_image = pygame.image.load('./monster_wrangler_assets/yellow_monster.png')

        # list corresponds to the monster type attribute
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]
        self.target_monster_type = random.randint(0,3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH //2
        self.target_monster_rect.top = 30

    def update(self):
        """update the game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0


        # check for collisions
        self.check_collisions()

    def draw(self):
        """draw the HUD HERE"""
        # set colors
        WHITE = (255, 255, 255)
        BLUE = (20,176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # add monster colors to a list where index on list matches target monster image
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # set text on hud
        catch_text = self.font.render('Current Catch', True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH //2
        catch_rect.top = 5

        score_text = self.font.render('Score: ' + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,5)

        lives_text = self.font.render('Lives: ' + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render('Current round: ' + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render('Round time: ' + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH -10, 5)

        warp_text = self.font.render('Warps: ' + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH -10, 35)

        # blit the hud
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        # rectangle around the monster image and other around the game area
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH//2- 32, 30, 64, 64),2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200 ), 4)

    def check_collisions(self):
        """check for collisions between player and monsters"""
        # check for collision between player and monsters
        # need to check the type of monster - point or lost life
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)
        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += 100* self.round_number
                # remove the monster from group
                collided_monster.remove(self.monster_group)
                # any more monsters in the group?
                if (self.monster_group):
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    # round complete
                    self.player.reset()
                    self.start_new_round()
            # caught wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                # check for game over
                if self.player.lives <= 0:
                    self.pause_game("Final Score: " + str(self.score), "Press Enter to play again")
                    self.reset_game()
                self.player.reset()

    def start_new_round(self):
        """populate board with new monster set"""
        # score bonus for quick round finish
        self.score += int(10000* self.round_number/(1+self.round_time))
        # reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        # remove any remaining monsters from the group
        for monster in self.monster_group:
            self.monster_group.remove(monster)
        # add monster to the monster group 4 for each round -> each color
        for i in range (self.round_number):
            self.monster_group.add(Monster(random.randint(0,WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[0], 0))
            self.monster_group.add(Monster(random.randint(0,WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[1], 1))
            self.monster_group.add(Monster(random.randint(0,WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[2], 2))
            self.monster_group.add(Monster(random.randint(0,WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[3], 3))

        # choose a new target monster
        self.choose_new_target()

        # play sound 
        self.next_level_sound.play()

    def choose_new_target(self):
        """choose new target monster for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image


    def pause_game(self, main_text, sub_text):
        global running # this is quick bugfix, bad practise to use global variables 

        # set color 
        WHITE = (255, 255, 255)
        BLACK = (0,0,0)

        # create main pause text
        main_text = self.font.render(main_text,True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        # sub pause text

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        # display the text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)

        pygame.display.update()

        # pause the game
        ispaused = True
        while ispaused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ispaused = False
                if event.type == pygame.QUIT:
                    ispaused = False
                    running = False

    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


class Player(pygame.sprite.Sprite):
    """a player class that the user can control"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./monster_wrangler_assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH //2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound('./monster_wrangler_assets/catch.wav')
        self.die_sound = pygame.mixer.Sound('./monster_wrangler_assets/die.wav')
        self.warp_sound = pygame.mixer.Sound('./monster_wrangler_assets/warp.wav')

    def update(self):
        """update the player"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity

    def warp(self):
        """warp the player to the safe zone in the bottom"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT
        
    def reset(self):
        """after dying reset the player position"""
        self.rect.centerx = WINDOW_WIDTH //2
        self.rect.bottom = WINDOW_HEIGHT

class Monster(pygame.sprite.Sprite):
    """a monster class to create enemies"""
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # monster type is an int 0 blue, 1 green, 2 is purple, 3 is yellow
        self.type = monster_type

        # set random motion of monster
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.randint(1,5)

    def update(self):
        """update the monster"""
        self.rect.x += self.dx*self.velocity
        self.rect.y += self.dy*self.velocity

        # bounce the monster off the edges of the display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = -1 * self.dy


# create a sprite groups
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

# monster group will be populated in the game class
my_monster_group = pygame.sprite.Group()

# test monster for testing purposes only
# monster = Monster(500, 500, pygame.image.load('./monster_wrangler_assets/green_monster.png'), 1)
# my_monster_group.add(monster)
# monster = Monster(100, 100, pygame.image.load('./monster_wrangler_assets/yellow_monster.png'), 3)
# my_monster_group.add(monster)

# create a game object
my_game = Game(my_player, my_monster_group)
my_game.pause_game('Monster hunter', 'Press "enter" to start')
my_game.start_new_round()


# main game loop
running = True
while running:
    # check if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()


    # fill the display
    display_surface.fill((0,0,0))

    # update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    # update and draw the game
    my_game.update()
    my_game.draw()   # its game class own draw method, not derived from sprite


    # update the display and tick the clock

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()