import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

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
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.rect(self.image, color, [0, 0, 21, 21])

        self.rect = pygame.rect.Rect((0, 0, 21, 21))


    def moveRight(self, pixels):

        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels


