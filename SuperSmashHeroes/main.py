import pygame
from pygame import *

class Player(pygame.sprite.Sprite):
    def __init__(self, rect, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.rect.x = x
        self.rect.y = y
        self.image = image
        self.speedx = 0
        self.speedy = 8
        self.njump = 0
        self.colided = False
        self.display = pygame.display.get_surface()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def move_r(self):
        self.speedx = 4

    def move_l(self):
        self.speedx = -4

    def jump(self):
        if self.njump == 2:
            pass
        else:
            self.speedy = -10
            self.njump += 1
            

    def stop(self, event):
        if event == pygame.K_RIGHT and self.speedx != -4:
            self.speedx = 0
        elif event == pygame.K_LEFT and self.speedx != 4:
            self.speedx = 0

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

    player = Player(pygame.Rect(0, 0, 40, 86), pygame.image.load("Sprite.png").convert_alpha(),
                    info.current_w//2 - 20, -130)
    #takes start pos and then size not end pos!
    platform_top = Platform(info.current_w//12*4, info.current_h//4, info.current_w//12*4, 1,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midl = Platform(info.current_w//12, info.current_h//4*2, info.current_w//12*2, 32,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midd = Platform(info.current_w//12*5, info.current_h//4*2, info.current_w//12*2, 32,
                            pygame.image.load("tile.png").convert_alpha())
    platform_midr = Platform(info.current_w//12*9, info.current_h//4*2, info.current_w//12*2, 32,
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

        if pygame.sprite.collide_rect(player, platform_top) == True and player.speedy > 0:
            player.rect.y = info.current_h//4 - 85
            player.speedy = 0
            player.njump = 0
        elif pygame.sprite.collide_rect(player, platform_midl) == True and player.speedy > 0:
            player.speedy = 0
            player.rect.y = info.current_h//4*2 - 85
            player.njump = 0
        elif pygame.sprite.collide_rect(player, platform_midd) == True and player.speedy > 0:
            player.speedy = 0
            player.rect.y = info.current_h//4*2 - 85
            player.njump = 0
        elif pygame.sprite.collide_rect(player, platform_midr) == True and player.speedy > 0:
            player.speedy = 0
            player.rect.y = info.current_h//4*2 - 85
            player.njump = 0
        elif pygame.sprite.collide_rect(player, platform_botl) == True and player.speedy > 0:
            player.speedy = 0
            player.rect.y = info.current_h//4*3 - 85
            player.njump = 0
        elif pygame.sprite.collide_rect(player, platform_botr) == True and player.speedy > 0:
            player.speedy = 0
            player.rect.y = info.current_h//4*3 - 85
            player.njump = 0
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
