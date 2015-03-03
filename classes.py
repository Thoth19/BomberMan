import math, pygame, os

SQUARE_SIZE = 50
PLAYER_SIZE = 40
BOMB_SIZE = SQUARE_SIZE * 0.8
EXPLOSION_WIDTH = 30

INITIAL_PLAYER_SPEED = 4

# TODO: consider optimizing image creation for objects
#      Game runs fast enough without such optimizations

# Position variable refers to which square on the game board the object is on
# The Rect object holds the exact pixel position
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, position, color, name):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.color = color
        self.speed = INITIAL_PLAYER_SPEED
        self.range = 1
        self.bombs = 0
        self.bombs_max=1
        try:
            # Load image from folder
            # We use the os.path.join so it is cross platform
            self.image = pygame.image.load(os.path.join("images",'player.png')).convert()
        except:
            raise UserWarning, "Unable to find images."
        image2 = pygame.PixelArray(self.image)
        image2.replace((255,255,255),color)
        image3 = image2.make_surface()
        self.image = image3
        # We need to convert the image to have the correct color

        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
        self.direction = 0 #angle
        self.alive = 1
        self.name = name
    def rotate(self, direction):
        self.image = pygame.transform.rotate(self.image,direction-self.direction)
        self.direction = direction
    def move(self, position):
        if self.alive:
            self.rect.x , self.rect.y = position[0]+self.rect.x,position[1]+self.rect.y 
            # The position of rect.x and y is the upper left corner of the rect


class BombSprite(pygame.sprite.Sprite):
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)
        self.position = owner.position
        self.power = owner.range
        self.time = 0
        try:
            self.image = pygame.image.load(os.path.join("images",'bomb.png')).convert()
        except:
            raise UserWarning, "Unable to find images."
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 50 +5
        self.rect.y = self.position[1] * 50 +5
        self.owner = owner
        self.solid = False
    def update(self):
        self.time += 1
        # Bombs tick towards destruction

# Wall and granite are effectively the same other than color and 
# solidity. Since the number of objects is so small, and other objects
# such as powerups don't interact the same wasy as Wall and Granite do,
# it makes more sense to handle the solidity in the main based on which
# group the objects are in, rather than a private "solid" variable
class WallSprite(pygame.sprite.Sprite):
    # breakable
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.Surface([50,50])
        self.image.fill((144,144,144))
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
    def update(self):
        pass
class GraniteSprite(pygame.sprite.Sprite):
    # not breakable
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.Surface([50,50])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
    def update(self):
        pass
class ExplosionLineSprite(pygame.sprite.Sprite):
    def __init__(self, position, horiz):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        try:
            self.image = pygame.image.load(os.path.join("images",'fireStrip.png')).convert()
        except:
            raise UserWarning, "Unable to find images."
        self.image = pygame.transform.scale(self.image,(50,30))
        self.horiz = horiz # boolean for angle
        self.rect = self.image.get_rect()
        # Explosions can be either vertical or horizontal
        if not(horiz):
            self.image = pygame.transform.rotate(self.image,90)
            self.rect = self.image.get_rect()
            self.rect.x = position[0] * 50 + 10
            self.rect.y = position[1] * 50
        else:
            self.rect.x = position[0] * 50
            self.rect.y = position[1] * 50+10
        self.time = 0
    def update(self):
        self.time += 1
class ExplosionCenterSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        try:
            self.image = pygame.image.load(os.path.join("images",'fireCenter.png')).convert()
        except:
            raise UserWarning, "Unable to find images."
        self.image = pygame.transform.scale(self.image,(50,50))

        self.time = 0
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
    def update(self):
        self.time += 1
# All three powerups are a single object with one of three styles
# Since each powerup of a given type is isomorphic, it is better 
# to just deal with one powerup object that can do different things
# depending on which style it has
class PowerSprite(pygame.sprite.Sprite):
    def __init__(self, position, style):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        if style == 1:
            try:
                self.image = pygame.image.load(os.path.join("images",'powerupFire.png')).convert()
            except:
                raise UserWarning, "Unable to find images."
            self.image.set_colorkey((255,255,255))
            
        elif style == 2:
            try:
                self.image = pygame.image.load(os.path.join("images",'powerupSpeed.png')).convert()
            except:
                raise UserWarning, "Unable to find images."
            
            self.image.set_colorkey((0,0,0))
        else:
            try:
                self.image = pygame.image.load(os.path.join("images",'powerupBomb.png')).convert()
            except:
                raise UserWarning, "Unable to find images."
            self.image.set_colorkey((0,0,0))
        self.style = style;
        
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50 +5
        self.rect.y = position[1] * 50 +5