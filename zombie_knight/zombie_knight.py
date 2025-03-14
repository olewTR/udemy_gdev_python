import pygame, random
# we will need vectors a lot
vector = pygame.math.Vector2
pygame.init()

# set display settings (the tile size is 32x32 so there is 40x23 tiles on screen)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Knight")

# load in background image
background_image = pygame.transform.scale(pygame.image.load("./images/background.png"),(WINDOW_WIDTH, WINDOW_HEIGHT)) 
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

# set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

# game classes go here
class Game():
    """a class to help manage the gameplay"""
    def __init__(self):
        """initialize class"""
        pass

    def update(self):
        """method to update the game"""
        pass

    def draw(self):
        """drawing elements"""
        pass

    def add_zombie(self):
        """add more zombies"""
        pass

    def check_collisions(self):
        """check for collisions"""
        pass

    def check_round_completion(self):
        """check if player survived night"""
        pass

    def check_gameover(self):
        """check to see if player lost the game"""
        pass

    def start_new_round(self):
        """starts new night"""
        pass
    
    def pause_game(self):
        pass

    def reset_game(self):
        pass


class Player(pygame.sprite.Sprite):
    """a class to represent player object"""
    def __init__(self):
        """initialize class"""
        super().__init__()
        pass
    def update(self):
        """update the player"""
        pass
    def move(self):
        """move the player"""
        pass
    def check_collisions(self):
        """check for collisions with platform and portals"""
        pass
    def check_animations(self):
        """check if animations should be made"""
        pass
    def jump(self):
        """jump your player if on a platform"""
        pass
    def fire(self):
        """fire your guns"""
        pass
    def reset(self):
        """reset your player state"""
        pass
    def animate(self):
        """animate your character"""
        pass


class Tile(pygame.sprite.Sprite):
    """a class to represent the tile elements"""
    def __init__(self):
        """initialize class"""
        super().__init__()
        pass


class Bullet(pygame.sprite.Sprite):
    """a projectile created by player"""
    def __init__(self):
        """"init the class"""
        super().__init__()
        pass
    def update(self):
        """update the bullet object"""
        pass
    

class Zombie(pygame.sprite.Sprite):
    """initialize the class"""
    def __init__(self):
        super().__init__()
        pass
    def update(self):
        """update the zombie"""
        pass
    def move(self):
        """move the zombie"""
        pass
    def check_collisions(self):
        """check for collisions"""
        pass
    def check_animations(self):
        """check if animation should run"""
        pass
    def animate(self):
        """animate the zombie object"""
        pass
    

class RubyMaker(pygame.sprite.Sprite):
    """a tile that is animated - a ruby is generated here"""
    def __init__(self):
        """init the class"""
        super().__init__()
        """init also the superclass"""
        pass
    def update(self):
        """update the ruby maker"""
        pass
    def animate(self):
        """do the ruby animation"""
        pass


class Ruby(pygame.sprite.Sprite):
    """class for ruby object that is needed to get more health etc"""
    def __init__(self):
        super().__init__()
        pass
    def update(self):
        """update the ruby object"""
        pass
    def check_collisions(self):
        """check for collsions with platforms and portals"""
        pass
    def move(self):
        """move the ruby"""
        pass
    def animat(self):
        """animate the ruby object"""
        pass
    

class Portal(pygame.sprite.Sprite):
    """class for portal object"""
    def __init__(self):
        super().__init__()
    def update(self):
        """update the portal object"""
        pass
    def animate(self):
        """animate the object"""
        pass

# main game loop here
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.blit(background_image, background_rect)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()