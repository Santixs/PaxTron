import pygame, colors
from MyPlayer import player
from gridTile import Grid
from random import randint, choice
from math import trunc
#--------------------------Options--------------------------
goOverOwnTilesAllowed = False
goOverOthersTilesAllowed = False
edgesRemoveLives = True
percentageToWin = 0.51
numberObstacles = 50
numberEnemies = 0 #Unfinished
numberLifes = 1

##----------------------------------------------------------

def draw():
    screen.fill(colors.BLACK)
    #The gris is drawn
    grid_list.draw((screen))
    #the players are drawn
    all_sprites_list.draw(screen)
    enemies_list.draw(screen)

    #Health and score bar, the number is truncated to 2 decimals
    scoreA = "{:.2f}".format(playerA.score/numberTiles*100)
    scoreB = "{:.2f}".format(playerB.score / numberTiles * 100)
    total = "{:.2f}".format( numberTilesNoOwner/ numberTiles * 100)
    labelA = font.render("PlayerA: " + scoreA + "% and " + str(playerA.lifes) + " lifes", 1, colors.RED)
    screen.blit(labelA, (400, 18))
    labelB = font.render("PlayerB: " + scoreB + "% and " + str(playerB.lifes) + " lifes", 1, colors.GREEN)
    screen.blit(labelB, (600, 18))
    labelTotal = font.render("Left:" + total, 1, colors.GREEN)
    screen.blit(labelTotal, (200, 18))

def change(player):
    #Every time a player moves, the ownership of that tile is checked and a life is lost if it
    # is another player's, if it is nobody's it becomes that player's

    global numberTilesNoOwner

    tile = matrix[coordToIndex(player.rect.center[0])][coordToIndex(player.rect.center[1]-21)]

    if not goOverOthersTilesAllowed :
        if tile.owner.name == 'No':
            tile.setOwner(player)
            player.score += 1
            numberTilesNoOwner -=1
        elif tile.owner.name == player.name and goOverOwnTilesAllowed: pass
        else:
            player.lifes -= 1
            checkLifes(player)
    else:
        tile.owner.score -= 1
        tile.setOwner(player)
        player.score +=1

    checkWinner()


def checkWinner():
    global mode, numberTilesNoOwner
    if numberTilesNoOwner < numberTiles*percentageToWin : mode = "Winner"

def coordToIndex(coord):
    #the coordinates are transformed into an index
    #The +1 is for the margin between tiles
    return trunc((coord - 1) / (block_size + 1))

def knock(player,side):
    #When one player is in the border of the screen loses one life and it is moved behind
    player.move(side, 126)
    player.lifes -= 1
    checkLifes(player)



def checkLifes(player):
    if (player.lifes == 0):
        global loser, mode
        loser = player.name
        mode = "End"


def reset():
    global carryOn, all_sprites_list, playerA, playerB, mode, loser, numberTilesNoOwner, enemies_list, moveEnemies

    createGrid()

    numberTilesNoOwner = numberTiles

    all_sprites_list = pygame.sprite.Group()
    enemies_list = pygame.sprite.Group()



    playerA = player("playerA", colors.REDD, numberLifes )
    playerA.rect.x = 0
    playerA.rect.y = 42

    playerB = player("playerB", colors.GREEND, numberLifes )
    playerB.rect.x = 778
    playerB.rect.y = 42

    all_sprites_list.add(playerA)
    all_sprites_list.add(playerB)


    #To set the initial tile ownership
    change(playerA)
    change(playerB)

    generateObstacles()
    generateEnemies()


    mode = "Normal"
    loser = "No"
    carryOn = True

    screen.fill(colors.BLACK)


def createGrid():
    global block_size, rows, cols, noOwner, matrix, nGrid, grid_list

    grid_list = pygame.sprite.Group()

    block_size = 20  # Set the size of the grid block
    # We calculate the number of rows and columns dividing thw width and length by the size of each tile plus the margin
    rows, cols = (int(size[0] / (block_size + 1)), int((size[1] + barSize) / (block_size + 1)))

    noOwner = player("No", colors.WHITE, 3, numberTiles)
    # We create the matrix and draw the grid
    matrix = [[0] * cols for i in range(rows)]
    for x in range(1, size[0], block_size + 1):
        for y in range(barSize, size[1] + barSize, block_size + 1):
            nGrid = Grid(x, y, noOwner)
            grid_list.add(nGrid)
            # We translate the coordinates into the index of the bi-dimensional matrix
            matrix[coordToIndex(x)][coordToIndex(y)] = nGrid



def generateEnemies():
    global enemyList
    enemyList = []

    for num in range(numberEnemies):
        enemy = player("Enemy", colors.GREYD, 120, numberTiles)
        enemy.speed=5
        #21 is the size of each tile, 38 the number of tiles in the x axis and 28 in the y axis
        #Since we do not want to have an enemy between 2 tiles we generate a discrete value
        x = 21*randint(1, 38)
        y = 21*randint(1, 28)
        enemy.rect.x = x
        enemy.rect.y = y
        enemies_list.add(enemy)
        enemyList.append(enemy)
        matrix[coordToIndex(x)][coordToIndex(y)].setOwner(enemy)


def moveEnemies():
    pass
    #Unfinished
    ''' for num in range(numberEnemies):
        enemyList[num].move(choice(directions))
        #change(enemyList[num])'''

def generateObstacles():
    obstacle = player("Obstacle", colors.BLACK, 0, numberTiles)
    for num in range(numberObstacles):
        x = randint(0, size[0])
        y = randint(22, size[1])
        matrix[coordToIndex(x)][coordToIndex(y)].setOwner(obstacle)


def keyPressed():
    global mode

    if keys[pygame.K_ESCAPE]:
        mode = "Pause"
    # Up -> 1, Right -> 2, Down -> -1, Left -> -2
    # Player1
    if keys[pygame.K_a]:
        if playerA.rect.x > 2:
            playerA.move(-2,playerA.speed)
            change(playerA)
        else:
           if edgesRemoveLives : knock(playerA, -2)
    elif keys[pygame.K_d]:
        if playerA.rect.x < 771:
            playerA.move(2,playerA.speed)
            change(playerA)
        else:

            if edgesRemoveLives: knock(playerA, 2)
    elif keys[pygame.K_w]:
        if playerA.rect.y > 44:
            playerA.move(1,playerA.speed)
            change(playerA)
        else:
            if edgesRemoveLives :knock(playerA, 1)
    elif keys[pygame.K_s]:
        if playerA.rect.y < 608:
            playerA.move(-1,playerA.speed)
            change(playerA)
        else:
            if edgesRemoveLives :knock(playerA, -1)

    # Player2
    if keys[pygame.K_LEFT]:
        if playerB.rect.x > 2:
            playerB.move(-2,playerB.speed)
            change(playerB)
        else:
            if edgesRemoveLives :knock(playerB,-2)
    elif keys[pygame.K_RIGHT]:
        if playerB.rect.x < 778:
            playerB.move(2,playerB.speed)
            change(playerB)
        else:
            if edgesRemoveLives :knock(playerB, 2)
    elif keys[pygame.K_UP]:
        if playerB.rect.y > 44:
            playerB.move(1,playerB.speed)
            change(playerB)
        else:
            if edgesRemoveLives :knock(playerB, 2)
    elif keys[pygame.K_DOWN]:
        if playerB.rect.y < 608:
            playerB.move(-1,playerB.speed)
            change(playerB)
        else:
            if edgesRemoveLives :knock(playerB, -1)


pygame.init()
# Open a new window
barSize = 42
size = (798,588+barSize)#798,630
numberTiles = 1064
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PaxTron")

directions = [1,-1,2,-2] #Up -> 1, Right -> 2, Down -> -1, Left -> -2
# Health and score bar
font = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 48)
font3 = pygame.font.Font(None, 100)

clock = pygame.time.Clock()
reset()


#With this windows size, there are 1064 tiles (38*28)


# -------- Main Program Loop -----------

while carryOn:
    keys = pygame.key.get_pressed()
    pygame.display.flip()
    # Limit to 10 frames per second
    clock.tick(10)
    moveEnemies()

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop


    if mode == "Pause":
        screen.fill((255, 255, 255, 10))
        labelP = font2.render("Pause Mode, press escape to return to the game", 20, colors.BLACK)
        screen.blit(labelP, (20, 300))

        if keys[pygame.K_ESCAPE]:
            mode = "Normal"



    elif mode == "End":

        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 10))  # notice the alpha value in the color
        screen.blit(s, (0, 0))
        labelP = font3.render("The loser is " + loser, 20, colors.RED)
        screen.blit(labelP, (65, 280))

        if keys[pygame.K_1]:
            reset()

    elif mode == "Winner":

        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 10))  # notice the alpha value in the color
        screen.blit(s, (0, 0))
        if playerA.score > playerB.score: winner = playerA.name
        else: winner = playerB.name
        labelP = font3.render("The Winner is " + winner, 20, colors.RED)
        screen.blit(labelP, (25, 280))

        if keys[pygame.K_1]:
            reset()


    elif mode == "Normal":

        draw()
        keyPressed()




# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

