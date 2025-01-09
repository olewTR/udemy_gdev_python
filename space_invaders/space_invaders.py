import pygame, random

pygame.init()


# set display properties
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')

BLACK = (0,0,0)

FPS = 60
clock = pygame.time.Clock()

# define classesmy_alien = Alien(my_alien_bullet_group)


class Game():
    """a class to control the display and gameplay"""
    def __init__(self):
        pass

    def update(self):
        pass
    
    def draw(self):
        """ draw the HUD and other elements to the display"""
        pass
    
    def shift_aliens(self):
        """method to move the aliens, horizontally, then when 
        edge is reached - one row down"""
        pass

    def check_collisions(self):
        """check collisions between player, alien and shots"""
        pass

    def check_round_completion(self):
        pass
    
    def start_new_round(self):
        """ starts new round"""
        pass

    def check_game_status(self):
        """ is player dead etc"""

    def pause_game(self):
        pass

    def reset_game(self):
        pass

class Player(pygame.sprite.Sprite):
    """a class to hold the spaceship object"""
    def __init__(self, bullet_group):
        super().__init__()
        self.image = pygame.image.load('./assets/player_ship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.velocity = 8
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound('./assets/player_fire.wav')

    def update(self):
        """this method will move the player on screen"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        pass

    def reset(self):
        """ reset the player position on screen"""
        self.rect.center = WINDOW_WIDTH//2

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        pass

    def fire(self):
        pass

    def reset(self):
        pass

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

# creating bullet groups

my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

# create a player group
my_player = Player(my_player_bullet_group)
player_group = pygame.sprite.Group()
player_group.add(my_player)

# create an alien group - alien object will be added in the 
# game class / new round method

alien_group = pygame.sprite.Group()

# create the game object
my_game = Game()



# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the display 
    display_surface.fill(BLACK)
    player_group.update()
    player_group.draw(display_surface)

    alien_group.update()
    alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
