# Import the pygame library and initialise the game engine
import pygame, colors
from MyPlayer import player
from gridTile import Grid


def draw():
    screen.fill(colors.BLACK)
    #The gris is drawn
    grid_list.draw((screen))
    #the players are drawn
    all_sprites_list.draw(screen)

    #Health and score bar, the number is truncated to 2 decimals
    scoreA = "{:.2f}".format(playerA.score/numberTiles*100)
    scoreB = "{:.2f}".format(playerB.score / numberTiles * 100)

    labelA = font.render("PlayerA: " + scoreA + "% and " + str(playerA.lifes) + " lifes", 1, colors.RED)
    screen.blit(labelA, (400, 18))
    labelB = font.render("PlayerB: " + scoreB + "% and " + str(playerB.lifes) + " lifes", 1, colors.GREEN)
    screen.blit(labelB, (600, 18))

def change(player):
    #Every time a player moves, the ownership of that tile is checked and a life is lost if it
    # is another player's, if it is nobody's it becomes that player's
    tile = matrix[coordToIndex(player.rect.center[0])][coordToIndex(player.rect.center[1]-21)]
    if tile.owner.name == 'No' or tile.owner.name ==player.name:
        tile.setOwner(player)
        player.score += 1
    else:
        player.lifes -= 1
        checkLifes(player)

    # To allow passing through another player's zone we have to change the if and else for this
    '''tile.owner.score -= 1
    tile.setOwner(player)
    player.score +=1'''


def coordToIndex(coord):
    #the coordinates are transformed into an index
    #The +1 is for the margin between tiles
    return int((coord - 1) / (block_size + 1))

def knock(player,side):
    #When one player is in the border of the screen loses one life and it is moved behind
    if side == "left": player.moveRight(126)
    elif side == "right": player.moveLeft(126)
    elif side == "up": player.moveDown(126)
    elif side == "down": player.moveUp(126)

    player.lifes -= 1
    checkLifes(player)



def devMode():
    #It only shows the x and y coordinates of each player
    labelAA = font.render("PlayerA:  X:"+ str(playerA.rect.x) + ",  Y:" + str(playerA.rect.y), 1, colors.WHITE)
    screen.blit(labelAA, (50, 18))
    labelBB = font.render("PlayerB:  X:" + str(playerB.rect.x) + ",  Y:" + str(playerB.rect.y), 1, colors.WHITE)
    screen.blit(labelBB, (200, 18))

def checkLifes(player):
    if (player.lifes == 0):
        global loser, mode
        loser = player.name
        mode = "End"


def reset():
    global carryOn, enableDevMode, all_sprites_list, playerA, playerB, mode, loser

    all_sprites_list = pygame.sprite.Group()

    playerA = player("playerA", colors.REDD, 1)
    playerA.rect.x = 0
    playerA.rect.y = 42

    playerB = player("playerB", colors.GREEND, 1)
    playerB.rect.x = 778
    playerB.rect.y = 42

    all_sprites_list.add(playerA)
    all_sprites_list.add(playerB)

    mode = "Normal"
    loser = "No"
    carryOn = True
    screen.fill(colors.BLACK)
    enableDevMode = False



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




def keyPressed(keys):
    global mode, enableDevMode
    if keys[pygame.K_p]:
        enableDevMode = True

    if keys[pygame.K_ESCAPE]:
        mode = "Pause"

    # Player1
    if keys[pygame.K_a]:
        if playerA.rect.x > 2:
            playerA.moveLeft(playerA.speed)
            change(playerA)
        else:
            knock(playerA, "left")
    elif keys[pygame.K_d]:
        if playerA.rect.x < 771:
            playerA.moveRight(playerA.speed)
            change(playerA)
        else:

            knock(playerA, "right")
    elif keys[pygame.K_w]:
        if playerA.rect.y > 44:
            playerA.moveUp(playerA.speed)
            change(playerA)
        else:
            knock(playerA, "up")
    elif keys[pygame.K_s]:
        if playerA.rect.y < 608:
            playerA.moveDown(playerA.speed)
            change(playerA)
        else:
            knock(playerA, "down")

    # Player2
    if keys[pygame.K_LEFT]:
        if playerB.rect.x > 2:
            playerB.moveLeft(playerB.speed)
            change(playerB)
        else:
            knock(playerB, "left")
    elif keys[pygame.K_RIGHT]:
        if playerB.rect.x < 778:
            playerB.moveRight(playerB.speed)
            change(playerB)
        else:
            knock(playerB, "right")
    elif keys[pygame.K_UP]:
        if playerB.rect.y > 44:
            playerB.moveUp(playerB.speed)
            change(playerB)
        else:
            knock(playerB, "up")
    elif keys[pygame.K_DOWN]:
        if playerB.rect.y < 608:
            playerB.moveDown(playerB.speed)
            change(playerB)
        else:
            knock(playerB, "down")


pygame.init()
# Open a new window
barSize = 42
size = (798,588+barSize)
numberTiles = 1064
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MySnake Game")

# Health and score bar
font = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 48)
font3 = pygame.font.Font(None, 100)

clock = pygame.time.Clock()

createGrid()
reset()


# -------- Main Program Loop -----------

while carryOn:
    pygame.display.flip()
    # Limit to 10 frames per second
    clock.tick(10)

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop


    if mode == "Pause":
        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 10))  # notice the alpha value in the color
        screen.blit(s, (0, 0))
        labelP = font2.render("Pause Mode, press escape to return to the game", 20, colors.BLACK)
        screen.blit(labelP, (20, 300))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            mode = "Normal"



    elif mode == "End":

        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 10))  # notice the alpha value in the color
        screen.blit(s, (0, 0))
        labelP = font2.render("The loser is " + loser, 20, colors.RED)
        screen.blit(labelP, (65, 280))


    elif mode == "Normal":

        draw()
        keyPressed(pygame.key.get_pressed())
        if enableDevMode: devMode()



# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

