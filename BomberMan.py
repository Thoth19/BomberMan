import pygame, math,random
from classes import *
pygame.init()
screen = pygame.display.set_mode([555,555])
clock = pygame.time.Clock()

POWERUP_FREQUENCY = 100 # higher means less frequent
SPEED_INCREASE_FACTOR = 0.5
BOMB_FUSE_LENGTH = 100 # time in ms between plant and detonation
EXPLOSION_LIFE_TIME = 50 # time in ms between explode and end

pygame.display.set_caption('BomberMan: A Game of Agility, Strategy and C4')
#init board

STANDARD_BOARD = [
[2,2,2,2,2,2,2,2,2,2,2],
[2,3,0,0,1,1,1,1,0,0,2],
[2,4,0,0,2,1,2,1,2,0,2],
[2,0,0,0,1,1,1,1,1,1,2],
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
explosion_group = pygame.sprite.Group()

wall_dict={}
granite_dict={}

for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == 2:
            granite = GraniteSprite((i,j))
            granite_group.add(granite)
            all_group.add(granite)
            granite_dict[(i,j)] = granite
        if board[i][j] == 1:
            wall = WallSprite((i,j))
            wall_group.add(wall)
            all_group.add(wall)
            wall_dict[(i,j)] = wall
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
time = 0
num_powerups = 0
while sum([player1.alive, player2.alive, player3.alive, player4.alive])>1 and not(done):
    pygame.display.update()
    pygame.event.poll()
    clock.tick(30)
    time += 1

    corrupt_rect = []

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]: 
        pygame.display.quit()
        done = True

    if pressed[pygame.K_w]and player1.alive:
        corrupt_rect.append(player1.rect.copy())
        player1.move((0,-player1.speed))
        player1.rotate(0)
    elif pressed[pygame.K_a]and player1.alive:
        corrupt_rect.append(player1.rect.copy())
        player1.move((-player1.speed,0))
        player1.rotate(90)
    elif pressed[pygame.K_s]and player1.alive:
        corrupt_rect.append(player1.rect.copy())
        player1.move((0,player1.speed))
        player1.rotate(180)
    elif pressed[pygame.K_d]and player1.alive:
        corrupt_rect.append(player1.rect.copy())
        player1.move((player1.speed,0))
        player1.rotate(-90)
    #add other players movements 
    if pressed[pygame.K_TAB] and player1.bombs < player1.bombs_max and player1.alive:
        corrupt_rect.append(player1.rect.copy())
        bomb = BombSprite(player1)
        bomb_group.add(bomb)
        all_group.add(bomb)
        player1.bombs += 1
        
    #update player position when they change squares
    player1.position = player1.rect.center[0]/50,player1.rect.center[1]/50
    # print player1.position
    for i in bomb_group:
        if i.time == BOMB_FUSE_LENGTH:
            i.owner.bombs -= 1
            center = ExplosionCenterSprite((i.position))
            explosion_group.add(center)
            all_group.add(center)
            corrupt_rect.append(center.rect.copy())
            pos_x=True
            neg_x =True
            pos_y=True
            neg_y=True
            for j in range(1,bomb.owner.range+1):
                #if you hit a block stop
                
                # if (i.position[0]+j,i.position[1]) in wall_dict.keys() and pos_x:
                if pos_x:
                    if (i.position[0]+j,i.position[1]) in wall_dict.keys():
                        pos_x = False
                        wall = wall_dict[i.position[0]+j,i.position[1]]
                        corrupt_rect.append(wall.rect.copy())
                        wall_group.remove(wall)
                        all_group.remove(wall)
                        del wall_dict[i.position[0]+j,i.position[1]]
                    elif (i.position[0]+j,i.position[1]) in granite_dict.keys():
                        pos_x = False
                    else:
                        explosion = ExplosionLineSprite((i.position[0]+j,i.position[1]),True)
                        explosion_group.add(explosion)
                        all_group.add(explosion)
                if neg_x:
                    if (i.position[0]-j,i.position[1]) in wall_dict.keys():
                        neg_x = False
                        wall =wall_dict[i.position[0]-j,i.position[1]]
                        corrupt_rect.append(wall.rect.copy())
                        wall_group.remove(wall)
                        all_group.remove(wall)
                        del wall_dict[i.position[0]-j,i.position[1]]
                    elif (i.position[0]-j,i.position[1]) in granite_dict.keys():
                        neg_x = False
                    else:
                        explosion = ExplosionLineSprite((i.position[0]-j,i.position[1]),True)
                        explosion_group.add(explosion)
                        all_group.add(explosion)
                if pos_y:
                    if (i.position[0],i.position[1]+j) in wall_dict.keys():
                        pos_y = False
                        wall =wall_dict[i.position[0],i.position[1]+j]
                        corrupt_rect.append(wall.rect.copy())
                        wall_group.remove(wall)
                        all_group.remove(wall)
                        del wall_dict[i.position[0],i.position[1]+j]
                    elif (i.position[0],i.position[1]+j) in granite_dict.keys():
                        pos_y = False
                    else:
                        explosion = ExplosionLineSprite((i.position[0],i.position[1]+j),False)
                        explosion_group.add(explosion)
                        all_group.add(explosion)
                if neg_y:
                    if (i.position[0],i.position[1]-j) in wall_dict.keys():
                        neg_y = False
                        wall =wall_dict[i.position[0],i.position[1]-j]
                        corrupt_rect.append(wall.rect.copy())
                        wall_group.remove(wall)
                        all_group.remove(wall)
                        del wall_dict[i.position[0],i.position[1]-j]
                    elif (i.position[0],i.position[1]-j) in granite_dict.keys():
                        neg_y = False
                    else:
                        explosion = ExplosionLineSprite((i.position[0],i.position[1]-j),False)
                        explosion_group.add(explosion)
                        all_group.add(explosion)
                #else create a explosion line
            corrupt_rect.append(i.rect.copy())
            all_group.remove(i)
            bomb_group.remove(i)
    for explosion in explosion_group:
        if explosion.time == EXPLOSION_LIFE_TIME:
            corrupt_rect.append(explosion.rect.copy())
            #bug here not removign all explosions why?
            explosion_group.remove(explosion)
            all_group.remove(explosion)
    for player in player_group:
        for wall in player_group:
            if player.rect.colliderect(wall) and wall != player:
                if player.direction == -90:
                    player.rect.right = wall.rect.left
                elif player.direction == 90:
                    player.rect.left = wall.rect.right
                    
                if player.direction == 0:
                    player.rect.top = wall.rect.bottom
                elif player.direction == 180:
                    player.rect.bottom = wall.rect.top
        for wall in wall_group:
            if player.rect.colliderect(wall):
                if player.direction == -90:
                    player.rect.right = wall.rect.left
                elif player.direction == 90:
                    player.rect.left = wall.rect.right
                    
                if player.direction == 0:
                    player.rect.top = wall.rect.bottom
                elif player.direction == 180:
                    player.rect.bottom = wall.rect.top
        for wall in granite_group:
            if player.rect.colliderect(wall):
                if player.direction == -90:
                    player.rect.right = wall.rect.left
                elif player.direction == 90:
                    player.rect.left = wall.rect.right

                if player.direction == 0:
                    player.rect.top = wall.rect.bottom
                elif player.direction == 180:
                    player.rect.bottom = wall.rect.top
        for powerup in powerup_group:
            if player.rect.colliderect(powerup):
                if powerup.style == 1:
                    player.range +=1
                elif powerup.style == 2:
                    player.speed += SPEED_INCREASE_FACTOR
                elif powerup.style == 3:
                    player.bombs_max += 1
                powerup_group.remove(powerup)
                all_group.remove(powerup)
                corrupt_rect.append(powerup.rect.copy())
        for explosion in explosion_group:
            if player.rect.colliderect(explosion):
                player.alive = 0
                player_group.remove(player)
                all_group.remove(player)

    #able to pass through explosions to begin
    for bomb in bomb_group:
            vacated = True
            for player in player_group:
                if player.rect.colliderect(bomb) and bomb.solid:
                    if player.direction == -90:
                        player.rect.right = bomb.rect.left
                    elif player.direction == 90:
                        player.rect.left = bomb.rect.right
                    if player.direction == 0:
                        player.rect.top = bomb.rect.bottom
                    elif player.direction == 180:
                        player.rect.bottom = bomb.rect.top
                    print 'get'
                elif not(bomb.solid) and player.rect.colliderect(bomb):
                    vacated = False
                    print "het"
                print vacated
                bomb.solid = vacated
    #powerups
    if (num_powerups + 1) * POWERUP_FREQUENCY < time:
        # print (num_powerups+1)*POWERUP_FREQUENCY
        num_powerups += 1
        problem = True
        loop_number = 0
        while problem:
            if loop_number >10:
                break
            loop_number += 1
            problem = False
            proposed_position = random.randint(1,9),random.randint(1,9)
            for i in all_group:
                if i.position == proposed_position:
                    problem = True
        if loop_number <=10 and not(problem):
            powerup = PowerSprite(proposed_position, random.randint(1,3))
            powerup_group.add(powerup)
            all_group.add(powerup)

    # print time
    all_group.update()
    for i in corrupt_rect:
        screen.fill((224,224,224), i)
    all_group.draw(screen)
    pygame.display.flip()

#TODO switch  to event q so that multiple boms works right