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

    def update(self):
        # draw a rectangle of a tile with blue line
        pygame.draw.rect(display_surface, (0,0,255), self.rect, 1)

class Player(pygame.sprite.Sprite):
    """ a class to hold players object"""
    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        # animation frames instead of knight image
        self.move_left_sprites = []
        self.move_right_sprites = []
        self.idle_left_sprites = []
        self.idle_right_sprites = []

        # animate move right        
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (1).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (2).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (3).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (4).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (5).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (6).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (7).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (8).png"),(64,64)))

        # transform move right to animate moving left
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # animate idle right
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (1).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (8).png"), (64,64)))

        # transforming idle right to idle left animation
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite,True,False))

        self.current_sprite = 0

        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        self.starting_x = x
        self.starting_y = y # ffs couldn't it be taken from the tuple above?

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles
        
        # kinematic vectors - first value => x second value => y
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        
        # some kinemtatic constants to make moving better
        self.HORIZONTAL_ACCELERATION = 1
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5 # this is gravity
        self.VERTICAL_JUMP_SPEED = 15


    def update(self):
        """method to update the player object"""
        
        # create a mask around player for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image, (255,255,0), True, mask_outline)

        self.move()
        self.check_collisions()


    def move(self):
        # if no force is applied (key presses, acceleration should be 0
        # gravity should always be present
        self.acceleration = vector(0,self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .2)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .2)
        else:
            if self.velocity.x >0:
                self.animate(self.idle_right_sprites, .2)
            else:
                self.animate(self.idle_left_sprites, .2)

                
        # calculate new kinematics values 
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5* self.acceleration # this is from some kinematic stuff
        
        # update new rect with above data and wrap around the screen motion
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        # check for collision with grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if collided_platforms:
            # if there is grass and only if falling down
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top + 10
                self.velocity.y = 0

        # check for collision with water
        if pygame.sprite.spritecollide(self,self.water_tiles, False):
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0,0)
            print("urdead")

    def jump(self):
        """a method allowing player to jump"""
        # jumping only from grass tile
        if pygame.sprite.spritecollide(self,self.grass_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED


    def animate(self, sprite_list, speed):
        """animate the player image"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]


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
        elif event.type == pygame.KEYDOWN: # why the hell here not in player?
            if event.key == pygame.K_SPACE:
                my_player.jump()  

    #fill the display 
    # display_surface.fill((10, 75, 75))
    display_surface.blit(background_image, background_rect)
    main_tile_group.draw(display_surface)
    main_tile_group.update()

    my_player_group.update()
    my_player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
