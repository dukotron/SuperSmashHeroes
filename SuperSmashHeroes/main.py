import pygame
from pygame import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = 0
        self.speed_y = 8
        self.sprites = []
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
        elif collidedp == -1:
            self.speed_y += 0.35

    def update(self, display, platforms):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.rect = pygame.Rect(self.pos_x, self.pos_y + 84, 40, 2)

        self.collision(platforms)
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
            one.fire()

    def move(self, event):
        if event.key == pygame.K_RIGHT:
            self.speed_x = 4
            self.moving = True
            self.direction = 1
        elif event.key == pygame.K_LEFT:
            self.speed_x = -4
            self.moving = True
            self.direction = 0
        elif event.key == pygame.K_UP:
            if self.jump == 2:
                pass
            else:
                self.speed_y = -10
                self.jumped = True
                self.jump += 1
        elif event.key == pygame.K_h:
            self.shoot = True
            self.projectiles.append(Projectile(self.pos_x, self.pos_y, self.direction))
            

    def stop(self, event):
        if event.key == pygame.K_RIGHT and self.speed_x != -4:
            self.speed_x = 0
            self.moving = False
        elif event.key == pygame.K_LEFT and self.speed_x != 4:
            self.speed_x = 0
            self.moving = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, length, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.pos_y = pos_y #used to calculate fall missplacement
        self.rect = pygame.Rect(pos_x, pos_y, length*32, height)
        self.image = pygame.image.load(image).convert_alpha()

    def draw(self, pos_x, pos_y, length, display):
        for i in range(0, length):
            display.blit(self.image, (pos_x + 32 * i, pos_y))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(pos_x + 20, pos_y + 10, 40, 20)
        self.image = pygame.image.load("pew.png").convert_alpha()
        self.speed = 20
        self.direction = direction
        self.display = pygame.display.get_surface()

    def fire(self):
        if self.direction == 1:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x > 1920 or self.rect.x < 0:
            self.kill()
        else:
            self.display.blit(self.image, (self.rect.x, self.rect.y))

def main():
    pygame.init()
    info = pygame.display.Info()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    background = pygame.image.load("placeholderbg.jpg").convert_alpha()
    background = pygame.transform.scale(background, (info.current_w, info.current_h))

    font = pygame.font.SysFont("comicsansms", 24)

    player = Player(info.current_w//2 - 20, -130)
    player.load_sheet((0, 0), (40, 86), "placeholder.png")

    #t = top, m = middle, b = bottom, l/r = left/right, p = platform
    #0-tp, 1-mlp, 2-mmp, 3-mrp, 4-blp, 5-brp
    #(x,y - starting corner, a - length in blocks of 32x32, b - height of collision)
    platforms = []
    platforms.append(Platform(info.current_w // 60 * 20, info.current_h // 4, 20, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 5, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 25, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 45, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 10, info.current_h // 4 * 3, 15, 24, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 35, info.current_h // 4 * 3, 15, 24, "placeholdert.png"))

    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                player.move(event)
        elif event.type == pygame.KEYUP:
            player.stop(event)

        display.blit(background, (0, 0))
        display.blit(font.render("FPS: " + str(int(clock.get_fps())), 1, (0,0,0)), (0,0))

        
        player.update(display, platforms)
        #x,y - 32x32 corner start pos, a - length of platform in 32x32 blocks
        platforms[0].draw(info.current_w // 60 * 20, info.current_h // 4, 20, display)
        platforms[1].draw(info.current_w // 60 * 5, info.current_h // 4 * 2, 10, display)
        platforms[2].draw(info.current_w // 60 * 25, info.current_h // 4 * 2, 10, display)
        platforms[3].draw(info.current_w // 60 * 45, info.current_h // 4 * 2, 10, display)
        platforms[4].draw(info.current_w // 60 * 10, info.current_h // 4 * 3, 15, display)
        platforms[5].draw(info.current_w // 60 * 35, info.current_h // 4 * 3, 15, display)
        
        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption("Super Smash Heroes")
        
    pygame.quit()

if __name__ == "__main__":
    main()

