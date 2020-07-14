import pygame
import colors

#Player class
class player(pygame.sprite.Sprite):

    def __init__(self, name, color, lifes,score=0):
        super().__init__()
        self.name = name
        self.color = color
        self.lifes = lifes
        self.speed = 21
        self.width = self.height = 25
        self.score = score
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colors.WHITE)
        self.image.set_colorkey(colors.WHITE)

        pygame.draw.rect(self.image, color, [0, 0, 21, 21])

        self.rect = pygame.rect.Rect((0, 0, 21, 21))

    def move(self,direction, pixels = 21):
        #Up -> 1, Right -> 2, Down -> -1, Left -> -2
        if direction == 1 or direction == -1:
            self.rect.y += pixels*-direction
        else:
            self.rect.x += pixels*(direction/2)