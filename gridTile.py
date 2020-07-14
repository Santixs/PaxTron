import pygame, colors

#Tile object, each of the "squares" on the grid is a different tile

class Grid(pygame.sprite.Sprite):

    def __init__(self, x, y, owner):
        super().__init__()

        self.width = self.height = 20
        self.owner = owner
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colors.BLACK)
        self.image.set_colorkey(colors.BLACK)

        pygame.draw.rect(self.image, colors.WHITE, [0, 0, 20, 20])
        self.rect = pygame.rect.Rect((x, y, 16, 16))
        self.setOwner(owner)

    def setOwner(self, owner):
        self.owner = owner
        if self.owner.name == "No":
            pass
        elif self.owner.name == "playerA":
            pygame.draw.rect(self.image, colors.RED, [0, 0, 20, 20])


        elif self.owner.name == "playerB":
            pygame.draw.rect(self.image, colors.GREEN, [0, 0, 20, 20])

        elif self.owner.name == "Obstacle":
            pygame.draw.rect(self.image, colors.BLACK, [0, 0, 20, 20])

        elif self.owner.name == "Enemy":
            pygame.draw.rect(self.image, colors.GREYD, [0, 0, 20, 20])


