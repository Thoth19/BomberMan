import pygame, math
from classes import *
pygame.init()
screen = pygame.display.set_mode([555,555])
clock = pygame.time.Clock()

POWERUP_FREQUENCY = 15000 # higher means less frequent
SPEED_INCREASE_FACTOR = 0.5
BOMB_FUSE_LENGTH = 3000 # time in ms between plant and detonation
EXPLOSION_LIFE_TIME = 1000 # time in ms between explode and end

pygame.display.set_caption('BomberMan: A Game of Agility, Strategy and C4')
#init board

STANDARD_BOARD = [
[2,2,2,2,2,2,2,2,2,2,2],
[2,3,0,1,1,1,1,1,1,4,2],
[2,0,2,1,2,1,2,1,2,0,2],
[2,1,1,1,1,1,1,1,1,1,2],
[2,1,2,1,2,1,2,1,2,1,2],
[2,1,1,1,1,1,1,1,1,1,2],
[2,1,2,1,2,1,2,1,2,1,2],
[2,1,1,1,1,1,1,1,1,1,2],
[2,0,2,1,2,1,2,1,2,0,2],
[2,5,0,1,1,1,1,1,0,6,2],
[2,2,2,2,2,2,2,2,2,2,2]]
board = STANDARD_BOARD
#todo make boards randomized

all_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
granite_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == 2:
            granite = GraniteSprite((i,j))
            granite_group.add(granite)
            all_group.add(granite)
        if board[i][j] == 1:
            wall = WallSprite((i,j))
            wall_group.add(wall)
            all_group.add(wall)
        if board[i][j] == 3:
            player1 = PlayerSprite((i,j),(255,0,0))
            player_group.add(player1)
            all_group.add(player1)
        if board[i][j] == 4:
            player2 = PlayerSprite((i,j),(0,0,255))
            player_group.add(player2)
            all_group.add(player2)
        if board[i][j] == 5:
            player3 = PlayerSprite((i,j),(0,255,0))
            player_group.add(player3)
            all_group.add(player3)
        if board[i][j] == 6:
            player4 = PlayerSprite((i,j),(255,255,0))
            player_group.add(player4)
            all_group.add(player4)
screen.fill((224,224,224))
all_group.update()
all_group.draw(screen)
pygame.display.flip()

done = False
while sum([player1.alive, player2.alive, player3.alive, player4.alive])>1 and not(done):
    pygame.display.update()
    pygame.event.poll()
    clock.tick(30)

    corrupt_rect = []

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]: 
        pygame.display.quit()
        done = True

    if pressed[pygame.K_w]:
        corrupt_rect.append(player1.rect.copy())
        player1.move((0,-player1.speed))
        player1.rotate(0)
    if pressed[pygame.K_a]:
        corrupt_rect.append(player1.rect.copy())
        player1.move((-player1.speed,0))
        player1.rotate(90)
    if pressed[pygame.K_s]:
        corrupt_rect.append(player1.rect.copy())
        player1.move((0,player1.speed))
        player1.rotate(180)
    if pressed[pygame.K_d]:
        corrupt_rect.append(player1.rect.copy())
        player1.move((player1.speed,0))
        player1.rotate(-90)
    #add other players movements 
    if pressed[pygame.K_TAB] and player1.bombs < player1.bombs_max:
        corrupt_rect.append(player1.rect.copy())
        bomb = BombSprite((player1.position),player1.range)
        bomb_group.add(bomb)
        all_group.add(bomb)

    #update player position when they change squares
    player1.position = player1.rect.x/50,player1.rect.y/50

    all_group.update()
    for i in corrupt_rect:
        screen.fill((224,224,224), i)
    all_group.draw(screen)
    pygame.display.flip()