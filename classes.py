import math, pygame #make for multiple os

SQUARE_SIZE = 50
PLAYER_SIZE = 40
BOMB_SIZE = SQUARE_SIZE * 0.8
EXPLOSION_WIDTH = 30

INITIAL_PLAYER_SPEED = 3

#position always refers to square. use rect to store pixel position
class PlayerSprite(pygame.sprite.Sprite):
	def __init__(self, position, color):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.color = color
		self.speed = INITIAL_PLAYER_SPEED
		self.range = 1
		self.bombs = 1
		self.image = pygame.image.load('player.png').convert()
		image2 = pygame.pxarray(self.image)
		image3 = image2.replace((255,255,255),color)
		image4 = image3.make_surface()
		self.image = image4
		self.rect = self.image.get_rect()
		self.direction = 0 #angle
	def rotate(self, direction):
		self.image = pygame.transform.rotate(self.image,direction-self.direction)
		self.direction = direction
	def move(self, position):
		self.rect.x , self.rect.y = position #note this is upper left corner

class BombSprite(pygame.sprite.Sprite):
	def __init__(self, position, power):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.power = power
		self.time = 0
	def update(self):
		self.time += 1
class WallSprite(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('bomb.png').convert()
        self.rect = self.image.get_rect()
    def update(self):
    	pass
class ExplosionLineSprite(pygame.sprite.Sprite):
	def __init__(self, position, horiz):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('fireStrip.png').convert()
        self.horiz = horiz #boolean for angle
        if not(horiz):
        	self.image = pygame.transform.rotate(self.image,90)
        self.time = 0
    def update(self):
    	self.time += 1
class ExplosionCenterSprite(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('fireCenter.png').convert()
        self.time = 0
    def update(self):
    	self.time += 1
class FirePowerSprite(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('powerupFire.png').convert()
class SpeedPowerSprite(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('powerupSpeed.png').convert()
class BombPowerSprite(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
        self.image = pygame.image.load('powerupBomb.png').convert()