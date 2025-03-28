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
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        """initialize class"""
        super().__init__()
        # load appropriate images by looking up the image_int
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load('images/tiles/Tile (1).png'),(32,32))
        # platform tiles
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load('images/tiles/Tile (2).png'),(32,32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load('images/tiles/Tile (3).png'), (32,32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load('images/tiles/Tile (4).png'), (32,32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load('images/tiles/Tile (5).png'), (32,32))
            sub_group.add(self)

        # evey tile needs to be added to main tile group
        main_group.add(self)

        # setting the rect
        self.rect = self.image.get_rect()
        self.rect.topleft=(x, y)

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
    def __init__(self, x, y, main_group):
        """init the class"""
        super().__init__()
        """init also the superclass"""
        
        # animation frames
        self.ruby_sprites = []

        # rotating
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile000.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile001.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile002.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile003.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile004.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile005.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./images/ruby/tile006.png'), (64,64)))

        # load image and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        # add to the main group for the drawing purposes
        main_group.add(self)

    def update(self):
        """update the ruby maker"""
        self.animate(self.ruby_sprites, 0.25)

    def animate(self, sprite_list, speed):
        """do the ruby animation"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

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

# create sprite groups  
my_main_tile_group = pygame.sprite.Group()  # all tiles in this group
my_platform_group = pygame.sprite.Group() # only platform tiles
my_player_group = pygame.sprite.Group() # player group
my_bullet_group = pygame.sprite.Group() # the slashes from the sword 
my_zombie_group = pygame.sprite.Group() # zombie group
my_portal_group = pygame.sprite.Group() # portals group
my_ruby_group = pygame.sprite.Group() # ruby group

# create the tile map here
# 0 => no tile
# 1 => dirt tile
# 2-5 => platforms
# 6 => ruby maker
# 7,8 => platform
# 9 => player
# tile map is 40 x 23 (tiles)
tile_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,6,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
# generate tile map from the list of lists
# loop through the 23 lists (i moves down, j moves right)
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        # for 0 do nothing, for 1 - dirt
        if tile_map[i][j]== 1:
            Tile(j*32, i*32, 1, my_main_tile_group)
        # for platform tiles 2-5
        elif tile_map[i][j]==2:
            Tile(j*32,i*32, 2, my_main_tile_group, my_platform_group)
        elif tile_map[i][j]==3:
            Tile(j*32,i*32, 3, my_main_tile_group, my_platform_group)
        elif tile_map[i][j]==4:
            Tile(j*32,i*32, 4, my_main_tile_group, my_platform_group)
        elif tile_map[i][j]==5:
            Tile(j*32,i*32, 5, my_main_tile_group, my_platform_group)
        # ruby maker
        elif tile_map[i][j]==6:
            RubyMaker(j*32, i*32, my_main_tile_group)
        # portals
        elif tile_map[i][j]==7:
            pass # not ready yet
        elif tile_map[i][j]==8:
            pass # not ready yet
        # player
        elif tile_map[i][j]==9:
            pass # not ready yet


# main game loop here
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # blit the background
    display_surface.blit(background_image, background_rect)

    # blit the tiles
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()