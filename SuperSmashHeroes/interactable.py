import pygame
from pygame import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, length, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.pos_y = pos_y #used to calculate fall missplacement
        self.rect = pygame.Rect(pos_x, pos_y, length*32, height)
        self.image = pygame.image.load(image).convert_alpha()

    def draw(self, pos_x, pos_y, length, display):
        for i in range(0, length):
            display.blit(self.image, (pos_x + 32 * i, pos_y))
