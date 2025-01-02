import pygame, random

# initialize game
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLACK = (0,0,0)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sprite groups')

# define classes 
class Player(pygame.sprite.Sprite):
    """ a class to represent the Player object """
    def __init__(self, x, y, monster_group):
        super().__init__()
        self.image = pygame.image.load('./assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 5
        self.monster_group = monster_group
    def update(self):
        """ update the move of player object """
        self.move()
        self.collisions()
    def move(self):
        """move the player object on screen"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
    def collisions(self):
        """check for collisions between sprite groups Player and Monster"""
        if pygame.sprite.spritecollide(self, self.monster_group, True):
            print(len(self.monster_group))

class Monster(pygame.sprite.Sprite):
    """ a class to represent monster asset """
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load('./assets/blue_monster.png')    
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 
        self.velocity = random.randint(1,10)
    def update(self):
        """ update and move the monster """
        self.rect.y += self.velocity

# create a sprite group to hold 10 monsters
my_monster_group = pygame.sprite.Group()
for i in range(10):
    monster = Monster(i*64, 10)
    my_monster_group.add(monster)

# create a player group
player_group = pygame.sprite.Group()
player = Player(500, 500, my_monster_group)
player_group.add(player)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the display black 
    display_surface.fill(BLACK)

    # blit the assets - or draw them all rather
    my_monster_group.update()
    my_monster_group.draw(display_surface)

    player_group.update()
    player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()