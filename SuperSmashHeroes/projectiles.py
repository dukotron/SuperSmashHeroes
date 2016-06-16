import pygame
from pygame import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, owner):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        if self.direction == 1:
            self.rect = Rect(pos_x + 20, pos_y + 10, 40, 20)
        else:
            self.rect = Rect(pos_x - 20, pos_y + 10, 40, 20)
        self.image = pygame.image.load("pew.png").convert_alpha()
        self.owner = owner
        self.speed = 20
        self.damage = 10

    def fire(self, display):
        if self.direction == 1:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x > 1920 or self.rect.x < -40:
            del self
        else:
            display.blit(self.image, (self.rect.x, self.rect.y))
