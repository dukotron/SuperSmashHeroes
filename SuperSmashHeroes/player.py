import pygame
from pygame import *
from projectiles import Projectile
from random import randint

class Entity(pygame.sprite.Sprite):
    def __init__(self, count, ch):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = randint(640, 1280)
        self.pos_y = -130
        self.speed_x = 0
        self.speed_y = 4
        self.sprites = []
        self.count = count
        #related to horizontal movement
        self.moving = False
        self.delay = 0
        self.select = 0
        self.direction = 1
        #related to vertical movement
        self.jump = 0
        self.jumped = False
        #related to attack
        self.shoot = False
        self.projectiles = []
        self.id = randint(1, 587632)
        #related to hp
        self.p1img = pygame.image.load(ch).convert_alpha()
        self.hp = 150
        self.ratio = 365/self.hp
        self.death = 0
        self.dead = False
        
    def load_sheet(self, start, sprite_size, file):
        start_x, start_y = start
        size_x, size_y = sprite_size

        sheet = pygame.image.load(file).convert_alpha()
        rect = sheet.get_rect()
        for i in range(0, rect.height, size_y):
            for i in range(0, rect.width, size_x):
                sheet.set_clip(pygame.Rect(start_x, start_y, size_x, size_y))
                sprite = sheet.subsurface(sheet.get_clip())
                #sprite = pygame.transform.scale(sprite, (512, 512))
                self.sprites.append(sprite)
                start_x += size_x

            start_y += size_y
            start_x = 0

    def collision(self, platforms):
        collidedp = self.rect.collidelist(platforms)

        if collidedp != -1 and self.speed_y > 0:
            self.speed_y = 0
            self.pos_y = platforms[collidedp].pos_y - 84
            self.jumped = False
            self.jump = 0
        elif collidedp == -1 and self.pos_y < 1080:
            self.speed_y += 0.35
        
        if self.pos_y > 1080 and self.hp > 0:
            self.hp -= 3
            self.dead = True
        elif self.hp <= 0 and self.death == 100:
            self.hp = 154
            self.pos_y = -130
            self.pos_x = 940
            self.death = 0
            self.dead = False
        elif self.dead == True:
            self.death += 1
        elif self.hp <= 0:
            self.dead = True

    def update(self, display, platforms, players):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.rect = pygame.Rect(self.pos_x, self.pos_y + 84, 40, 2)
        self.rect2 = pygame.Rect(self.pos_x, self.pos_y, 40, 86)

        self.collision(platforms)
        self.collision_p(players)
        
        if self.moving == True or self.shoot == True:
            self.delay += 1

        if self.shoot == True:
            self.select = 9
            if self.delay == 18:
                self.delay = 0
                self.shoot = False
        elif self.jumped == True:
            self.select = 7
            self.delay = 0
        elif self.moving == True and self.delay == 9:
            if self.select >= 6:
                self.select = 1
                self.delay = 0
            else:
                self.select += 1
                self.delay = 0
        elif self.moving == False:
            self.select = 0
            self.delay = 0

        sprite = self.sprites[self.select]   
        if self.direction == 1:
            display.blit(sprite, (self.pos_x, self.pos_y))
        else:
            sprite = pygame.transform.flip(sprite, True, False)
            display.blit(sprite, (self.pos_x, self.pos_y))

        for one in self.projectiles:
            one.fire(display)

class Player1(Entity):
    def __init__(self, count, ch):
        Entity.__init__(self, count, ch)

    def collision_p(self, players):
        collidepr = self.rect2.collidelist(players[1].projectiles)

        if collidepr != -1 and self.hp > 0:
            self.hp -= 3
            del players[1].projectiles[collidepr]
        
    def update_p(self, display, platforms, players):
        self.update(display, platforms, players)
        
        pygame.draw.rect(display, (255,0,0), (118, 968, self.hp*self.ratio, 18))
        display.blit(self.p1img, (16, 934))

    def move(self, event):
        if event.key == pygame.K_d:
            self.speed_x = 3
            self.moving = True
            self.direction = 1
        elif event.key == pygame.K_a:
            self.speed_x = -3
            self.moving = True
            self.direction = 0
        elif event.key == pygame.K_w:
            if self.jump == 2:
                pass
            else:
                self.speed_y = -10
                self.jumped = True
                self.jump += 1
        elif event.key == pygame.K_h:
            self.shoot = True
            self.projectiles.append(Projectile(self.pos_x, self.pos_y, self.direction, self.id))
            

    def stop(self, event):
        if event.key == pygame.K_d and self.speed_x != -3:
            self.speed_x = 0
            self.moving = False
        elif event.key == pygame.K_a and self.speed_x != 3:
            self.speed_x = 0
            self.moving = False

class Player2(Entity):
    def __init__(self, count, ch):
        Entity.__init__(self, count, ch)

    def collision_p(self, players):
        collidepr = self.rect2.collidelist(players[0].projectiles)

        if collidepr != -1 and self.hp > 0:
            self.hp -= 3
            del players[0].projectiles[collidepr]
        
    def update_p(self, display, platforms, players):
        self.update(display, platforms, players)
        
        pygame.draw.rect(display, (255,0,0), (1803, 968, -self.hp*self.ratio, 18))
        display.blit(self.p1img, (1392, 934))

    def move(self, event):
        if event.key == pygame.K_RIGHT:
            self.speed_x = 3
            self.moving = True
            self.direction = 1
        elif event.key == pygame.K_LEFT:
            self.speed_x = -3
            self.moving = True
            self.direction = 0
        elif event.key == pygame.K_UP:
            if self.jump == 2:
                pass
            else:
                self.speed_y = -10
                self.jumped = True
                self.jump += 1
        elif event.key == pygame.K_KP4:
            self.shoot = True
            self.projectiles.append(Projectile(self.pos_x, self.pos_y, self.direction, self.id))
            
    def stop(self, event):
        if event.key == pygame.K_RIGHT and self.speed_x != -3:
            self.speed_x = 0
            self.moving = False
        elif event.key == pygame.K_LEFT and self.speed_x != 3:
            self.speed_x = 0
            self.moving = False
