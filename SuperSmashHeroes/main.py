import pygame
from pygame import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y+80, 40, 86)
        self.speedx = 0
        self.speedy = 8
        self.njump = 0
        self.delay = 0
        self.select = 0
        self.direction = 1
        self.moving = False
        self.jumped = False
        self.fall = True
        self.sprites = []
        self.display = pygame.display.get_surface()

    def load_sheet(self, start, sprite_size, file):
        start_x, start_y = start
        size_x, size_y = sprite_size

        sheet = pygame.image.load(file).convert_alpha()
        rect = sheet.get_rect()
        for i in range(0, rect.height, size_y):
            for i in range(0, rect.width, size_x):
                sheet.set_clip(pygame.Rect(start_x, start_y, size_x, size_y))
                sprite = sheet.subsurface(sheet.get_clip())
                #sprite = pygame.transform.scale(sprite, (192, 192))
                self.sprites.append(sprite)
                start_x += size_x

            start_y += size_y
            start_x = 0

    def update(self):
        self.x += self.speedx
        self.y += self.speedy

        if self.moving == True:
            self.delay += 1
        if self.speedy > 2:
            self.fall = True

        if self.fall == True:
            self.select = 8
            self.delay = 0
        elif self.jumped == True:
            self.select = 7
            self.delay = 0
        elif self.select >= 6 and self.delay == 9 and self.moving == True:
            self.select = 1
            self.delay = 0
        elif self.delay == 9 and self.moving == True and self.jumped == False:
            self.select += 1
            self.delay = 0
        elif self.moving == False and self.jumped == False and self.fall == False:
            self.select = 0
            self.delay = 0

        sprite = self.sprites[self.select]
        if self.direction == 1:
            self.rect = pygame.Rect(self.x, self.y+84, 40, 2)
            self.display.blit(sprite, (self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y+84, 40, 2)
            sprite = pygame.transform.flip(sprite, True, False)
            self.display.blit(sprite, (self.x, self.y))
            
    def move_r(self):
        self.speedx = 4
        self.moving = True
        self.direction = 1

    def move_l(self):
        self.speedx = -4
        self.moving = True
        self.direction = 0

    def jump(self):
        if self.njump == 2:
            pass
        else:
            self.speedy = -10
            self.jumped = True
            self.fall = False
            self.njump += 1
            
    def stop(self, event):
        if event == pygame.K_RIGHT and self.speedx != -4:
            self.speedx = 0
            self.moving = False
        elif event == pygame.K_LEFT and self.speedx != 4:
            self.speedx = 0
            self.moving = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, x1, y1)
        self.image = image
        self.display = pygame.display.get_surface()

    def draw(self, x, x1, y, info):
        for i in range(x, x1):
            self.display.blit(self.image, (32*i, info.current_h//4*y))
        
def main():
    pygame.init()
    info = pygame.display.Info()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    background = pygame.image.load("portal.jpg").convert_alpha()
    background = pygame.transform.scale(background, (info.current_w, info.current_h))

    font = pygame.font.SysFont("comicsansms", 24)

    player = Player(info.current_w//2 - 20, -130)
    player.load_sheet((0, 0), (40, 86), "pls.png")
    #takes start pos and then size not end pos!
    platform_top = Platform(info.current_w//12*4, info.current_h//4, info.current_w//12*4, 16,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midl = Platform(info.current_w//12, info.current_h//4*2, info.current_w//12*2, 16,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midd = Platform(info.current_w//12*5, info.current_h//4*2, info.current_w//12*2, 16,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midr = Platform(info.current_w//12*9, info.current_h//4*2, info.current_w//12*2, 16,
                            pygame.image.load("tile.png").convert_alpha())
    platform_botl = Platform(info.current_w//12*2, info.current_h//4*3, info.current_w//12*3, 32,
                            pygame.image.load("tile.png").convert_alpha())
    platform_botr = Platform(info.current_w//12*7, info.current_h//4*3, info.current_w//12*3, 32,
                            pygame.image.load("tile.png").convert_alpha())
    
    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_l()
            elif event.key == pygame.K_RIGHT:
                player.move_r()
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_DOWN:
                print("")
            elif event.key == pygame.K_j:
                print("")
            elif event.key == pygame.K_F1:
                pygame.display.iconify()
        elif event.type == pygame.KEYUP:
            player.stop(event.key)
            
        display.blit(background, (0, 0))
        display.blit(font.render("FPS: " + str(int(clock.get_fps())), 1, (0,0,0)), (0,0))

        if pygame.sprite.collide_rect(player, platform_top) ==  True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        elif pygame.sprite.collide_rect(player, platform_midl) == True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4*2 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        elif pygame.sprite.collide_rect(player, platform_midd) == True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4*2 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        elif pygame.sprite.collide_rect(player, platform_midr) == True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4*2 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        elif pygame.sprite.collide_rect(player, platform_botl) == True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4*3 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        elif pygame.sprite.collide_rect(player, platform_botr) == True and player.speedy > 0:
            player.speedy = 0
            player.y = info.current_h//4*3 - 85
            player.njump = 0
            player.jumped = False
            player.fall = False
        else:
            player.speedy += 0.35
        
        player.update()
        #screen divided into 60 32x32 squares in width divided in groups of 5,
        #first parameter is first square pos(x axis),
        #second is last square pos(x axis), height is divided into quarters of screen,
        #third parameter is which quarter the platform is on, last parameter is the screen info
        platform_top.draw((info.current_w // 32)//12*4, (info.current_w // 32)//12*8, 1, info)
        platform_midl.draw((info.current_w // 32)//12, (info.current_w // 32)//12*3, 2, info)
        platform_midd.draw((info.current_w // 32)//12*5, (info.current_w // 32)//12*7, 2, info)
        platform_midd.draw((info.current_w // 32)//12*9, (info.current_w // 32)//12*11, 2, info)
        platform_botl.draw((info.current_w // 32)//12*2, (info.current_w // 32)//12*5, 3, info)
        platform_botr.draw((info.current_w // 32)//12*7, (info.current_w // 32)//12*10, 3, info)

        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption("Super Smash Heroes")
        
    pygame.quit()

if __name__ == "__main__":
    main()
