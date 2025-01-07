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
    def __init__(self):
        """initialize the game object here"""
        pass
    def update(self):
        """update the game object"""
        pass       
    def draw(self):
        """draw the HUD HERE"""
        pass
    def check_collisions(self):
        """check for collisions between player and monsters"""
        pass
    def start_new_round(self):
        """populate board with new monster set"""
        pass
    def choose_new_target(self):
        """choose new target monster for the player"""
        pass
    def pause_game(self):
        pass
    def reset_game(self):
        pass

class Player(pygame.sprite.Sprite):
    """a player class that the user can control"""
    def __init__(self, *groups):
        super().__init__(*groups)
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
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.warp()

    def warp(self):
        """warp the player to the safe zone in the bottom"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT
        
    def reset_player(self):
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
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy = -1 * self.dy


# create a sprite groups
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

# monster group will be populated in the game class
my_monster_group = pygame.sprite.Group()

# test monster for testing purposes only
monster = Monster(500, 500, pygame.image.load('./monster_wrangler_assets/green_monster.png'), 1)
monster2 = Monster(100, 100, pygame.image.load('./monster_wrangler_assets/yellow_monster.png'), 3)
my_monster_group.add(monster)
my_monster_group.add(monster2)

# create a game object
my_game = Game()


# main game loop
running = True
while running:
    # check if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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