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
background_image = pygame.transform.scale(pygame.image.load("./assets/images/background.png"),(WINDOW_WIDTH, WINDOW_HEIGHT)) 
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

# set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

# game classes go here
class Game():
    """a class to help manage the gameplay"""
    def __init__(self, player, zombie_group, platform_group, portal_group, bullet_group, ruby_group):
        """initialize class"""

        # class constants
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ZOMBIE_CREATION_TIME = 5  # so every 5 seconds a zombie should be created

        # class variables
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

        self.title_font = pygame.font.Font('./assets/fonts/Poultrygeist.ttf', 48)
        self.hud_font = pygame.font.Font('./assets/fonts/Pixel.ttf', 24)

        # attach groups and sprites
        self.player = player
        self.zombie_group = zombie_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group

    def update(self):
        """method to update the game"""
        
        # update the round time every second
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0

        # check for gampelay collisions
        self.check_collisions()

        # add zombie if zombie creation time is met
        self.add_zombie()

    def draw(self):
        """drawing elements"""
        
        # define colors
        WHITE = (255, 255, 255)
        GREEN = (20, 200, 20)

        # set text
        score_text = self.hud_font.render('Score: ' + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 50)
        health_text = self.hud_font.render('Health: ' + str(self.player.health), True, WHITE)
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
        # check to add zombie every second
        if self.frame_count % FPS ==0:
            # only add zombie if...
            if self.round_time % self.zombie_creation_time == 0:
                zombie = Zombie(self.platform_group, self.portal_group, self.round_number, self.round_number + 5)
                self.zombie_group.add(zombie)


    def check_collisions(self):
        """check for collisions"""
        # see if any bullet hit a zombie
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)
        if collision_dict:
            for zombies in collision_dict.values():
                for zombie in zombies:
                    zombie.hit_sound.play()
                    zombie.is_dead = True
                    zombie.animate_death = True

        # see if player stomped a zombie or a zombie bite and done damage
        collision_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)
        if collision_list:
            for zombie in collision_list:
                # is zombie dead?
                if zombie.is_dead == True:
                    zombie.kick_sound.play()
                    zombie.kill()
                    self.score += 25

                    ruby = Ruby(self.platform_group, self.portal_group)
                    self.ruby_group.add(ruby)

                else:
                    self.player.health -= 20
                    self.player.hit_sound.play()
                    # move the player to not take continous damage
                    self.player.position.x -= 256 * zombie.direction
                    self.player.rect.bottomleft = self.player.position

        

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
    def __init__(self, x, y, platform_group, portal_group, bullet_group):
        """initialize class"""
        super().__init__()
        
        # set constants 
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.8  # gravity
        self.VERTICAL_JUMP_SPEED = 18  # how high the player jump
        self.STARTING_HEALTH = 100

        # animation frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        # moving animations
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (1).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (2).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (3).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (4).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (5).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (6).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (7).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (8).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (9).png'), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/run/Run (10).png'), (64,64)))

        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # idle animations
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (1).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (2).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (3).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (4).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (5).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (6).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (7).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (8).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (9).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/idle/Idle (10).png'), (64, 64)))

        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # jumping animations
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (1).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (2).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (3).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (4).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (5).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (6).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (7).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (8).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (9).png'), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/jump/Jump (10).png'), (64,64)))

        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # attack animation
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (1).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (2).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (3).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (4).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (5).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (6).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (7).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (8).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (9).png'), (64, 64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/player/attack/Attack (10).png'), (64, 64)))

        for sprite in self.attack_right_sprites:
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # load image and get rect
        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # attach sprite groups 
        self.platform_group = platform_group  # or will it be platform grup rather?
        self.portal_group = portal_group
        self.bullet_group = bullet_group

        # animation booleans
        self.animate_jump = False
        self.animate_fire = False

        # load sounds
        self.jump_sound = pygame.mixer.Sound('./assets/sounds/jump_sound.wav')
        self.slash_sound = pygame.mixer.Sound('./assets/sounds/slash_sound.wav')
        self.portal_sound = pygame.mixer.Sound('./assets/sounds/portal_sound.wav')
        self.hit_sound = pygame.mixer.Sound('./assets/sounds/player_hit.wav')

        # kinematic vectors
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # set initial player values
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y


    def update(self):
        """update the player"""
        self.move()
        self.check_collisions()
        self.check_animations()

    def move(self):
        """move the player"""
        # set the acceleration vector
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # if is user is pressing the key, then set x component
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.animate(self.move_left_sprites, 0.5)
            self.acceleration.x = self.HORIZONTAL_ACCELERATION * -1
        elif keys[pygame.K_RIGHT]:
            self.animate(self.move_right_sprites, 0.5)
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.5)
            else:
                self.animate(self.idle_left_sprites, 0.5)

        # calculate new kinematics values
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # update rect based on kinematic calculations and wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        """check for collisions with platform and portals"""
        # collision check between player and platforms for falling
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0

        # collision check between player and platform when jumping up
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        # collistion check with portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # determine which portal are you moving to
            # left and right
            if self.position.x > WINDOW_WIDTH //2:
                self.position.x = 86 # hardcoded position to go to
            else:
                self.position.x = WINDOW_WIDTH - 150
            # top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position


    def check_animations(self):
        """check if animations should be made"""
        # animate players jump
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, 0.1)
            else:
                self.animate(self.jump_left_sprites, 0.1)
        # player fires
        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, 0.25)
            else:
                self.animate(self.attack_left_sprites, 0.25)

    def jump(self):
        """jump your player if on a platform"""
        # only jump if on platform
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
        self.animate_jump = True

    def fire(self):
        """fire your guns"""
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True

    def reset(self):
        """reset your player state"""
        self.position = vector(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """animate your character"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # end the jump animation
            if self.animate_jump:
                self.animate_jump = False
            # end the attack animation
            if self.animate_fire:
                self.animate_fire = False

        self.image = sprite_list[int(self.current_sprite)]

class Tile(pygame.sprite.Sprite):
    """a class to represent the tile elements"""
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        """initialize class"""
        super().__init__()
        # load appropriate images by looking up the image_int
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/tiles/Tile (1).png'),(32,32))
        # platform tiles
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/tiles/Tile (2).png'),(32,32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/tiles/Tile (3).png'), (32,32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/tiles/Tile (4).png'), (32,32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/tiles/Tile (5).png'), (32,32))
            sub_group.add(self)

        # evey tile needs to be added to main tile group
        main_group.add(self)

        # setting the rect
        self.rect = self.image.get_rect()
        self.rect.topleft=(x, y)

class Bullet(pygame.sprite.Sprite):
    """a projectile created by player"""
    def __init__(self, x, y, bullet_group, player):
        """"init the class"""
        super().__init__()
        # set constatnts
        self.VELOCITY = 20 # not affected by gravity
        self.RANGE = 200 # range 200 px then dissapears

        # load the image and get the rect
        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load('./assets/images/player/slash.png'), (32,32))
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/images/player/slash.png'), (32,32)), True, False)
            self.VELOCITY = -1*self.VELOCITY

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.starting_x = x
        bullet_group.add(self)
        
    def update(self):
        """update the bullet object"""
        self.rect.x += self.VELOCITY

        # if the bullet passed the range, remove it
        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    """initialize the class"""
    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        # set constants
        self.VERTICAL_ACCELERATION = 3 # gravity
        self.RISE_TIME = 2 # reanimation time

        # animation frames
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        gender = random.randint(0,1)
        if gender ==0:
            # walking 
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (1).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (2).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (3).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (4).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (5).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (6).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (7).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (8).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (9).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/walk/Walk (10).png'),(64, 64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # dying animation
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (1).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (2).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (3).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (4).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (5).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (6).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (7).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (8).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (9).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (10).png'), (64, 64)))
            
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # rising animation - reverted dying animation, I think better copy die instead load / transform again etc
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (10).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (9).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (8).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (7).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (6).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (5).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (4).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (3).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (2).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/boy/dead/Dead (1).png'), (64, 64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        else:
            # walking 
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (1).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (2).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (3).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (4).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (5).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (6).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (7).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (8).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (9).png'),(64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/walk/Walk (10).png'),(64, 64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # dying animation
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (1).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (2).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (3).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (4).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (5).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (6).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (7).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (8).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (9).png'), (64, 64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (10).png'), (64, 64)))
            
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # rising animation - reverted dying animation, I think better copy die instead load / transform again etc
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (10).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (9).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (8).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (7).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (6).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (5).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (4).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (3).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (2).png'), (64, 64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/zombie/girl/dead/Dead (1).png'), (64, 64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # load the image and get the rect
        self.direction = random.choice([-1,1])
        self.current_sprite = 0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.current_sprite]
        else:
            self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH -100), -100)

        # attach sprite groups 
        self.platform_group = platform_group
        self.portal_group = portal_group

        # animation booleans
        self.animate_death = False
        self.animate_rise = False

        # load sounds
        self.hit_sound = pygame.mixer.Sound('./assets/sounds/zombie_hit.wav')
        self.kick_sound = pygame.mixer.Sound('./assets/sounds/zombie_kick.wav')
        self.portal_sound = pygame.mixer.Sound('./assets/sounds/portal_sound.wav')

        # kinematic vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction * random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # initial zombie values
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0

    def update(self):
        """update the zombie"""
        self.move()
        self.check_collisions()
        self.check_animations()

        # determine when zombie rise from dead
        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True
                    # when the zombie died, the image was kept as last image
                    # when it rises, we want to start at index 0 of rise_sprite collection
                    self.current_sprite = 0
        
    def move(self):
        """move the zombie"""
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, 0.5)
            else:
                self.animate(self.walk_right_sprites, 0.5)
            
            # we dont need to update acceleration vector, it never changes
            # reused move method from Player class, but rest is not needed
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration

            # when it reaches the screen edge:
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0

            self.rect.bottomleft = self.position

    def check_collisions(self):
        """check for collisions"""
        # collision check between zombie and platform when falling
        collided_patforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_patforms:
            self.position.y = collided_patforms[0].rect.top + 1
            self.velocity.y = 0

        # collistion check with portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # determine which portal zobmie will move to
            # left and right
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            # top and bottom
            if self.position.y > WINDOW_HEIGHT //2:
                self.position.y = 64
            else: 
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        """check if animation should run"""
        # animate zombie death
        if self.animate_death:
            if self.direction == 1:
                self.animate(self.die_right_sprites, 0.095)
            else:
                self.animate(self.die_left_sprites, 0.095)

        # animate zombie rise
        if self.animate_rise:
            if self.direction == 1:
                self.animate(self.rise_right_sprites, 0.095)
            else: 
                self.animate(self.rise_left_sprites, 0.095)

    def animate(self, sprite_list, speed):
        """animate the zombie object"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # end the death animation
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False  
            
            # end the rise animation
            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
                self.frame_count = 0
                self.round_time = 0
                

        self.image = sprite_list[int(self.current_sprite)]

class RubyMaker(pygame.sprite.Sprite):
    """a tile that is animated - a ruby is generated here"""
    def __init__(self, x, y, main_group):
        """init the class"""
        super().__init__()
        """init also the superclass"""
        
        # animation frames
        self.ruby_sprites = []

        # rotating
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile000.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile001.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile002.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile003.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile004.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile005.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile006.png'), (64,64)))

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
    def __init__(self, platform_group, portal_group):
        super().__init__()
        # constants for ruby
        self.VERTICAL_ACCELERATION = 3 # gravity
        self.HORIZONTAL_VELOCITY = 5

        # animation framses
        self.ruby_sprites = []

        # rotating (same as in ruby maker)
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile000.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile001.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile002.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile003.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile004.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile005.png'), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/ruby/tile006.png'), (64,64)))

        # load image and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WINDOW_WIDTH //2 , 100)

        # attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        # load sounds
        self.portal_sound = pygame.mixer.Sound('./assets/sounds/portal_sound.wav')

        # kinematic vectors to move
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(random.choice([-1*self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]),0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

    def update(self):
        """update the ruby object"""
        self.animate(self.ruby_sprites, 0.25)
        self.move()
        self.check_collisions()

    def check_collisions(self):
        """check for collsions with platforms and portals"""
        # collision check between rubys and platforms / zombies / player
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0
        
                # collistion check with portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # determine which portal zobmie will move to
            # left and right
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            # top and bottom
            if self.position.y > WINDOW_HEIGHT //2:
                self.position.y = 64
            else: 
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def move(self):
        """move the ruby"""
        # we dont need to update acceleration vector, it never changes
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # when it reaches the screen edge:
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """animate the ruby object"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

class Portal(pygame.sprite.Sprite):
    """class for portal object"""
    def __init__(self, x, y, color, portal_group):
        super().__init__()

        # animation frames
        self.portal_sprites = []

        # portal animation
        if color == "green":
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile000.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile001.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile002.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile003.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile004.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile005.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile006.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile007.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile008.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile009.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile010.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile011.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile012.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile013.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile014.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile015.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile016.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile017.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile018.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile019.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile020.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/green/tile021.png'),(72,72)))
        else :
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile000.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile001.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile002.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile003.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile004.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile005.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile006.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile007.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile008.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile009.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile010.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile011.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile012.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile013.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile014.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile015.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile016.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile017.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile018.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile019.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile020.png'),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load('./assets/images/portals/purple/tile021.png'),(72,72)))
        
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
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
            my_player = Player(j*32 -32, i*32 +32, my_platform_group, my_portal_group, my_bullet_group)
            my_player_group.add(my_player)



my_game = Game(my_player, my_zombie_group, my_platform_group, my_portal_group, my_bullet_group, my_ruby_group)

# main game loop here
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # jump 
            if event.key == pygame.K_SPACE:
                my_player.jump()
            # fire
            if event.key == pygame.K_UP:
                my_player.fire()

            # create zombie
            if event.key == pygame.K_RETURN:
                zombie = Zombie(my_platform_group, my_portal_group, 2, 7)
                my_zombie_group.add(zombie)


    # blit the background
    display_surface.blit(background_image, background_rect)

    # blit the tiles
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)
    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_bullet_group.update()
    my_bullet_group.draw(display_surface)

    my_zombie_group.update()
    my_zombie_group.draw(display_surface)

    my_ruby_group.update()
    my_ruby_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()