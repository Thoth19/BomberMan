import pygame, math,random
from classes import *
pygame.init()
screen = pygame.display.set_mode([555,555])
clock = pygame.time.Clock()

POWERUP_FREQUENCY = 20 # higher means less frequent
SPEED_INCREASE_FACTOR = 0.5
BOMB_FUSE_LENGTH = 100 # time in ms between plant and detonation
EXPLOSION_LIFE_TIME = 50 # time in ms between explode and end

pygame.display.set_caption('BomberMan: A Game of Agility, Strategy and C4')

pygame.mouse.set_visible(False)

# Initialize board
# We could use a loop to initialize, but that would make it 
# harder to test and change quickly. This representation also sllows 
# for easier visualization.
STANDARD_BOARD = [
[2,2,2,2,2,2,2,2,2,2,2],
[2,3,0,1,1,1,1,1,0,4,2],
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
# The array indicates what objects start where
# 2 indicates granite (solid, immunte to explosion)
# 1 indicates wall (solid, can be destroyed)
# 0 indicates blank tile
# 3,4,5,6 indicate players

#TODO: Make boards randomized so that game experiences can be different

all_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
granite_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

wall_dict={}
granite_dict={}

# Initialize the objects by putting them in their groups
for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == 1:
            wall = WallSprite((i,j))
            wall_group.add(wall)
            all_group.add(wall)
            wall_dict[(i,j)] = wall
        if board[i][j] == 2:
            granite = GraniteSprite((i,j))
            granite_group.add(granite)
            all_group.add(granite)
            granite_dict[(i,j)] = granite
        if board[i][j] == 3:
            player1 = PlayerSprite((i,j),(255,0,0),"red")
            player_group.add(player1)
            all_group.add(player1)
        if board[i][j] == 4:
            player2 = PlayerSprite((i,j),(0,0,255),"blue")
            player_group.add(player2)
            all_group.add(player2)
        if board[i][j] == 5:
            player3 = PlayerSprite((i,j),(0,255,0),"green")
            player_group.add(player3)
            all_group.add(player3)
        if board[i][j] == 6:
            player4 = PlayerSprite((i,j),(255,255,0),"yellow")
            player_group.add(player4)
            all_group.add(player4)

# Initialize the board itself by setting up the background
# and displaying the screen
screen.fill((224,224,224))
all_group.update()
all_group.draw(screen)
pygame.display.flip()


# Initialize player controls. We could do this next to the code that uses it,
# but it is constant over the course of the program, and we might want to 
# change it on future iterations

control_bomb = {player1:pygame.K_TAB, player2:pygame.K_SPACE, player3:pygame.K_RETURN,player4:pygame.K_KP0}
control_up = {player1:pygame.K_w, player2:pygame.K_i, player3:pygame.K_UP,player4:pygame.K_KP8}
control_down = {player1:pygame.K_s, player2:pygame.K_k, player3:pygame.K_DOWN,player4:pygame.K_KP5}
control_left = {player1:pygame.K_a, player2:pygame.K_j, player3:pygame.K_LEFT,player4:pygame.K_KP4}
control_right = {player1:pygame.K_d, player2:pygame.K_l, player3:pygame.K_RIGHT,player4:pygame.K_KP6}
players = [player1,player2,player3,player4]

done = False
time = 0
num_powerups = 0
# Continue playing the game until only one player is left and/or the game is quit
while sum([player1.alive, player2.alive, player3.alive, player4.alive])>1 and not(done):
    # We need to update the display and retrieve keyboard input
    pygame.display.update()
    pygame.event.poll()
    clock.tick(30)
    time += 1

    corrupt_rect = [] # list of rectangles to reset to normal color

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]: 
        pygame.display.quit()
        done = True

    # Using the control_bomb dictionary we process bomb placement commands
    for event in pygame.event.get(pygame.KEYUP):
        for player in control_bomb.keys():
            if event.key == control_bomb[player] and player.bombs < player.bombs_max and player.alive:
                corrupt_rect.append(player.rect.copy())
                bomb = BombSprite(player)
                bomb_group.add(bomb)
                all_group.add(bomb)
                player.bombs += 1
    
    # Using the controls dictionaries we process movement for all players
    for player in players:
        if player.alive:
            if pressed[control_up[player]]:
              corrupt_rect.append(player.rect.copy())  
              player.move((0,-player.speed))
              player.rotate(0)
            elif pressed[control_left[player]]:
                corrupt_rect.append(player.rect.copy())
                player.move((-player.speed,0))
                player.rotate(90)
            elif pressed[control_down[player]]:
                corrupt_rect.append(player.rect.copy())
                player.move((0,player.speed))
                player.rotate(180)
            elif pressed[control_right[player]]:
                corrupt_rect.append(player.rect.copy())
                player.move((player.speed,0))
                player.rotate(-90)

    #Check if bombs should explode
    for i in bomb_group:
        if i.time == BOMB_FUSE_LENGTH:
            i.owner.bombs -= 1
            center = ExplosionCenterSprite((i.position))
            explosion_group.add(center)
            all_group.add(center)
            corrupt_rect.append(center.rect.copy())
            # We need to replace the image with an explosion
            pos_x=[True, 1, 0]
            neg_x=[True,-1, 0]# hasn't hit a wall, x direction,y direction
            pos_y=[True, 0, 1]
            neg_y=[True, 0,-1]
            for j in range(1,bomb.owner.range+1):
                # Explosions propogate, but stop when the hit a block
                for angle in [pos_x,pos_y,neg_x,neg_y]:
                    if angle[0]:
                        if (i.position[0]+j*(angle[1]),i.position[1]+j*(angle[2])) in wall_dict.keys():
                            angle[0] = False
                            wall = wall_dict[i.position[0]+j*angle[1],i.position[1]+j*angle[2]]
                            corrupt_rect.append(wall.rect.copy())
                            wall_group.remove(wall)
                            all_group.remove(wall)
                            del wall_dict[i.position[0]+j*angle[1],i.position[1]+j*angle[2]]
                        elif (i.position[0]+j*angle[1],i.position[1]+j*angle[2]) in granite_dict.keys():
                            angle[0] = False
                        # else create a explosion line
                        else:
                            explosion = ExplosionLineSprite((i.position[0]+j*angle[1],i.position[1]+j*angle[2]),(angle[2] == 0))
                            explosion_group.add(explosion)
                            all_group.add(explosion)
                            corrupt_rect.append(wall.rect.copy())
               
            corrupt_rect.append(i.rect.copy())
            all_group.remove(i)
            bomb_group.remove(i)
    for explosion in explosion_group:
        # We also need to update the explosions like the bombs
        if explosion.time == EXPLOSION_LIFE_TIME:
            corrupt_rect.append(explosion.rect.copy())
            explosion_group.remove(explosion)
            all_group.remove(explosion)
    for player in player_group:
        player.position = player.rect.center[0]/50,player.rect.center[1]/50
        # Update which square the player is in

        # Players cannot move through walls or granite
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
        for granite in granite_group:
            if player.rect.colliderect(granite):
                if player.direction == -90:
                    player.rect.right = granite.rect.left
                elif player.direction == 90:
                    player.rect.left = granite.rect.right

                if player.direction == 0:
                    player.rect.top = granite.rect.bottom
                elif player.direction == 180:
                    player.rect.bottom = granite.rect.top
        # Players can pick up powerups
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
        # Players die when hitting explosions
        for explosion in explosion_group:
            if player.rect.colliderect(explosion):
                player.alive = 0
                player_group.remove(player)
                all_group.remove(player)
                corrupt_rect.append(player.rect.copy())

    # Bombs are only solid to a player if they are not currently inside of it
    # We want to leave the bomb's square, but not run through it later
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
                elif not(bomb.solid) and player.rect.colliderect(bomb):
                    vacated = False
            bomb.solid = vacated
  
    # Powerups spawn. If the square they try to land on is occupied, no powerup spawns.
    # Thus, there is incentive to clear out more of the board near you so more powerups
    # spawn there.
    if time % POWERUP_FREQUENCY == 0:
        place_here = True
        proposed_position = random.randint(1,9),random.randint(1,9)
        for i in all_group:
            if i.position == proposed_position:
                place_here = False
                break
        if place_here:
            powerup = PowerSprite(proposed_position, random.randint(1,3))
            powerup_group.add(powerup)
            all_group.add(powerup)

    
    all_group.update()
    for i in corrupt_rect:
        screen.fill((224,224,224), i)
    # We only need to draw over pixels that have changed
    all_group.draw(screen)
    pygame.display.flip()

# Sometimes the winner is hard to determine. So we print the color to terminal
for player in player_group:
    if player.alive == 1:
        print "The final living player is", player.name, "!"