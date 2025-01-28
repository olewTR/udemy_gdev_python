import pygame
# declare a vector
vector = pygame.math.Vector2

pygame.init()

# set display - the screen dimmensions take into account
# the tile size which is 32x32 
WINDOW_WIDTH = 960   
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Making a tile map')

clock = pygame.time.Clock()
FPS = 60

# define classes
class Tile(pygame.sprite.Sprite):
    """ a class to read and create individual tiles """
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        # load images and put them to proper groups
        if image_int == 1:
            self.image = pygame.image.load('./assets/dirt.png')
        elif image_int == 2:
            self.image = pygame.image.load('./assets/grass.png')
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load('./assets/water.png')
            sub_group.add(self)

        # all tiles should go to the main group
        main_group.add(self)

        # get the rect of the image and position it on grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class Player(pygame.sprite.Sprite):
    """ a class to hold players object"""
    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()
        self.image = pygame.image.load('./assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((x,y))

        # kinematic vectors - first value => x second value => y
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        # some kinemtatic constants to make moving better
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5 # this is gravity


    def update(self):
        """method to update the player object"""

        # if no force is applied (key presses, acceleration should be 0
        # gravity should always be present
        self.acceleration = vector(0,self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
        
        # calculate new kinematics values
        self.acceleration -= self.velocity * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5* self.acceleration # this is from some kinematic stuff
        
        # TODO: potenial problem with acceleration, its slowing down instead
        # print(f"acceleration x {self.acceleration.x} y ={self.acceleration.y}")
        # print(f"velocity x {self.velocity.x} y ={self.velocity.y}")
        # update new rect with above data
        self.rect.bottomleft = self.position

        # check for collision with grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)
        if collided_platforms:
            # if there is grass
            self.position.y = collided_platforms[0].rect.top
            self.velocity.y = 0

        # check for collision with water
        if pygame.sprite.spritecollide(self,self.water_tiles, False):
            print("urdead")

# create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

# load the background

background_image = pygame.image.load('./assets/background.png')
background_rect = background_image.get_rect()
background_rect.topleft =(0,0)


# here create the tile map - nested list?
# 20 rows x 30 columns 
# 0 -> no tile, 1 -> dirt, 2-> grass, 3-> water 4-> player
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2 ],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2 ],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2 ],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1 ],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1 ]
]

# create individual object from the tile map

for i in range (len(tile_map)):
    for j in range (len(tile_map[0])):
        if tile_map[i][j] == 1:
            Tile(j * 32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j * 32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j * 32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j * 32, i * 32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)


# main game loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    #fill the display 
    # display_surface.fill((10, 75, 75))
    display_surface.blit(background_image, background_rect)
    main_tile_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
