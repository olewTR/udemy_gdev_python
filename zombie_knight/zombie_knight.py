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

        # class constants
        self.STARTING_ROUND_TIME = 30

        # class variables
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME

        self.title_font = pygame.font.Font('./fonts/Poultrygeist.ttf', 48)
        self.hud_font = pygame.font.Font('./fonts/Pixel.ttf', 24)

    def update(self):
        """method to update the game"""
        
        # update the round time every second
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0

    def draw(self):
        """drawing elements"""
        
        # define colors
        WHITE = (255, 255, 255)
        GREEN = (20, 200, 20)

        # set text
        score_text = self.hud_font.render('Score: ' + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 50)
        health_text = self.hud_font.render('Health: ' + str('100 for now'), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 25)
        title_text = self.title_font.render('Zombie knight', True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT -25)
        round_text = self.hud_font.render('Night: ' + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topright = (WINDOW_WIDTH -10, WINDOW_HEIGHT - 50)
        time_text = self.hud_font.render('Sunrise in: ' + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH -1, WINDOW_HEIGHT - 25)

        # draw the HUD
        display_surface.blit(score_text, score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text, title_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)




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
    def __init__(self, x, y, color, portal_group):
        super().__init__()

        # animation frames
        self.portal_sprites = []

        # portal animation
        if color == "green":
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile000.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile001.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile002.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile003.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile004.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile005.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile006.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile007.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile008.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile009.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile010.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile011.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile012.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile013.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile014.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile015.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile016.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile017.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile018.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile019.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile020.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/green/tile021.png'),(72,72)))
        else :
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile000.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile001.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile002.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile003.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile004.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile005.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile006.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile007.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile008.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile009.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile010.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile011.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile012.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile013.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile014.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile015.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile016.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile017.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile018.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile019.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile020.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./images/portals/purple/tile021.png'),(72,72)))
        
        # load an image and get a rect
        self.current_sprite = random.randint(0, len(self.portal_sprites) -1)
        self.image = self.portal_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        portal_group.add(self)

    def update(self):
        """update the portal object"""
        self.animate(self.portal_sprites, 0.2)

    def animate(self, sprite_list, speed):
        """animate the object"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

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
# 7,8 => portals
# 9 => player
# tile map is 40 x 23 (tiles)
tile_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0],
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
    [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0],
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
            Portal(j*32, i*32, 'green', my_portal_group)
        elif tile_map[i][j]==8:
            Portal(j*32, i*32, 'purple', my_portal_group)
        # player
        elif tile_map[i][j]==9:
            pass # not ready yet


my_game = Game()

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
    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()