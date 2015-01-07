import math, pygame #make for multiple os

SQUARE_SIZE = 50
PLAYER_SIZE = 40
BOMB_SIZE = SQUARE_SIZE * 0.8
EXPLOSION_WIDTH = 30

INITIAL_PLAYER_SPEED = 3

#consider optimizing image creation for objects

#position always refers to square. use rect to store pixel position
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, position, color):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.color = color
        self.speed = INITIAL_PLAYER_SPEED
        self.range = 1
        self.bombs = 0
        self.bombs_max=5
        self.image = pygame.image.load('player.png').convert()
        image2 = pygame.PixelArray(self.image)
        image2.replace((255,255,255),color)
        image3 = image2.make_surface()
        self.image = image3
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
        self.direction = 0 #angle
        self.alive = 1
    def rotate(self, direction):
        self.image = pygame.transform.rotate(self.image,direction-self.direction)
        self.direction = direction
    def move(self, position):
        if self.alive:
            self.rect.x , self.rect.y = position[0]+self.rect.x,position[1]+self.rect.y #note this is upper left corner


class BombSprite(pygame.sprite.Sprite):
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)
        self.position = owner.position
        self.power = owner.range
        self.time = 0
        self.image = pygame.image.load('bomb.png').convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 50 +5
        self.rect.y = self.position[1] * 50 +5
        self.owner = owner
    def update(self):
        self.time += 1
class WallSprite(pygame.sprite.Sprite):
    #breakable
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
    #not breakable
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
        self.image = pygame.image.load('fireStrip.png').convert()
        self.image = pygame.transform.scale(self.image,(50,30))
        self.horiz = horiz #boolean for angle
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
        if not(horiz):
            self.image = pygame.transform.rotate(self.image,90)
            self.rect.x += 10
        else:
            self.rect.y +=10
        self.rect = self.image.get_rect()
        self.time = 0
    def update(self):
        self.time += 1
class ExplosionCenterSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.image.load('fireCenter.png').convert()
        self.image = pygame.transform.scale(self.image,(50,50))

        self.time = 0
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50
        self.rect.y = position[1] * 50
    def update(self):
        self.time += 1
#consider powerups being one object with a variable and three possible images
class PowerSprite(pygame.sprite.Sprite):
    def __init__(self, position, style):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        if style == 1:
            self.image = pygame.image.load('powerupFire.png').convert()
            self.image.set_colorkey((255,255,255))
            self.style = 1
        elif style == 2:
            self.image = pygame.image.load('powerupSpeed.png').convert()
            self.style = 2
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pygame.image.load('powerupBomb.png').convert()
            self.style = 3
            self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * 50 +5
        self.rect.y = position[1] * 50 +5